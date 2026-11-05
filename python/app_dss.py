# -*- coding: utf-8 -*-
"""DSS CompanyX – giao diện 5 màn hình theo Bảng 3.32 (mục 3.5.6), viết cho người quản lý không chuyên kỹ thuật.
Chạy:  streamlit run python/app_dss.py   (theme sáng trong .streamlit/config.toml)
Dữ liệu: results/cum6/dss_khach.csv (sinh bởi cum6_phan_tich_dss.py). Đặt DSS_SOURCE=db để đọc trực tiếp CompanyX_DW khi có pyodbc."""
import os, sys, json
import pandas as pd, numpy as np
import streamlit as st
import altair as alt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as C
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); R6 = f'{ROOT}/results/cum6'; R4 = f'{ROOT}/results/cum4'
st.set_page_config(page_title='DSS CompanyX', layout='wide', initial_sidebar_state='expanded')

# ---------------- kiểu dáng: nền sáng, không bo góc, chữ rõ ----------------
NAVY, GREY, RED, GREEN, LIGHT = '#1F3A5F', '#5F6B7A', '#B42318', '#1E7F4F', '#F3F5F7'
st.markdown(f"""
<style>
  html, body, [class*="css"] {{ font-family: Arial, Helvetica, sans-serif; }}
  * {{ border-radius: 0 !important; }}
  .block-container {{ padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1250px; }}
  h1 {{ font-size: 1.55rem; font-weight: 700; color: {NAVY}; border-bottom: 2px solid {NAVY}; padding-bottom: .35rem; margin-bottom: .6rem; }}
  h2 {{ font-size: 1.15rem; font-weight: 700; color: {NAVY}; margin-top: 1.4rem; }}
  h3 {{ font-size: 1.0rem; font-weight: 700; color: #1C1C1C; }}
  [data-testid="stMetric"] {{ background: #FFFFFF; border: 1px solid #C9D1DA; padding: .6rem .8rem; }}
  [data-testid="stMetricLabel"] {{ color: {GREY}; font-size: .82rem; }}
  [data-testid="stMetricValue"] {{ color: #1C1C1C; font-size: 1.45rem; font-weight: 700; }}
  [data-testid="stSidebar"] {{ background: {LIGHT}; border-right: 1px solid #C9D1DA; }}
  [data-testid="stSidebar"] h1 {{ border: none; font-size: 1.2rem; }}
  .stButton > button, .stDownloadButton > button {{ background: {NAVY}; color: #fff; border: 1px solid {NAVY}; font-weight: 600; }}
  .stButton > button:hover, .stDownloadButton > button:hover {{ background: #2C5282; border-color: #2C5282; color: #fff; }}
  .tag {{ display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.02em; padding:.1rem .45rem; border:1px solid; margin-right:.35rem; vertical-align:middle; }}
  .tag-du-lieu {{ color:{NAVY}; border-color:{NAVY}; }}  .tag-du-doan {{ color:#7A4E00; border-color:#7A4E00; }}  .tag-gia-dinh {{ color:#5B2C83; border-color:#5B2C83; }}
  .ghi-chu {{ background:{LIGHT}; border: 1px solid #C9D1DA; padding:.55rem .8rem; color:#1C1C1C; font-size:.9rem; margin:.4rem 0 .9rem 0; }}
  .canh-bao {{ background:#FDF2F0; border: 1px solid #E4B4AE; padding:.55rem .8rem; font-size:.9rem; margin:.4rem 0; }}
  .on {{ background:#EEF7F1; border: 1px solid #B7D9C3; padding:.55rem .8rem; font-size:.9rem; margin:.4rem 0; }}
  thead tr th {{ background:{LIGHT} !important; color:#1C1C1C !important; font-weight:700 !important; }}
  [data-testid="stDataFrame"] {{ border: 1px solid #C9D1DA; }}
</style>""", unsafe_allow_html=True)
def tag(kind): return {'du_lieu': '<span class="tag tag-du-lieu">DỮ LIỆU THỰC TẾ</span>', 'du_doan': '<span class="tag tag-du-doan">DỰ ĐOÁN CỦA MÔ HÌNH</span>', 'gia_dinh': '<span class="tag tag-gia-dinh">THEO GIẢ ĐỊNH</span>'}[kind]
def tags(*k): st.markdown(''.join(tag(x) for x in k), unsafe_allow_html=True)
def ghi_chu(s): st.markdown(f'<div class="ghi-chu">{s}</div>', unsafe_allow_html=True)
def vn(x, d=0):
    if x is None or (isinstance(x, float) and np.isnan(x)): return '—'
    s = f'{x:,.{d}f}'; return s.replace(',', '#').replace('.', ',').replace('#', '.')
def usd(x): return vn(x) + ' USD'
def pct(x, d=1): return '—' if x is None or (isinstance(x, float) and np.isnan(x)) else vn(100 * x, d) + '%'
def fmt(d=0): return lambda x: vn(x, d)          # dùng trong Styler.format để mọi bảng hiển thị số kiểu Việt
def fpct(d=1): return lambda x: pct(x, d)

# Diễn giải luật lá cây (TopFactors) sang lời cho người quản lý. Dữ liệu gốc trong kho giữ nguyên, chỉ đổi cách hiển thị.
_TEN_TT = {'Recency': ('lần mua gần nhất cách đây', 'ngày'), 'Monetary': ('tổng chi tiêu', 'USD'), 'Tenure': ('đã là khách được', 'ngày'), 'Frequency': ('số đơn đã mua', 'đơn'),
           'Orders90': ('số đơn trong 90 ngày gần nhất', 'đơn'), 'Orders180': ('số đơn trong 180 ngày gần nhất', 'đơn'), 'NSub': ('số danh mục đã mua', 'danh mục')}
def de_hieu(top):
    import re
    if not isinstance(top, str) or ':' not in top: return top
    head, rest = top.split(':', 1); rule, _, info = rest.partition('|'); parts = []; bound = {}
    for f, op, val in re.findall(r'(\w+) (<=|>) ([\d.]+)', rule):                 # gộp các điều kiện cùng thuộc tính thành một khoảng (lo, hi]
        lo, hi = bound.get(f, (None, None)); v = float(val)
        bound[f] = (max(lo, v) if (op == '>' and lo is not None) else (v if op == '>' else lo), min(hi, v) if (op == '<=' and hi is not None) else (v if op == '<=' else hi))
    for f, (lo, hi) in bound.items():
        if f == 'BikeBuyer': parts.append('chủ yếu mua xe đạp' if lo is not None else 'chủ yếu mua phụ kiện, quần áo'); continue
        if f.startswith('Share_'): ten, show = 'tỷ trọng ' + dict(Share_Bikes='xe đạp', Share_Accessories='phụ kiện', Share_Clothing='quần áo')[f], (lambda x: pct(x, 0))
        else: ten, dv = _TEN_TT.get(f, (f, '')); show = (lambda x, dv=dv: f'{vn(int(x))} {dv}')
        parts.append(f'{ten} từ {show(lo)} đến {show(hi)}' if lo is not None and hi is not None else f'{ten} trên {show(lo)}' if lo is not None else f'{ten} không quá {show(hi)}')
    m = re.search(r'nhóm (\d+) khách, tỷ lệ không mua lại ([\d.]+)%', info)
    tail = f'. Lúc huấn luyện nhóm này có {vn(int(m.group(1)))} khách, {vn(float(m.group(2)), 1)}% không mua lại trong 90 ngày' if m else ''
    return f'{head.strip()}: ' + ', '.join(parts) + tail + '.'

CHAN = {'R3': ('Liên hệ cá nhân kèm ưu đãi', 25.0, 0.15), 'R4': ('Mời quay lại kèm ưu đãi', 15.0, 0.12), 'R5': ('Email cá nhân hoá tự động', 3.0, 0.05)}
TEN = {'N1': 'N1 – Mua nhiều lần, giá trị cao', 'N2': 'N2 – Mua một lần, giá trị trung bình', 'N3': 'N3 – Mua một lần, đã lâu không quay lại', 'N4': 'N4 – Mua lặp lại, giá trị thấp', 'N5': 'N5 – Mua một lần, giá trị thấp'}
MAU_NHOM = {'N1': NAVY, 'N2': '#4A7FB5', 'N3': '#9B2C2C', 'N4': '#7A4E00', 'N5': '#8A94A6'}

@st.cache_data
def load():
    df = pd.read_csv(f'{R6}/dss_khach.csv'); df[['SanPhamGoiY', 'QuyTacSP']] = df[['SanPhamGoiY', 'QuyTacSP']].fillna('')
    if os.getenv('DSS_SOURCE') == 'db':
        try:
            con = C.connect(); live = pd.read_sql("SELECT r.CustomerID, r.RiskScore, r.RiskPercentile, r.RiskLevel, r.TreeScore, r.TopFactors, s.ABCClass AS ABC FROM analytics.CustomerRiskScore r JOIN analytics.CustomerSegment s ON s.CustomerID=r.CustomerID AND s.SnapshotDate=r.ScoreDate JOIN analytics.ModelRegistry m ON m.ModelVersion=r.ModelVersion AND m.IsActive=1 AND m.ModelRole='SCORING'", con)
            df = df.drop(columns=['RiskScore', 'RiskPercentile', 'RiskLevel', 'TreeScore', 'TopFactors', 'ABC']).merge(live, on='CustomerID')
        except Exception as e: st.sidebar.warning(f'Không nối được kho, dùng dữ liệu đã xuất: {e}')
    return df
df = load()
folds = pd.read_csv(f'{R4}/bang_4_3_2a_theo_fold.csv'); moc = pd.read_csv(f'{ROOT}/results/cum3b/bang_4_3_1a_moc.csv')

def solve(d, r, c, B, kenh=False):
    """Chọn khách theo giá trị kỳ vọng trong ngân sách (mục 3.5.4). kenh=True: chi phí và tỷ lệ thành công theo kênh R3–R5."""
    p, v = d.RiskScore.values, d.v.values
    ck, rk = (d.c_k.values, d.r_k.values) if kenh else (np.full(len(d), c), np.full(len(d), r))
    ev = p * rk * v - ck; ok = ev > 0; order = np.argsort(-(ev / ck)) if kenh else np.argsort(-(p * v))
    cum = np.cumsum(ck[order]); sel = order[(cum <= B) & ok[order]]; return sel, ev
def hist_chart(series, title, color=NAVY, x_title='RiskScore'):
    h = pd.DataFrame({'khoang': [f'{i / 20:.2f}–{(i + 1) / 20:.2f}' for i in range(20)], 'so_khach': np.histogram(series, bins=20, range=(0, 1))[0]})
    h['khoang'] = h.khoang.str.replace('.', ',', regex=False)
    return alt.Chart(h).mark_bar(color=color).encode(x=alt.X('khoang:N', title=x_title, sort=None, axis=alt.Axis(labelAngle=-45)), y=alt.Y('so_khach:Q', title='Số khách', axis=alt.Axis(labelExpr="replace(format(datum.value, ',.0f'), ',', '.')")),
                                                     tooltip=[alt.Tooltip('khoang', title='Khoảng'), alt.Tooltip('so_khach', title='Số khách')]).properties(height=260, title=title)

# ---------------- thanh bên ----------------
st.sidebar.title('DSS CompanyX')
st.sidebar.markdown(f'<div style="font-size:.85rem;color:{GREY}">Hệ hỗ trợ quyết định chăm sóc khách hàng<br>Mốc chấm điểm: <b>{pd.Timestamp(C.SCORING_DATE):%d/%m/%Y}</b><br>Mô hình đang dùng: Naive Bayes, học ở {pd.Timestamp(C.SCORING_TRAIN_DATE):%d/%m/%Y}</div>', unsafe_allow_html=True)
st.sidebar.markdown('---')
man = st.sidebar.radio('Màn hình', ['Hướng dẫn sử dụng', '1. Tổng quan rủi ro', '2. Hồ sơ khách hàng', '3. Phân tích kịch bản', '4. Danh sách chăm sóc', '5. Theo dõi mô hình và quy tắc'],
                       format_func=lambda s: s.replace('. ', '\\. ', 1) if s[0].isdigit() else s, label_visibility='visible')   # thoát dấu chấm để số thứ tự không bị hiểu là danh sách
vai_tro = st.sidebar.selectbox('Bạn đang dùng với vai trò', ['Quản lý Marketing/Sales', 'Nhân viên phân tích dữ liệu', 'Nhân viên chăm sóc khách hàng'])
st.sidebar.markdown('---')
st.sidebar.markdown(f'<div style="font-size:.8rem;color:{GREY}"><b>Cách đọc nhãn</b><br>{tag("du_lieu")}<br>số thật từ kho dữ liệu<br>{tag("du_doan")}<br>xác suất do mô hình tính<br>{tag("gia_dinh")}<br>phụ thuộc r, c, B bạn nhập</div>', unsafe_allow_html=True)

# ================= 0. HƯỚNG DẪN SỬ DỤNG =================
if man.startswith('Hướng dẫn'):
    st.title('Hướng dẫn sử dụng DSS CompanyX'); tags('du_lieu', 'du_doan', 'gia_dinh')
    ghi_chu('Hệ thống giúp trả lời một câu hỏi: <b>với ngân sách có hạn, nên chăm sóc những khách nào để giữ được nhiều giá trị nhất?</b> Bạn không cần biết mô hình bên trong. Làm theo 5 bước dưới đây, mỗi bước là một màn hình ở thanh bên trái, mất khoảng 10 phút.')
    st.subheader('Trước khi bắt đầu: ba khái niệm cần nắm')
    st.markdown(f"""
| Khái niệm | Nghĩa đơn giản | Ở đâu trên màn hình |
|---|---|---|
| **Xác suất không mua lại** | Khả năng (0 đến 1) khách này không đặt đơn nào trong 90 ngày tới, do mô hình tính từ lịch sử mua | Cột "Xác suất không mua lại", nhãn {tag('du_doan')} |
| **Mức rủi ro Cao / Thấp** | Cao = thuộc 25% khách có xác suất cao nhất **trong cùng hạng giá trị** (A, B hoặc C). Là mức ưu tiên tương đối, không phải lời khẳng định khách sẽ bỏ đi | Thẻ số và cột "Mức rủi ro" |
| **Giá trị ròng Z** | Lợi nhuận kỳ vọng từ những khách được giữ lại, trừ đi chi phí chăm sóc. Phụ thuộc ba con số bạn nhập: r, c, B | Màn hình 3 và 4, nhãn {tag('gia_dinh')} |
""", unsafe_allow_html=True)
    st.markdown(f"""
Ba con số bạn sẽ nhập ở màn hình 3:
- **r** – tỷ lệ chăm sóc thành công: trong 100 khách được chăm sóc mà lẽ ra sẽ bỏ đi, bao nhiêu người quay lại mua. Mặc định 10%.
- **c** – chi phí cho mỗi khách được chăm sóc (liên hệ cộng ưu đãi). Mặc định 10 USD.
- **B** – ngân sách chiến dịch. Mặc định 40.000 USD.
""")
    st.markdown('---')
    buoc = [
        ('Bước 1 – Xem tình hình chung', '1. Tổng quan rủi ro', [
            'Nhìn bốn thẻ số ở trên: tổng số khách, số khách rủi ro Cao, tổng tiền họ đã mua, số khách cần xem xét thêm.',
            'Nhìn **Ma trận Rủi ro × Giá trị** bên phải. Ô đáng chú ý nhất là **A – Cao**: khách giá trị lớn nhưng có nguy cơ rời bỏ.',
            'Dùng hai bộ lọc phía trên để thu hẹp theo nhóm khách hoặc hạng giá trị, mọi số bên dưới tự tính lại.',
            'Bảng **Năm nhóm khách hàng** cho biết mỗi nhóm mua như thế nào. Bảng cuối liệt kê 20 khách rủi ro Cao có giá trị lớn nhất, ghi lại vài mã khách để xem ở bước 2.']),
        ('Bước 2 – Xem một khách cụ thể', '2. Hồ sơ khách hàng', [
            'Nhập mã khách vào ô "Mã khách" (ví dụ một mã lấy từ bước 1).',
            'Đọc năm thẻ số: lần mua gần nhất cách đây bao nhiêu ngày, đã mua mấy đơn, tổng chi tiêu, xác suất không mua lại, mức rủi ro.',
            'Ô "Khách này thuộc nhóm nào theo cây đối chứng" mô tả nhóm khách có đặc điểm giống nhau và tỷ lệ bỏ đi của nhóm đó. Đây là cách nhìn thứ hai để đối chiếu.',
            'Nếu thấy ô đỏ **Cần xem xét thêm**: hai cách nhìn không thống nhất, nên hỏi thêm đội bán hàng trước khi quyết định. Ô xanh nghĩa là hai cách nhìn khớp nhau.',
            'Phần **Khuyến nghị chăm sóc** cho biết nên liên hệ bằng hình thức nào, tốn bao nhiêu, kỳ vọng thu về bao nhiêu và gợi ý sản phẩm gì.']),
        ('Bước 3 – Thử các kịch bản ngân sách', '3. Phân tích kịch bản', [
            'Kéo ba thanh trượt r, c, B. Bốn thẻ số bên dưới (Z, số khách, chi phí, số khách giữ lại) tự tính lại ngay.',
            'Bấm **Lưu kịch bản này** sau mỗi lần thử để so sánh các phương án trong bảng bên cạnh.',
            'Chọn một kỹ thuật ở hàng nút: **So sánh các kịch bản** (bảng có sẵn), **Độ nhạy** (tham số nào ảnh hưởng Z nhiều nhất), **Tìm mục tiêu** (cần r bao nhiêu để hoà vốn hoặc đạt Z mong muốn), **Z theo ngân sách khi chưa biết r** (ba tiêu chí lạc quan, bi quan, kỳ vọng), **Mô phỏng** (xác suất lỗ), **Theo kênh** (chi phí khác nhau cho từng hình thức liên hệ).',
            'Nhớ rằng mọi số ở đây mang nhãn THEO GIẢ ĐỊNH: đúng trong phạm vi r, c, B bạn nhập.']),
        ('Bước 4 – Duyệt danh sách chăm sóc', '4. Danh sách chăm sóc', [
            'Nhập ngân sách B. Giữ ô "theo kênh" được tích để chi phí và tỷ lệ thành công khác nhau theo hình thức liên hệ.',
            'Đọc ba thẻ số: số khách, tổng chi phí (có báo nếu vượt ngân sách) và Z sau điều chỉnh.',
            'Muốn thêm hoặc bớt khách: gõ mã khách vào ô, dấu trừ phía trước để bớt (ví dụ 11000, -19785), và **bắt buộc ghi lý do**. Hệ thống tính lại ngay.',
            'Mỗi dòng trong bảng có hình thức liên hệ, sản phẩm gợi ý và cột **Giải thích** nói vì sao khách được chọn.',
            'Bấm **Xuất danh sách đã duyệt (CSV)** để gửi cho đội chăm sóc. Vai trò "Nhân viên phân tích" không có nút này.']),
        ('Bước 5 – Kiểm tra mô hình còn tốt không', '5. Theo dõi mô hình và quy tắc', [
            'Biểu đồ đầu so mô hình đang dùng với quy tắc đơn giản "khách lâu không mua thì rủi ro cao". Đường mô hình phải nằm bằng hoặc trên đường quy tắc, nếu không thì cần huấn luyện lại.',
            'Bảng **Cơ cấu khách thay đổi theo thời gian** giải thích vì sao mỗi kỳ phải huấn luyện lại.',
            'Bảng **Phiên bản** cho biết mô hình và quy tắc nào đang được dùng, để ghi vào biên bản chiến dịch.',
            'Quản lý và nhân viên phân tích có thể đề xuất quy tắc mới ở cuối trang, quy tắc sẽ ở trạng thái chờ duyệt.']),
    ]
    for i, (ten, man_hinh, cac_buoc) in enumerate(buoc):
        with st.expander(f'{ten}  —  mở màn hình "{man_hinh}" ở thanh bên trái', expanded=(i == 0)):
            for j, b in enumerate(cac_buoc, 1): st.markdown(f'{j}. {b}')
    st.markdown('---')
    st.subheader('Câu hỏi thường gặp')
    st.markdown("""
- **Tại sao một khách giá trị lớn lại ở mức rủi ro Thấp?** Mức rủi ro so sánh trong cùng hạng giá trị. Khách đó có xác suất không mua lại thấp hơn 75% khách cùng hạng với mình.
- **Z có phải là lợi nhuận chắc chắn không?** Không. Z là giá trị kỳ vọng theo giả định r, c, B. Màn hình 3 có phần Mô phỏng để xem xác suất lỗ.
- **Tôi có thể bỏ một khách mà hệ thống chọn không?** Có, ở màn hình 4, nhưng phải ghi lý do. Hệ thống tính lại chi phí và Z.
- **Số liệu được cập nhật khi nào?** Mỗi kỳ chấm điểm (ghi ở thanh bên trái). Khi kho dữ liệu có đơn mới, nhân viên phân tích chạy lại chấm điểm và phiên bản mới xuất hiện ở màn hình 5.
- **Hệ thống có tự gửi email hay gọi khách không?** Không. Hệ thống chỉ đề xuất danh sách và hình thức, việc thực hiện do đội chăm sóc làm theo CSV đã xuất.
""")
    st.caption('Thiết kế theo Bảng 3.20 (quy trình ra quyết định), Bảng 3.31 (vai trò) và Bảng 3.32 (năm màn hình) của báo cáo.')

# ================= 1. TỔNG QUAN =================
elif man.startswith('1'):
    st.title('1. Tổng quan rủi ro khách hàng'); tags('du_lieu', 'du_doan')
    ghi_chu('Màn hình này trả lời: <b>hiện có bao nhiêu khách có nguy cơ không mua lại trong 90 ngày tới, họ thuộc nhóm nào và đáng giá bao nhiêu.</b> Rủi ro Cao = 25% khách có xác suất không mua lại cao nhất trong cùng hạng giá trị (A, B, C).')
    nhom = st.pills('Lọc theo nhóm khách (bấm để bật hoặc tắt)', list(TEN), selection_mode='multi', default=list(TEN), format_func=lambda x: TEN[x])
    abc = st.pills('Lọc theo hạng giá trị (ABC)', ['A', 'B', 'C'], selection_mode='multi', default=['A', 'B', 'C'], format_func=lambda x: {'A': 'A – 28% khách giữ 80% doanh thu', 'B': 'B – 14% khách giữ 15% doanh thu', 'C': 'C – 58% khách giữ 5% doanh thu'}[x])
    if not nhom or not abc: st.markdown('<div class="canh-bao">Chưa chọn nhóm hoặc hạng nào. Bấm vào ít nhất một nhóm và một hạng ở trên.</div>', unsafe_allow_html=True); st.stop()
    d = df[df.Nhom.isin(nhom) & df.ABC.isin(abc)]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric('Số khách đang xem', vn(len(d))); k2.metric('Khách rủi ro Cao', f'{vn((d.RiskLevel == "Cao").sum())}  ({pct((d.RiskLevel == "Cao").mean())})')
    k3.metric('Đã mua (khách Cao)', usd(d.loc[d.RiskLevel == 'Cao', 'Monetary'].sum()), help='Tổng tiền các khách rủi ro Cao đã mua từ trước đến mốc chấm điểm')
    k4.metric('Cần xem xét thêm', vn(int(d.Flag.sum())), help='Số khách mà cây đối chứng và mô hình chấm điểm lệch nhau quá 0,3')
    a, b = st.columns([3, 2])
    with a:
        st.subheader('Phân bố xác suất không mua lại'); st.altair_chart(hist_chart(d.RiskScore, ''), use_container_width=True)
    with b:
        st.subheader('Ma trận Rủi ro × Giá trị (số khách)')
        mx = pd.crosstab(d.ABC, d.RiskLevel).reindex(index=['A', 'B', 'C'], columns=['Cao', 'Thấp']).fillna(0).astype(int); mx.index.name = 'Hạng'; st.dataframe(mx.rename(columns={'Cao': 'Rủi ro Cao', 'Thấp': 'Rủi ro Thấp'}), use_container_width=True)
        st.caption('Ô "A – Cao" là nơi đáng chú ý nhất: khách giá trị lớn nhưng có nguy cơ rời bỏ.')
    st.subheader('Năm nhóm khách hàng')
    g = d.groupby('Nhom').agg(so_khach=('CustomerID', 'size'), recency_trung_vi=('Recency', 'median'), so_don_TB=('Frequency', 'mean'), chi_tieu_trung_vi=('Monetary', 'median'), ty_le_rui_ro_cao=('RiskLevel', lambda x: (x == 'Cao').mean()), hang_A=('ABC', lambda x: (x == 'A').sum())).reindex(list(TEN)).dropna(how='all')
    out = pd.DataFrame({'Nhóm': [TEN[i] for i in g.index], 'Số khách': [vn(v) for v in g.so_khach], 'Ngày từ lần mua gần nhất (trung vị)': [vn(v) for v in g.recency_trung_vi], 'Số đơn trung bình': [vn(v, 2) for v in g.so_don_TB], 'Chi tiêu trung vị (USD)': [vn(v) for v in g.chi_tieu_trung_vi], 'Tỷ lệ rủi ro Cao': [pct(v) for v in g.ty_le_rui_ro_cao], 'Khách hạng A': [vn(v) for v in g.hang_A]})
    st.dataframe(out, hide_index=True, use_container_width=True)
    st.subheader('Xem chi tiết: 20 khách rủi ro Cao có giá trị lớn nhất')
    t = d[d.RiskLevel == 'Cao'].nlargest(20, 'Monetary')[['CustomerID', 'Nhom', 'ABC', 'Recency', 'Frequency', 'Monetary', 'RiskScore', 'RiskPercentile']].copy()
    t.columns = ['Mã khách', 'Nhóm', 'Hạng', 'Ngày từ lần mua gần nhất', 'Số đơn', 'Tổng chi tiêu (USD)', 'Xác suất không mua lại', 'Phân vị rủi ro trong hạng']
    st.dataframe(t.style.format({'Ngày từ lần mua gần nhất': fmt(), 'Tổng chi tiêu (USD)': fmt(), 'Xác suất không mua lại': fmt(3), 'Phân vị rủi ro trong hạng': fmt(1)}), hide_index=True, use_container_width=True)

# ================= 2. HỒ SƠ KHÁCH =================
elif man.startswith('2'):
    st.title('2. Hồ sơ một khách hàng'); tags('du_lieu', 'du_doan')
    ghi_chu('Nhập mã khách để xem lịch sử mua, xác suất không mua lại, nhóm, hạng và khuyến nghị chăm sóc kèm lý do.')
    cid = st.number_input('Mã khách (CustomerID)', min_value=int(df.CustomerID.min()), max_value=int(df.CustomerID.max()), value=int(df.CustomerID.iloc[0]), step=1)
    r = df[df.CustomerID == cid]
    if r.empty: st.markdown('<div class="canh-bao">Không có khách này tại mốc chấm điểm.</div>', unsafe_allow_html=True)
    else:
        r = r.iloc[0]
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric('Ngày từ lần mua gần nhất', vn(r.Recency)); k2.metric('Số đơn đã mua', vn(r.Frequency)); k3.metric('Tổng chi tiêu', usd(r.Monetary)); k4.metric('Xác suất không mua lại', vn(r.RiskScore, 3))
        k5.metric('Mức rủi ro', r.RiskLevel, help='Cao khi phân vị rủi ro trong hạng giá trị từ 75 trở lên')
        st.markdown(f'**Phân vị rủi ro trong hạng {r.ABC}:** {vn(r.RiskPercentile, 1)} (Cao khi từ 75 trở lên) &nbsp;|&nbsp; **Nhóm:** {TEN[r.Nhom]} &nbsp;|&nbsp; **Là khách được:** {vn(r.Tenure)} ngày &nbsp;|&nbsp; **Số danh mục đã mua:** {vn(r.NSub)} &nbsp;|&nbsp; **Tỷ trọng xe đạp:** {pct(r.Share_Bikes, 0)}')
        st.subheader('Khách này thuộc nhóm nào theo cây đối chứng')
        st.markdown(f'<div class="ghi-chu">{de_hieu(r.TopFactors)}<br><span style="color:{GREY};font-size:.85rem">Đây là mô tả nhóm khách có đặc điểm giống nhau, không phải lý do của xác suất ở trên.</span></div>', unsafe_allow_html=True)
        if r.Flag: st.markdown(f'<div class="canh-bao"><b>Cần xem xét thêm.</b> Cây đối chứng cho {vn(r.TreeScore, 3)} nhưng mô hình chấm điểm cho {vn(r.RiskScore, 3)}, lệch nhau quá {vn(C.TREE_FLAG_GAP, 1)}. Hai cách nhìn không thống nhất, nên hỏi thêm đội bán hàng trước khi quyết định.</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="on">Hai mô hình thống nhất (cây đối chứng cho {vn(r.TreeScore, 3)}).</div>', unsafe_allow_html=True)
        st.subheader('Khuyến nghị chăm sóc'); tags('gia_dinh')
        ten, ck, rk = CHAN[r.KenhRule]; ev = r.RiskScore * rk * r.v - ck
        st.markdown(f'- Giá trị một lần mua nếu giữ được khách: **{usd(r.v)}** (lợi nhuận gộp 41,15% × giá trị đơn trung bình)\n- Hình thức liên hệ theo quy tắc **{r.KenhRule}: {ten}**, chi phí {usd(ck)}, tỷ lệ thành công giả định {pct(rk, 0)}\n- Giá trị kỳ vọng của việc chăm sóc: **{vn(ev, 2)} USD** → ' + ('<b>đủ điều kiện đưa vào danh sách</b>' if ev > 0 else '<b>không đưa vào danh sách cá nhân</b> (quy tắc R2: chi phí lớn hơn lợi ích kỳ vọng)') + f'\n- Sản phẩm gợi ý: **{r.SanPhamGoiY or "nội dung mặc định (giới thiệu chung các nhóm phụ kiện)"}** {("(quy tắc " + r.QuyTacSP + ")") if r.QuyTacSP else ""}', unsafe_allow_html=True)

# ================= 3. KỊCH BẢN =================
elif man.startswith('3'):
    st.title('3. Phân tích kịch bản chăm sóc'); tags('gia_dinh')
    ghi_chu('Bạn nhập ba con số của chiến dịch, hệ thống chọn khách có lợi nhất trong ngân sách và cho biết <b>giá trị ròng Z</b> (lợi nhuận kỳ vọng trừ chi phí). Z là giá trị kỳ vọng theo giả định, không phải lợi nhuận chắc chắn.')
    c1, c2, c3 = st.columns(3)
    r = c1.slider('Tỷ lệ chăm sóc thành công r (%): trong 100 khách được chăm sóc, bao nhiêu người quay lại mua', 1, 30, int(C.BASE_SCENARIO['r'] * 100), 1, format='%d%%') / 100
    c = c2.slider('Chi phí cho mỗi khách được chăm sóc c (USD)', 1, 30, int(C.BASE_SCENARIO['c']), 1, format='%d USD') * 1.0
    B = c3.slider('Ngân sách chiến dịch B (USD)', 5000, 150000, int(C.BASE_SCENARIO['B']), 5000, format='%d USD')
    sel, ev = solve(df, r, c, B); Z = ev[sel].sum()
    k1, k2, k3, k4 = st.columns(4); k1.metric('Giá trị ròng Z', usd(Z)); k2.metric('Số khách được chọn', vn(len(sel))); k3.metric('Tổng chi phí', usd(c * len(sel))); k4.metric('Số khách giữ lại kỳ vọng', vn((df.RiskScore.values[sel] * r).sum()))
    cl, cr = st.columns([1, 3])
    if cl.button('Lưu kịch bản này'): st.session_state.setdefault('kich_ban', []).append({'r': pct(r, 0), 'c': usd(c), 'B': usd(B), 'Z': usd(Z), 'Số khách': vn(len(sel))}); st.toast('Đã lưu kịch bản vào bảng so sánh')
    if st.session_state.get('kich_ban'):
        cr.dataframe(pd.DataFrame(st.session_state['kich_ban']), hide_index=True, use_container_width=True)
        if cl.button('Xoá các kịch bản đã lưu'): st.session_state['kich_ban'] = []; st.rerun()
    st.subheader('Kỹ thuật phân tích')
    kt = st.radio('', ['So sánh các kịch bản (what-if)', 'Độ nhạy: thay đổi từng tham số ±20%', 'Tìm mục tiêu: cần r bao nhiêu để đạt Z', 'Z theo ngân sách khi chưa biết r', 'Mô phỏng khi r không chắc chắn', 'Chi phí và tỷ lệ thành công theo kênh'], horizontal=True, label_visibility='collapsed')
    if kt.startswith('So sánh'):
        w = pd.read_csv(f'{R6}/bang_4_4_what_if.csv'); w = w.rename(columns={'kich_ban': 'Kịch bản', 'r': 'r', 'c': 'c (USD)', 'B': 'B (USD)', 'Z': 'Z (USD)', 'K': 'Số khách', 'C': 'Chi phí (USD)', 'giu_lai_ky_vong': 'Khách giữ lại kỳ vọng', 'delta_Z': 'Chênh so với cơ sở (USD)'})
        st.dataframe(w.style.format({'r': fpct(0), 'c (USD)': fmt(), 'Z (USD)': fmt(), 'B (USD)': fmt(), 'Số khách': fmt(), 'Chi phí (USD)': fmt(), 'Chênh so với cơ sở (USD)': lambda x: ('+' if x > 0 else '') + vn(x), 'Khách giữ lại kỳ vọng': fmt()}), hide_index=True, use_container_width=True)
        st.caption('Kịch bản cơ sở: r = 10%, c = 10 USD, B = 40.000 USD. Mỗi dòng giải lại bài toán chọn khách.')
    elif kt.startswith('Độ nhạy'):
        rows = []
        for ten, kw in [('Tỷ lệ thành công r', dict(r=r * 1.2)), ('Xác suất không mua lại p', dict(pm=1.2)), ('Tỷ lệ lợi nhuận gộp g', dict(gm=1.2)), ('Chi phí c', dict(c=c * 1.2)), ('Ngân sách B', dict(B=B * 1.2))]:
            d = df.copy()
            if 'pm' in kw: d['RiskScore'] = (d.RiskScore * 1.2).clip(upper=1)
            if 'gm' in kw: d['v'] = d.v * 1.2
            s_, e_ = solve(d, kw.get('r', r), kw.get('c', c), kw.get('B', B)); rows.append(dict(tham_so=ten, delta=e_[s_].sum() - Z))
        t = pd.DataFrame(rows)
        st.altair_chart(alt.Chart(t).mark_bar(color=NAVY).encode(x=alt.X('delta:Q', title='Thay đổi của Z khi tham số tăng 20% (USD)'), y=alt.Y('tham_so:N', title='', sort='-x'), tooltip=['tham_so', alt.Tooltip('delta:Q', format=',.0f')]).properties(height=220), use_container_width=True)
        st.caption('r, p và g nhân với nhau trong doanh thu nên tác động bằng nhau khi danh sách không đổi. Chi phí c và ngân sách B đổi cả số khách được chọn.')
    elif kt.startswith('Tìm'):
        S = (df.RiskScore.values[sel] * df.v.values[sel]).sum(); zt = st.number_input('Z mục tiêu (USD)', value=100000, step=10000)
        st.markdown(f'Với danh sách **{vn(len(sel))} khách** đã chốt ở trên:\n- Tỷ lệ thành công tối thiểu để **hoà vốn** (Z = 0): **{pct(c * len(sel) / S, 2)}**\n- Tỷ lệ thành công cần có để Z đạt **{usd(zt)}**: **{pct((zt + c * len(sel)) / S, 2)}**')
        st.caption('Công thức (3.25): r* = (Z* + c·K) / Σ p·v trên K khách đã chọn.')
    elif kt.startswith('Z theo'):
        p = pd.read_csv(f'{R6}/bang_4_4_payoff.csv').rename(columns={'B': 'Ngân sách B (USD)', 'K': 'Số khách', 'r=2%': 'Z nếu r = 2% (bi quan)', 'r=10%': 'Z nếu r = 10% (cơ sở)', 'r=20%': 'Z nếu r = 20% (lạc quan)', 'gia_tri_ky_vong': 'Giá trị kỳ vọng (30/50/20%)'})
        st.dataframe(p.style.format(fmt()), hide_index=True, use_container_width=True)
        st.markdown('- **Lạc quan** (tốt nhất trong các kết quả tốt nhất): chọn B = 100.000 USD\n- **Bi quan** (tốt nhất trong các kết quả xấu nhất): chọn B = 40.000 USD\n- **Giá trị kỳ vọng lớn nhất**: chọn B = 100.000 USD\n\nPhương án cuối cùng tuỳ mức chấp nhận rủi ro của người quản lý.')
    elif kt.startswith('Mô phỏng'):
        sim = json.load(open(f'{R6}/mo_phong.json'))
        k1, k2, k3, k4 = st.columns(4); k1.metric('Z trung bình', usd(sim['Z_mean'])); k2.metric('Z xấu nhất 5%', usd(sim['Z_P5'])); k3.metric('Z tốt nhất 5%', usd(sim['Z_P95'])); k4.metric('Xác suất lỗ (Z < 0)', pct(sim['P_Z_am']))
        st.image(f'{R6}/hinh_4_4_mo_phong.png', use_container_width=True)
        st.caption('10.000 lần rút r từ phân phối Beta (trung bình 9,9%, 90% khối lượng trong 2–22%) với danh sách 4.000 khách của kịch bản cơ sở.')
    else:
        selk, evk = solve(df, r, c, B, kenh=True)
        k1, k2, k3 = st.columns(3); k1.metric('Giá trị ròng Z theo kênh', usd(evk[selk].sum())); k2.metric('Số khách được chọn', vn(len(selk))); k3.metric('Tổng chi phí', usd(df.c_k.values[selk].sum()))
        kk = pd.Series(df.KenhRule.values[selk]).value_counts().rename_axis('Quy tắc').reset_index(name='Số khách'); kk['Hình thức liên hệ'] = kk['Quy tắc'].map(lambda k: CHAN[k][0]); kk['Chi phí mỗi khách (USD)'] = kk['Quy tắc'].map(lambda k: CHAN[k][1]); kk['Tỷ lệ thành công'] = kk['Quy tắc'].map(lambda k: pct(CHAN[k][2], 0))
        st.dataframe(kk[['Quy tắc', 'Hình thức liên hệ', 'Chi phí mỗi khách (USD)', 'Tỷ lệ thành công', 'Số khách']], hide_index=True, use_container_width=True)
        st.caption('Mỗi khách được gán một kênh theo quy tắc R3–R5 (nhóm và mức rủi ro), rồi chọn khách có lợi nhất trong ngân sách (bài toán cái túi 0–1).')

# ================= 4. DANH SÁCH =================
elif man.startswith('4'):
    st.title('4. Danh sách chăm sóc'); tags('gia_dinh')
    ghi_chu('Danh sách khách được chọn theo giá trị kỳ vọng, kèm hình thức liên hệ, sản phẩm gợi ý và lý do. Bạn có thể thêm hoặc bớt khách, hệ thống tính lại chi phí và Z. Mỗi điều chỉnh thủ công được ghi vào file xuất (cột Nguồn chọn và Lý do điều chỉnh).')
    c1, c2 = st.columns([1, 2]); B = c1.number_input('Ngân sách B (USD)', value=int(C.BASE_SCENARIO['B']), step=5000); kenh = c2.checkbox('Chi phí và tỷ lệ thành công theo kênh R3–R5 (khuyên dùng)', value=True)
    sel, ev = solve(df, C.BASE_SCENARIO['r'], C.BASE_SCENARIO['c'], B, kenh=kenh); d = df.iloc[sel].copy(); d['EV'] = ev[sel]; d = d.sort_values('EV', ascending=False)
    d['NguonChon'] = 'DSS chọn'; d['LyDo'] = ''
    c3, c4 = st.columns(2); them = c3.text_input('Thêm hoặc bớt khách (mã khách, cách nhau bằng dấu phẩy, thêm dấu trừ để bớt, ví dụ 11000, -19785)', ''); ly_do = c4.text_input('Lý do điều chỉnh (bắt buộc khi thêm hoặc bớt)', '').strip()
    nhat_ky, loi = [], []
    if them.strip():
        ids_all, ids_cur = set(df.CustomerID), set(d.CustomerID)
        for tok in [t_.strip() for t_ in them.split(',') if t_.strip()]:
            bot = tok.startswith('-'); so = tok[1:].strip() if bot else tok
            if not so.isdigit() or int(so) not in ids_all: loi.append(f'{tok} (không có mã khách này)'); continue
            cid_ = int(so)
            if bot:
                if cid_ not in ids_cur: loi.append(f'{tok} (khách không có trong danh sách để bớt)'); continue
                d = d[d.CustomerID != cid_]; ids_cur.discard(cid_); nhat_ky.append(dict(thao_tac='Bớt', ma_khach=cid_, ly_do=ly_do))
            else:
                if cid_ in ids_cur: loi.append(f'{tok} (đã có trong danh sách)'); continue
                x = df[df.CustomerID == cid_].copy(); x['EV'] = (x.RiskScore * x.r_k * x.v - x.c_k) if kenh else (x.RiskScore * C.BASE_SCENARIO['r'] * x.v - C.BASE_SCENARIO['c'])
                x['NguonChon'] = 'Thêm thủ công'; x['LyDo'] = ly_do; d = pd.concat([d, x]); ids_cur.add(cid_); nhat_ky.append(dict(thao_tac='Thêm', ma_khach=cid_, ly_do=ly_do))
        if loi: st.markdown('<div class="canh-bao">Bỏ qua: ' + ', '.join(loi) + '.</div>', unsafe_allow_html=True)
    thieu_ly_do = bool(nhat_ky) and not ly_do
    if thieu_ly_do: st.markdown('<div class="canh-bao"><b>Chưa có lý do điều chỉnh.</b> Ghi lý do ở ô bên phải thì mới xuất được danh sách.</div>', unsafe_allow_html=True)
    tong = float(d.c_k.sum()) if kenh else C.BASE_SCENARIO['c'] * len(d); Z = float(d.EV.sum())
    k1, k2, k3 = st.columns(3); k1.metric('Số khách trong danh sách', vn(len(d))); k2.metric('Tổng chi phí', usd(tong), 'vượt ngân sách' if tong > B else 'trong ngân sách', delta_color='inverse' if tong > B else 'normal'); k3.metric('Giá trị ròng Z sau điều chỉnh', usd(Z))
    if nhat_ky:
        st.markdown('**Nhật ký điều chỉnh thủ công** (đi kèm file xuất)')
        st.dataframe(pd.DataFrame(nhat_ky).rename(columns={'thao_tac': 'Thao tác', 'ma_khach': 'Mã khách', 'ly_do': 'Lý do'}), hide_index=True, use_container_width=True)
    d['GiaiThichDeDoc'] = [f'Kênh {k_} ({CHAN[k_][0].lower()}) vì khách thuộc {n_}, rủi ro {lv_.lower()}. Giá trị kỳ vọng {vn(e_, 1)} USD. ' + (f'Gợi ý {sp_}. ' if sp_ else '') + de_hieu(tf_)
                           for k_, n_, lv_, e_, sp_, tf_ in zip(d.KenhRule, d.Nhom, d.RiskLevel, d.EV, d.SanPhamGoiY, d.TopFactors)]
    t = d[['CustomerID', 'NguonChon', 'Nhom', 'ABC', 'RiskScore', 'RiskLevel', 'v', 'EV', 'KenhRule', 'SanPhamGoiY', 'GiaiThichDeDoc']].head(500).copy(); t['KenhRule'] = t.KenhRule.map(lambda k: f'{k} – {CHAN[k][0]}')
    t.columns = ['Mã khách', 'Nguồn chọn', 'Nhóm', 'Hạng', 'Xác suất không mua lại', 'Mức rủi ro', 'Giá trị một lần mua (USD)', 'Giá trị kỳ vọng (USD)', 'Hình thức liên hệ', 'Sản phẩm gợi ý', 'Giải thích']
    st.dataframe(t.style.format({'Xác suất không mua lại': fmt(3), 'Giá trị một lần mua (USD)': fmt(1), 'Giá trị kỳ vọng (USD)': fmt(1)}), hide_index=True, use_container_width=True, height=420)
    if len(d) > 500: st.caption(f'Hiển thị 500 dòng đầu trong {vn(len(d))} khách. Xuất CSV để lấy đủ.')
    if vai_tro == 'Nhân viên phân tích dữ liệu': st.caption('Vai trò phân tích chỉ xem, không duyệt và không xuất danh sách (Bảng 3.31).')
    else:
        xuat = d[['CustomerID', 'NguonChon', 'LyDo', 'Nhom', 'ABC', 'RiskScore', 'RiskLevel', 'v', 'EV', 'KenhRule', 'SanPhamGoiY', 'QuyTacSP', 'GiaiThich']].rename(columns={'LyDo': 'LyDoDieuChinh'})
        bot_ra = [x_['ma_khach'] for x_ in nhat_ky if x_['thao_tac'] == 'Bớt']
        if bot_ra: xuat = pd.concat([xuat, pd.DataFrame({'CustomerID': bot_ra, 'NguonChon': 'Bớt thủ công (không chăm sóc)', 'LyDoDieuChinh': ly_do})])
        st.download_button('Xuất danh sách đã duyệt (CSV)', xuat.to_csv(index=False).encode('utf-8-sig'), file_name=f'danh_sach_cham_soc_{C.SCORING_DATE}.csv', disabled=thieu_ly_do)

# ================= 5. THEO DÕI =================
else:
    st.title('5. Theo dõi mô hình và quy tắc'); tags('du_lieu', 'du_doan')
    ghi_chu('Mô hình còn tốt hơn quy tắc đơn giản "khách lâu không mua thì rủi ro cao" hay không. Nếu không còn hơn, cần huấn luyện lại hoặc xem lại thiết kế (quy tắc R9).')
    t = folds[folds.mo_hinh.isin(['Naive Bayes rời rạc', 'Recency đảo chiều', 'MLP (32,16)'])][['E', 'mo_hinh', 'AUC']].copy(); t['mo_hinh'] = t.mo_hinh.map({'Naive Bayes rời rạc': 'Naive Bayes (đang dùng)', 'Recency đảo chiều': 'Recency (quy tắc đơn giản)', 'MLP (32,16)': 'MLP (so sánh)'})
    t['E'] = pd.to_datetime(t.E).dt.strftime('%d/%m/%Y'); t['AUC_vn'] = t.AUC.map(lambda x: vn(x, 3))
    st.subheader('Khả năng xếp hạng (ROC-AUC) ở bốn mốc đã đủ nhãn')
    st.altair_chart(alt.Chart(t).mark_line(point=True).encode(x=alt.X('E:N', title='Mốc đánh giá', sort=None, axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('AUC:Q', scale=alt.Scale(domain=[0.6, 0.8]), title='ROC-AUC', axis=alt.Axis(labelExpr="replace(format(datum.value, '.2f'), '.', ',')")),
                    color=alt.Color('mo_hinh:N', title='', scale=alt.Scale(domain=['Naive Bayes (đang dùng)', 'Recency (quy tắc đơn giản)', 'MLP (so sánh)'], range=[NAVY, '#8A94A6', '#C57B2A']), legend=alt.Legend(orient='bottom', labelLimit=300)), tooltip=[alt.Tooltip('E', title='Mốc'), alt.Tooltip('mo_hinh', title='Mô hình'), alt.Tooltip('AUC_vn', title='ROC-AUC')]).properties(height=300), use_container_width=True)
    st.caption('0,5 là đoán ngẫu nhiên, 1,0 là hoàn hảo. Mô hình đang dùng bằng hoặc hơn quy tắc đơn giản ở cả bốn mốc và cho xác suất chính xác hơn (Brier 0,125 so với 0,269).')
    st.subheader('Cơ cấu khách thay đổi theo thời gian (vì sao phải huấn luyện lại mỗi kỳ)')
    m = moc.rename(columns={'T': 'Mốc', 'so_khach': 'Số khách', 'ty_le_y1': 'Tỷ lệ không mua lại', 'mot_don': 'Tỷ lệ khách mới mua 1 đơn', 'bike': 'Tỷ lệ mua xe đạp', 'nsub2': 'Tỷ lệ mua từ 2 danh mục'})[['Mốc', 'Số khách', 'Tỷ lệ không mua lại', 'Tỷ lệ khách mới mua 1 đơn', 'Tỷ lệ mua xe đạp', 'Tỷ lệ mua từ 2 danh mục']]
    st.dataframe(m.style.format({'Số khách': fmt(), 'Tỷ lệ không mua lại': fpct(), 'Tỷ lệ khách mới mua 1 đơn': fpct(), 'Tỷ lệ mua xe đạp': fpct(), 'Tỷ lệ mua từ 2 danh mục': fpct()}), hide_index=True, use_container_width=True, height=300)
    st.caption('Mốc 08/07/2014 là mốc chấm điểm nên chưa có tỷ lệ không mua lại (dấu —).')
    st.subheader('Phiên bản mô hình và quy tắc đang dùng')
    km = json.load(open(f'{ROOT}/models/kmeans_E{C.SCORING_DATE.replace("-", "")}.json'))
    st.dataframe(pd.DataFrame([{'Thành phần': 'Mô hình chấm điểm', 'Phiên bản': f'NB_T{C.SCORING_TRAIN_DATE.replace("-", "")}_v1', 'Học ở mốc': '01/03/2014', 'Ghi chú': 'Naive Bayes, 5 thuộc tính rời rạc'}, {'Thành phần': 'Cây đối chứng', 'Phiên bản': f'TREE_T{C.SCORING_TRAIN_DATE.replace("-", "")}_v1', 'Học ở mốc': '01/03/2014', 'Ghi chú': '11 lá, cho TopFactors'}, {'Thành phần': 'Phân nhóm', 'Phiên bản': f'KMEANS_E{C.SCORING_DATE.replace("-", "")}_v1', 'Học ở mốc': '08/07/2014', 'Ghi chú': f'k = 5, silhouette {km["silhouette"]:.3f}'.replace('.', ',')}, {'Thành phần': 'Kho quy tắc', 'Phiên bản': 'R1–R9 bản 1', 'Học ở mốc': '—', 'Ghi chú': 'R1, R9 tạm tắt vì chưa có dữ liệu CRM'}]), hide_index=True, use_container_width=True)
    if vai_tro != 'Nhân viên chăm sóc khách hàng':
        st.subheader('Đề xuất quy tắc mới (trạng thái chờ duyệt)')
        c1, c2 = st.columns(2); dk = c1.text_input('Điều kiện (IF)', placeholder='ví dụ: Nhóm N2 và đã mua Road Bikes'); kn_ = c2.text_input('Khuyến nghị (THEN)', placeholder='ví dụ: Gợi ý Helmets')
        if st.button('Gửi duyệt'):
            if dk.strip() and kn_.strip(): st.markdown(f'<div class="on">Đã ghi nhận đề xuất "NẾU {dk.strip()} THÌ {kn_.strip()}" ở trạng thái chờ duyệt. Bản trình diễn chưa lưu đề xuất vào kho, quản lý duyệt rồi nhân viên phân tích thêm vào analytics.CareRule.</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="canh-bao">Cần nhập cả điều kiện và khuyến nghị.</div>', unsafe_allow_html=True)
    st.caption('Nhóm đối chứng và quy tắc R1, R9 cần dữ liệu chiến dịch từ CRM, chưa có trong phạm vi đề tài (mục 3.5.6).')
