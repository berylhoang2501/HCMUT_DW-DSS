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

# ---------------- giao diện (chỉ thay lớp trình bày, giữ nguyên dữ liệu và logic DSS) ----------------
NAVY, GREY, RED, GREEN, LIGHT = '#1F416B', '#66758C', '#AE352E', '#157052', '#F5F7FB'
st.markdown(f"""
<style>
:root {{
 --cx-navy:#203D64; --cx-hover:#2E5B8C; --cx-coral:#FF6B3D;
 --cx-bg:#F7F8FB; --cx-white:#FFFFFF; --cx-ink:#182538;
 --cx-muted:#66758A; --cx-border:#E6EAF0; --cx-green:#16835D;
}}
/* Header fix: no translucent or sticky layer over the app's own content.
   Role context is rendered as an in-flow toolbar, not a fixed overlay. */
[data-testid="stHeader"] {{ position:relative !important; inset:auto !important;
    background:#F7F8FB !important; backdrop-filter:none !important;
    -webkit-backdrop-filter:none !important; box-shadow:none !important;
    opacity:1 !important; z-index:2 !important; min-height:2.55rem; }}
[data-testid="stAppViewContainer"] {{ background:var(--cx-bg) !important; }}
html,body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; color:var(--cx-ink); }}
.block-container {{ padding:1.05rem 1.75rem 7rem !important; max-width:1490px !important; }}
.block-container h1 {{ font-size:clamp(1.6rem,2.15vw,2.05rem) !important; font-weight:770 !important;
 letter-spacing:-.035em; color:var(--cx-ink) !important; margin:.1rem 0 .38rem !important; }}
.block-container h2 {{ font-size:1.17rem !important; font-weight:740 !important; letter-spacing:-.01em; color:var(--cx-ink) !important; margin-top:.7rem !important; }}
.block-container h3 {{ font-size:1.04rem !important; color:var(--cx-ink) !important; font-weight:700 !important; }}
.block-container p, .block-container li {{ font-size:.91rem; line-height:1.55; }}
/* App navigation */
[data-testid="stSidebar"] {{ background:#FFFFFF !important; border-right:1px solid var(--cx-border) !important; }}
[data-testid="stSidebar"] > div:first-child {{ padding-top:.35rem; }}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap:.48rem; }}
[data-testid="stSidebar"] [role="radiogroup"] {{ gap:.25rem; }}
[data-testid="stSidebar"] [role="radiogroup"] label {{
 padding:.57rem .68rem; min-height:43px; border:1px solid transparent;
 border-radius:11px; transition:background .13s ease,border-color .13s ease; }}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {{ background:#F4F7FC; }}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
 background:#ECF3FA; border:1px solid #D9E6F5; box-shadow:inset 3px 0 var(--cx-coral); }}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {{ color:var(--cx-navy); font-weight:700; }}
[data-testid="stSidebar"] [role="radiogroup"] label p {{ font-size:.86rem !important; line-height:1.35 !important; }}
[data-testid="stSidebar"] label p, [data-testid="stSidebar"] [data-baseweb="select"] span {{
 white-space:normal !important; overflow:visible !important; text-overflow:clip !important; line-height:1.35; }}
[data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"] {{ height:auto !important; min-height:48px !important; }}
[data-testid="stSidebar"] button {{ white-space:normal; line-height:1.3; }}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ overflow-y:auto; }}
.brand {{ display:flex; align-items:center; gap:.7rem; padding:.72rem .24rem .9rem; border-bottom:1px solid var(--cx-border); margin-bottom:.72rem; }}
.brand-mark {{ flex:none; display:flex; align-items:center; justify-content:center; width:39px; height:39px;
 border-radius:12px; color:#fff; background:linear-gradient(145deg,#203D64,#456C91); font-size:1.19rem; font-weight:800;
 box-shadow:0 6px 12px rgba(32,61,100,.12); }}
.brand-main {{ font-size:.99rem; font-weight:820; color:var(--cx-navy); letter-spacing:.015em; line-height:1.23; }}
.brand-sub {{ font-size:.71rem; color:var(--cx-muted); line-height:1.4; margin-top:.17rem; }}
/* The role bar is a normal in-flow element; unlike the Streamlit header, it never sticks on scroll. */
.cx-topbar {{ display:flex; gap:.8rem; align-items:center; justify-content:space-between;
 background:#FFFFFF; border:1px solid var(--cx-border); border-radius:13px;
 padding:.65rem 1.03rem; box-shadow:0 1px 4px rgba(23,38,62,.025);
 margin:0 0 1.25rem; position:static !important; z-index:auto !important; }}
.cx-topbar-title {{ font-size:.81rem; font-weight:760; color:var(--cx-navy); letter-spacing:.015em; }}
.cx-topbar-sub {{ font-size:.76rem; color:var(--cx-muted); margin-top:.15rem; line-height:1.4; }}
.cx-topbar-right {{ display:flex; flex-wrap:wrap; gap:.5rem; justify-content:flex-end; align-items:center; }}
.cx-pill {{ display:inline-flex; padding:.33rem .66rem; background:#F0F5FB; border:1px solid #E1EAF5;
 border-radius:999px; font-size:.73rem; font-weight:650; color:var(--cx-navy); max-width:100%; }}
.cx-pill-date {{ background:#FFF6EF; border-color:#F8E9DE; color:#8C472B; }}
/* KPI cards: allow multi-line labels and values without clipping at the bottom. */
[data-testid="stMetric"] {{ position:relative; border:1px solid var(--cx-border) !important;
 background:#fff !important; border-radius:14px !important; padding:.92rem 1.01rem !important;
 min-height:112px; height:auto !important; box-sizing:border-box !important;
 box-shadow:0 3px 13px rgba(22,41,70,.045); overflow:visible !important; }}
[data-testid="stMetric"]::before {{ position:absolute; top:0; left:0; right:0; height:3px;
 content:""; background:#D8E4EF; }}
[data-testid="stMetricLabel"] {{ font-size:.79rem !important; color:var(--cx-muted) !important;
 font-weight:650 !important; line-height:1.32 !important; min-height:1.2em; }}
[data-testid="stMetricLabel"] p {{ white-space:normal !important; text-overflow:clip !important; overflow:visible !important; }}
[data-testid="stMetricValue"] {{ font-size:clamp(1.22rem,1.85vw,1.75rem) !important;
 color:var(--cx-ink); font-weight:780; letter-spacing:-.025em; white-space:normal !important;
 overflow-wrap:break-word; }}
/* CX_UI_TEXT_VISIBILITY_FIX_V1: readable notes, no cropping in result blocks. */
.block-container [data-testid="stCaptionContainer"],
.block-container [data-testid="stCaptionContainer"] p {{
 color:#4B5B70 !important; opacity:1 !important;
 line-height:1.6 !important; height:auto !important; max-height:none !important;
 overflow:visible !important; white-space:normal !important;
}}
.block-container [data-testid="stMarkdownContainer"] {{ overflow:visible !important; }}
.cx-action-decision, .cx-action-item, .ghi-chu, .insight, .canh-bao, .on, .data-note {{
 height:auto !important; max-height:none !important;
 overflow:visible !important; white-space:normal !important;
 line-height:1.6 !important; opacity:1 !important;
}}
.cx-action-decision {{ display:block; min-height:2.8rem; box-sizing:border-box;
 color:#6C371D; font-weight:650; margin-bottom:1rem; }}
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
 height:auto !important; max-height:none !important; overflow:visible !important;
}}
/* True native Streamlit containers, used as chart/table panels (not broken HTML wrappers) */
[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius:15px !important; border-color:var(--cx-border) !important;
 background:#fff !important; box-shadow:0 4px 16px rgba(24,45,71,.045) !important; }}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {{ gap:.62rem; }}
[data-testid="stDataFrame"] {{ border-radius:11px !important; border:1px solid var(--cx-border) !important; overflow:hidden; }}
[data-testid="stExpander"] {{ border-radius:13px !important; border-color:var(--cx-border) !important; background:#fff; }}
/* Inputs have the same radius as actionable cards. */
.stButton > button, .stDownloadButton > button, [data-baseweb="select"] > div,
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {{ border-radius:10px !important; }}
.stButton > button:hover, .stDownloadButton > button:hover {{ border-color:var(--cx-hover) !important; }}
.stButton > button[kind="primary"], .stDownloadButton > button {{ background:var(--cx-navy); color:#fff; border-color:var(--cx-navy); }}
[data-testid="stAlert"] {{ border-radius:11px !important; }}
/* Hierarchy: no report-like section numerals or lengthy divider lines. */
.section-caption {{ color:var(--cx-ink); font-weight:770; font-size:1.11rem; letter-spacing:-.015em;
 margin:1.2rem 0 .5rem; line-height:1.34; }}
.eyebrow {{ color:var(--cx-coral); text-transform:uppercase; font-weight:780; font-size:.7rem;
 letter-spacing:.12em; margin:0 0 .18rem; }}
.section-hint, .data-note {{ color:var(--cx-muted); font-size:.83rem; line-height:1.53; margin:.07rem 0 .58rem; }}
.ghi-chu {{ background:#FFF; border:1px solid var(--cx-border); border-left:3px solid var(--cx-navy);
 border-radius:0 11px 11px 0; padding:.66rem .88rem; margin:.5rem 0 .92rem;
 color:#3A4B61; font-size:.88rem; line-height:1.58; }}
.insight {{ background:#F1F6FC; border:1px solid #DFEAF6; border-left:3px solid #5C8AB6;
 border-radius:0 11px 11px 0; padding:.68rem .84rem; color:#304763; margin:.55rem 0 .95rem;
 font-size:.89rem; line-height:1.53; }}
.insight b {{ color:var(--cx-navy); }}
.canh-bao {{ background:#FFF6F5; border:1px solid #EBCBC8; border-left:3px solid #D94C54;
 border-radius:0 11px 11px 0; padding:.74rem .87rem; margin:.48rem 0; }}
.on {{ background:#F2FAF7; border:1px solid #C5E2D5; border-left:3px solid #16835D;
 border-radius:0 11px 11px 0; padding:.74rem .87rem; margin:.48rem 0; }}
.tag {{ display:inline-block; font-size:.7rem; font-weight:760; padding:.23rem .57rem;
 margin-right:.3rem; margin-bottom:.28rem; border-radius:100px; border:1px solid; }}
.tag-du-lieu {{ color:#235579; border-color:#D4E4F1; background:#F3F9FD; }}
.tag-du-doan {{ color:#945423; border-color:#F3DFCF; background:#FFF8F1; }}
.tag-gia-dinh {{ color:#634C87; border-color:#DFD6ED; background:#FAF6FF; }}
/* Customer 360's read-only field grid */
.cx-field-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.62rem; margin:.45rem 0 1rem; }}
.cx-field {{ padding:.7rem .79rem; border:1px solid var(--cx-border); border-radius:12px; background:#fff; }}
.cx-field-label {{ color:var(--cx-muted); font-size:.73rem; line-height:1.35; margin-bottom:.3rem; }}
.cx-field-value {{ color:var(--cx-ink); font-size:.91rem; line-height:1.46; font-weight:700; overflow-wrap:anywhere; }}
.cx-action-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.66rem; margin:.6rem 0; }}
.cx-action-item {{ background:#F8FAFD; border:1px solid var(--cx-border); border-radius:11px; padding:.68rem .8rem; }}
.cx-action-item b {{ display:block; margin-top:.22rem; font-size:.95rem; color:var(--cx-ink); }}
.cx-action-label {{ color:var(--cx-muted); font-size:.75rem; }}
.cx-action-decision {{ border-left:3px solid var(--cx-coral); padding:.6rem .8rem; margin:.55rem 0; background:#FFF7F0; border-radius:0 9px 9px 0; }}
.cx-hero {{ background:linear-gradient(115deg,#203D64,#2D5981); padding:1.1rem 1.3rem;
 color:#fff; border-radius:15px; margin:.35rem 0 1rem; }}
.cx-hero-kicker {{ font-size:.69rem; font-weight:750; letter-spacing:.14em; color:#CFE1F5; margin-bottom:.28rem; }}
.cx-hero-title {{ font-size:1.32rem; font-weight:760; letter-spacing:-.01em; margin-bottom:.2rem; }}
.cx-hero-description {{ font-size:.87rem; color:#E4EFFB; line-height:1.52; }}
@media(max-width:1280px) {{ .block-container {{ padding-left:1.05rem !important; padding-right:1.05rem !important; }}
 [data-testid="stMetric"] {{ padding:.75rem .72rem !important; }}
 [data-testid="stMetricValue"] {{ font-size:1.35rem !important; }} }}
@media(max-width:900px) {{ .cx-field-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
 .block-container {{ padding:.83rem .76rem 6rem !important; }} }}
@media(max-width:650px) {{ .cx-topbar {{ flex-direction:column; align-items:flex-start; }}
 .cx-topbar-right {{ justify-content:flex-start; }}
 .cx-action-grid,.cx-field-grid {{ grid-template-columns:1fr; }}
 [data-testid="stMetric"] {{ min-height:100px; height:auto !important; }} }}
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

# Chỉ UI: các lời dẫn dưới đây không phát sinh dữ liệu và không thay đổi công thức.
# Tương thích Streamlit: altair_chart ở các bản cũ chưa nhận tham số width.
# Chỉ xử lý cách hiển thị, không can thiệp dữ liệu hay phép tính.
def altair_wide(chart):
    import inspect
    if "width" in inspect.signature(st.altair_chart).parameters:
        return st.altair_chart(chart, width="stretch")
    return st.altair_chart(chart, use_container_width=True)

def eyebrow(label):
    st.markdown(f'<div class="eyebrow">{label}</div>', unsafe_allow_html=True)

def insight(title, message):
    st.markdown(f'<div class="insight"><b>{title}</b> · {message}</div>', unsafe_allow_html=True)

def section_caption(label):
    """Present an existing heading as a concise app section, without numbering."""
    display_label = label.split(' · ', 1)[-1]
    st.markdown(f'<div class="section-caption">{display_label}</div>', unsafe_allow_html=True)

def data_note(message):
    st.markdown(f'<div class="data-note">{message}</div>', unsafe_allow_html=True)

def nav_to(target):
    # on_click được thực thi trước khi radio widget khởi tạo lại.
    st.session_state['companyx_nav'] = target


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
def hist_chart(series, title, color='#FF6B3D', x_title='RiskScore'):
    h = pd.DataFrame({'khoang': [f'{i / 20:.2f}–{(i + 1) / 20:.2f}' for i in range(20)], 'so_khach': np.histogram(series, bins=20, range=(0, 1))[0]})
    h['khoang'] = h.khoang.str.replace('.', ',', regex=False)
    return alt.Chart(h).mark_bar(color=color).encode(x=alt.X('khoang:N', title=x_title, sort=None, axis=alt.Axis(labelAngle=-45)), y=alt.Y('so_khach:Q', title='Số khách', axis=alt.Axis(labelExpr="replace(format(datum.value, ',.0f'), ',', '.')")),
                                                     tooltip=[alt.Tooltip('khoang', title='Khoảng'), alt.Tooltip('so_khach', title='Số khách')]).properties(height=260, title=title)


# -------- VISUAL-ONLY: charts generated from existing, already computed data --------
def chart_high_risk_by_group(grouped):
    """Existing metric 'ty_le_rui_ro_cao' from the overview table; no new risk definition."""
    source = grouped.reset_index()[['Nhom', 'so_khach', 'ty_le_rui_ro_cao']].copy()
    source['NhomDayDu'] = source['Nhom'].map(TEN)
    return alt.Chart(source).mark_bar(color='#FF6B3D', cornerRadiusEnd=5, size=23).encode(
        y=alt.Y('NhomDayDu:N', title=None, sort=None, axis=alt.Axis(labelLimit=280)),
        x=alt.X('ty_le_rui_ro_cao:Q', title='Tỷ lệ khách rủi ro Cao trong từng nhóm',
                axis=alt.Axis(format='.0%'), scale=alt.Scale(domain=[0, 1])),
        tooltip=[alt.Tooltip('NhomDayDu:N', title='Nhóm'),
                 alt.Tooltip('so_khach:Q', title='Số khách trong nhóm', format=',.0f'),
                 alt.Tooltip('ty_le_rui_ro_cao:Q', title='Tỷ lệ rủi ro Cao', format='.1%')]
    ).properties(height=230)


def chart_customer_scores(customer):
    """Plot actual two scores; TreeScore is the independent CART reference, not NB attribution."""
    source = pd.DataFrame({
        'Mô hình': ['Naive Bayes · RiskScore', 'Decision Tree · TreeScore'],
        'Giá trị': [float(customer.RiskScore), float(customer.TreeScore)],
    })
    return alt.Chart(source).mark_bar(cornerRadiusEnd=5, size=27).encode(
        y=alt.Y('Mô hình:N', title=None, sort=None, axis=alt.Axis(labelLimit=265)),
        x=alt.X('Giá trị:Q', title='Điểm (0–1)', scale=alt.Scale(domain=[0, 1]),
                axis=alt.Axis(format='.0%')),
        color=alt.Color('Mô hình:N', legend=None,
                        scale=alt.Scale(domain=source['Mô hình'].tolist(), range=['#203D64', '#FF6B3D'])),
        tooltip=[alt.Tooltip('Mô hình:N'), alt.Tooltip('Giá trị:Q', format='.3f')]
    ).properties(height=116)


def chart_what_if_z(what_if):
    """Visualize existing what-if Z columns; no recalculation."""
    source = what_if[['Kịch bản', 'Z (USD)']].copy()
    source['Loại'] = np.where(source['Kịch bản'].eq('Cơ sở'), 'Cơ sở', 'Kịch bản khác')
    return alt.Chart(source).mark_bar(cornerRadiusEnd=4, size=23).encode(
        y=alt.Y('Kịch bản:N', title=None, sort=source['Kịch bản'].tolist(),
                axis=alt.Axis(labelLimit=220)),
        x=alt.X('Z (USD):Q', title='Giá trị ròng kỳ vọng Z (USD)', axis=alt.Axis(format=',.0f')),
        color=alt.Color('Loại:N', legend=None,
                        scale=alt.Scale(domain=['Cơ sở', 'Kịch bản khác'], range=['#FF6B3D', '#203D64'])),
        tooltip=[alt.Tooltip('Kịch bản:N'), alt.Tooltip('Z (USD):Q', title='Z (USD)', format=',.0f')]
    ).properties(height=max(230, 33 * len(source)))


def chart_payoff_by_budget(payoff):
    """Plot only the three r values provided in bang_4_4_payoff.csv."""
    source = payoff[['Ngân sách B (USD)', 'Z nếu r = 2% (bi quan)',
                     'Z nếu r = 10% (cơ sở)', 'Z nếu r = 20% (lạc quan)']].melt(
        id_vars='Ngân sách B (USD)', var_name='Giả định thành công', value_name='Z (USD)')
    return alt.Chart(source).mark_line(point=alt.OverlayMarkDef(size=65), strokeWidth=2.6).encode(
        x=alt.X('Ngân sách B (USD):Q', title='Ngân sách B (USD)', axis=alt.Axis(format=',.0f')),
        y=alt.Y('Z (USD):Q', title='Giá trị ròng kỳ vọng Z (USD)', axis=alt.Axis(format=',.0f')),
        color=alt.Color('Giả định thành công:N', title=None,
                        scale=alt.Scale(domain=['Z nếu r = 2% (bi quan)', 'Z nếu r = 10% (cơ sở)',
                                                'Z nếu r = 20% (lạc quan)'],
                                        range=['#D94C54', '#203D64', '#16835D']),
                        legend=alt.Legend(orient='bottom', labelLimit=255)),
        tooltip=[alt.Tooltip('Ngân sách B (USD):Q', title='B (USD)', format=',.0f'),
                 alt.Tooltip('Giả định thành công:N'), alt.Tooltip('Z (USD):Q', title='Z (USD)', format=',.0f')]
    ).properties(height=255)


def chart_care_channels(selected):
    """Distribution of the actual selected list after user's manual add/remove."""
    source = selected['KenhRule'].value_counts().reindex(list(CHAN), fill_value=0).reset_index()
    source.columns = ['Quy tắc', 'Số khách']
    source['Hình thức'] = source['Quy tắc'].map(lambda code: code + ' · ' + CHAN[code][0])
    source = source[source['Số khách'] > 0].copy()  # ẩn kênh không có khách trong danh sách hiện tại
    return alt.Chart(source).mark_bar(cornerRadiusEnd=4, size=28).encode(
        y=alt.Y('Hình thức:N', title=None, sort=None, axis=alt.Axis(labelLimit=260)),
        x=alt.X('Số khách:Q', title='Số khách trong danh sách', axis=alt.Axis(format=',.0f')),
        color=alt.Color('Quy tắc:N', legend=None,
                        scale=alt.Scale(domain=['R3', 'R4', 'R5'], range=['#FF6B3D', '#2E5B8C', '#16835D'])),
        tooltip=[alt.Tooltip('Hình thức:N'), alt.Tooltip('Số khách:Q', format=',.0f')]
    ).properties(height=160)


def chart_matured_snapshot_trends(snapshots):
    """Use only historical snapshots with an available 90-day label. 08/07/2014 is excluded."""
    source = snapshots.loc[snapshots['ty_le_y1'].notna(), ['T', 'ty_le_y1', 'mot_don']].copy()
    source['Ngày'] = pd.to_datetime(source['T'], format='%d/%m/%Y')
    source = source.rename(columns={
        'ty_le_y1': 'Tỷ lệ không mua lại trong 90 ngày',
        'mot_don': 'Tỷ lệ khách mới mua một đơn',
    }).melt(id_vars='Ngày', value_vars=['Tỷ lệ không mua lại trong 90 ngày',
                                        'Tỷ lệ khách mới mua một đơn'],
            var_name='Chỉ số', value_name='Tỷ lệ')
    return alt.Chart(source).mark_line(point=True, strokeWidth=2.3).encode(
        x=alt.X('Ngày:T', title='Mốc Snapshot', axis=alt.Axis(format='%m/%Y')),
        y=alt.Y('Tỷ lệ:Q', title='Tỷ lệ', axis=alt.Axis(format='.0%'),
                scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('Chỉ số:N', title=None,
                        scale=alt.Scale(domain=['Tỷ lệ không mua lại trong 90 ngày',
                                                'Tỷ lệ khách mới mua một đơn'],
                                        range=['#203D64', '#FF6B3D']),
                        legend=alt.Legend(orient='bottom', labelLimit=310)),
        tooltip=[alt.Tooltip('Ngày:T', title='Mốc', format='%d/%m/%Y'),
                 alt.Tooltip('Chỉ số:N'), alt.Tooltip('Tỷ lệ:Q', format='.1%')]
    ).properties(height=260)

# ---------------- thanh bên: điểm bắt đầu theo vai trò, 5 màn hình cũ giữ nguyên ----------------
PAGES = ['Hướng dẫn sử dụng', '1. Tổng quan rủi ro', '2. Hồ sơ khách hàng', '3. Phân tích kịch bản', '4. Danh sách chăm sóc', '5. Theo dõi mô hình và quy tắc']
ROLES = ['Quản lý Marketing/Sales', 'Nhân viên phân tích dữ liệu', 'Nhân viên chăm sóc khách hàng']
ROLE_START = {ROLES[0]: PAGES[1], ROLES[1]: PAGES[5], ROLES[2]: PAGES[4]}
ROLE_DESC = {
    ROLES[0]: ('Ra quyết định ngân sách', 'Nhìn rủi ro × giá trị, thử kịch bản và duyệt danh sách ưu tiên.'),
    ROLES[1]: ('Kiểm định & giám sát', 'Đối chiếu mô hình, kiểm tra cờ chênh lệch và đề xuất điều chỉnh quy tắc.'),
    ROLES[2]: ('Thực hiện chăm sóc', 'Tra cứu hồ sơ, xem kênh liên hệ và sản phẩm được gợi ý.'),
}

def role_changed():
    st.session_state['companyx_nav'] = ROLE_START[st.session_state['companyx_role']]

st.session_state.setdefault('companyx_nav', PAGES[1])
st.sidebar.markdown('<div class="brand"><span class="brand-mark">C</span><div><div class="brand-main">COMPANYX / DSS</div><div class="brand-sub">Customer Retention Decision Support<br>Phân tích · Ưu tiên · Hành động</div></div></div>', unsafe_allow_html=True)
vai_tro = st.sidebar.selectbox('Góc nhìn của bạn', ROLES, key='companyx_role', on_change=role_changed)
st.sidebar.caption(ROLE_DESC[vai_tro][0] + ' · ' + ROLE_DESC[vai_tro][1])
st.sidebar.markdown('---')
man = st.sidebar.radio('Điều hướng màn hình', PAGES, key='companyx_nav', format_func=lambda text: text.replace('. ', '.\u00a0', 1) if text[0].isdigit() else text)
st.sidebar.button('Đến màn hình ưu tiên', on_click=lambda: st.session_state.update({'companyx_nav': ROLE_START[vai_tro]}), width='stretch', help='Mở mục phù hợp với vai trò')
st.sidebar.markdown('---')
st.sidebar.caption(f'Mốc chấm điểm: {pd.Timestamp(C.SCORING_DATE):%d/%m/%Y}  ·  Mô hình: Naive Bayes')
st.sidebar.markdown('<span style="font-size:.76rem;color:#63748A">Vai trò chỉ mô phỏng góc nhìn và quyền thao tác trên giao diện; chưa phải đăng nhập xác thực.</span>', unsafe_allow_html=True)
with st.sidebar.expander('Cách đọc số liệu', expanded=False):
    st.markdown(tag('du_lieu') + '<div style="font-size:.85rem;margin-bottom:.55rem">Chỉ số tổng hợp từ dữ liệu hiện có</div>' + tag('du_doan') + '<div style="font-size:.85rem;margin-bottom:.55rem">Xác suất do mô hình dự đoán</div>' + tag('gia_dinh') + '<div style="font-size:.85rem">Giá trị tùy vào giả định r, c, B</div>', unsafe_allow_html=True)

st.markdown(f'<div class="cx-topbar"><div><div class="cx-topbar-title">{ROLE_DESC[vai_tro][0]}</div><div class="cx-topbar-sub">{ROLE_DESC[vai_tro][1]}</div></div><div class="cx-topbar-right"><span class="cx-pill">{vai_tro}</span><span class="cx-pill cx-pill-date">Mốc: {pd.Timestamp(C.SCORING_DATE):%d/%m/%Y}</span></div></div>', unsafe_allow_html=True)

# ================= 0. HƯỚNG DẪN SỬ DỤNG =================
if man.startswith('Hướng dẫn'):
    eyebrow('BẮT ĐẦU · WORKSPACE');
    st.title('Hướng dẫn sử dụng DSS CompanyX'); tags('du_lieu', 'du_doan', 'gia_dinh')
    ghi_chu('Hệ thống giúp trả lời một câu hỏi: <b>với ngân sách có hạn, nên chăm sóc những khách nào để giữ được nhiều giá trị nhất?</b> Bạn không cần biết mô hình bên trong. Làm theo 5 bước dưới đây, mỗi bước là một màn hình ở thanh bên trái, mất khoảng 10 phút.')
    st.markdown('<div class="cx-hero"><div class="cx-hero-kicker">COMPANYX · DECISION WORKSPACE</div><div class="cx-hero-title">Dữ liệu thành quyết định chăm sóc</div><div class="cx-hero-description">Khám phá rủi ro, so sánh kịch bản và hành động dựa trên dữ liệu CompanyX hiện có.</div></div>', unsafe_allow_html=True)
    insight('Gợi ý dành cho vai trò này', ROLE_DESC[vai_tro][1])
    a, b, c = st.columns(3)
    with a:
        st.button('Tổng quan rủi ro', width='stretch', on_click=nav_to, args=(PAGES[1],))
    with b:
        st.button('Hồ sơ khách hàng', width='stretch', on_click=nav_to, args=(PAGES[2],))
    with c:
        st.button('Danh sách chăm sóc', width='stretch', on_click=nav_to, args=(PAGES[4],))

    section_caption('Khái niệm cần biết')
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
    section_caption('Hỗ trợ')
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
    eyebrow('01 / TỔNG QUAN');
    st.title('1. Tổng quan rủi ro khách hàng'); tags('du_lieu', 'du_doan')
    ghi_chu('Màn hình này trả lời: <b>hiện có bao nhiêu khách có nguy cơ không mua lại trong 90 ngày tới, họ thuộc nhóm nào và đáng giá bao nhiêu.</b> Rủi ro Cao = 25% khách có xác suất không mua lại cao nhất trong cùng hạng giá trị (A, B, C).')
    section_caption('01 · Phạm vi phân tích')
    data_note('Chọn các nhóm N1–N5 và hạng ABC để lọc toàn bộ KPI, biểu đồ và danh sách bên dưới.')
    with st.container(border=True):
        nhom = st.pills('Lọc theo nhóm khách (bấm để bật hoặc tắt)', list(TEN), selection_mode='multi', default=list(TEN), format_func=lambda x: TEN[x])
        abc = st.pills('Lọc theo hạng giá trị (ABC)', ['A', 'B', 'C'], selection_mode='multi', default=['A', 'B', 'C'], format_func=lambda x: {'A': 'A – 28% khách giữ 80% doanh thu', 'B': 'B – 14% khách giữ 15% doanh thu', 'C': 'C – 58% khách giữ 5% doanh thu'}[x])
    if not nhom or not abc: st.markdown('<div class="canh-bao">Chưa chọn nhóm hoặc hạng nào. Bấm vào ít nhất một nhóm và một hạng ở trên.</div>', unsafe_allow_html=True); st.stop()
    d = df[df.Nhom.isin(nhom) & df.ABC.isin(abc)]
    section_caption('02 · Chỉ số tổng quan')
    k1, k2, k3, k4 = st.columns(4)
    k1.metric('Số khách đang xem', vn(len(d))); k2.metric('Khách rủi ro Cao', f'{vn((d.RiskLevel == "Cao").sum())}  ({pct((d.RiskLevel == "Cao").mean())})')
    k3.metric('Đã mua (khách Cao)', usd(d.loc[d.RiskLevel == 'Cao', 'Monetary'].sum()), help='Tổng tiền các khách rủi ro Cao đã mua từ trước đến mốc chấm điểm')
    k4.metric('Cần xem xét thêm', vn(int(d.Flag.sum())), help='Số khách mà cây đối chứng và mô hình chấm điểm lệch nhau quá 0,3')
    if vai_tro == ROLES[0]:
        so_a_cao = int(((d.ABC == 'A') & (d.RiskLevel == 'Cao')).sum())
        insight('Góc nhìn quản lý', f'Có <b>{vn(so_a_cao)} khách hạng A rủi ro Cao</b> trong bộ lọc hiện tại. Dùng màn hình Kịch bản để đối chiếu ngân sách và giá trị ròng kỳ vọng trước khi duyệt.')
    elif vai_tro == ROLES[1]:
        insight('Góc nhìn phân tích', f'Có <b>{vn(int(d.Flag.sum()))} khách</b> với chênh lệch giữa RiskScore và TreeScore vượt 0,3. Đây là cờ đối chiếu mô hình, không phải xác nhận dự đoán sai.')
    else:
        insight('Góc nhìn chăm sóc', f'Bộ lọc hiện có <b>{vn(int((d.RiskLevel == "Cao").sum()))} khách rủi ro Cao</b>. Tra cứu Hồ sơ để xem luật giải thích và kênh chăm sóc của từng khách.')

    section_caption('03 · Phân bố & phân khúc')
    a, b = st.columns([3, 2])
    with a:
        with st.container(border=True):
            st.subheader('Phân bố xác suất không mua lại'); altair_wide(hist_chart(d.RiskScore, ''))
    with b:
        with st.container(border=True):
            st.subheader('Ma trận Rủi ro × Giá trị (số khách)')
            mx = pd.crosstab(d.ABC, d.RiskLevel).reindex(index=['A', 'B', 'C'], columns=['Cao', 'Thấp']).fillna(0).astype(int); mx.index.name = 'Hạng'; st.dataframe(mx.rename(columns={'Cao': 'Rủi ro Cao', 'Thấp': 'Rủi ro Thấp'}), width="stretch")
            st.caption('Ô "A – Cao" là nơi đáng chú ý nhất: khách giá trị lớn nhưng có nguy cơ rời bỏ.')
    with st.container(border=True):
        st.subheader('Năm nhóm khách hàng')
        g = d.groupby('Nhom').agg(so_khach=('CustomerID', 'size'), recency_trung_vi=('Recency', 'median'), so_don_TB=('Frequency', 'mean'), chi_tieu_trung_vi=('Monetary', 'median'), ty_le_rui_ro_cao=('RiskLevel', lambda x: (x == 'Cao').mean()), hang_A=('ABC', lambda x: (x == 'A').sum())).reindex(list(TEN)).dropna(how='all')
        out = pd.DataFrame({'Nhóm': [TEN[i] for i in g.index], 'Số khách': [vn(v) for v in g.so_khach], 'Ngày từ lần mua gần nhất (trung vị)': [vn(v) for v in g.recency_trung_vi], 'Số đơn trung bình': [vn(v, 2) for v in g.so_don_TB], 'Chi tiêu trung vị (USD)': [vn(v) for v in g.chi_tieu_trung_vi], 'Tỷ lệ rủi ro Cao': [pct(v) for v in g.ty_le_rui_ro_cao], 'Khách hạng A': [vn(v) for v in g.hang_A]})
        altair_wide(chart_high_risk_by_group(g))
        st.caption('Tỷ lệ rủi ro Cao theo từng nhóm N1–N5 trong phạm vi bộ lọc; không phải xác suất churn trung bình.')
        st.dataframe(out, hide_index=True, width="stretch")
    section_caption('04 · Khách hàng cần xem xét')
    with st.container(border=True):
        st.subheader('Xem chi tiết: 20 khách rủi ro Cao có giá trị lớn nhất')
        t = d[d.RiskLevel == 'Cao'].nlargest(20, 'Monetary')[['CustomerID', 'Nhom', 'ABC', 'Recency', 'Frequency', 'Monetary', 'RiskScore', 'RiskPercentile']].copy()
        t.columns = ['Mã khách', 'Nhóm', 'Hạng', 'Ngày từ lần mua gần nhất', 'Số đơn', 'Tổng chi tiêu (USD)', 'Xác suất không mua lại', 'Phân vị rủi ro trong hạng']
        st.dataframe(t.style.format({'Ngày từ lần mua gần nhất': fmt(), 'Tổng chi tiêu (USD)': fmt(), 'Xác suất không mua lại': fmt(3), 'Phân vị rủi ro trong hạng': fmt(1)}), hide_index=True, width="stretch")

# ================= 2. HỒ SƠ KHÁCH =================
elif man.startswith('2'):
    eyebrow('02 / KHÁCH HÀNG');
    st.title('2. Hồ sơ một khách hàng'); tags('du_lieu', 'du_doan')
    ghi_chu('Nhập mã khách để xem lịch sử mua, xác suất không mua lại, nhóm, hạng và khuyến nghị chăm sóc kèm lý do.')
    section_caption('01 · Tra cứu')
    vi_du = [ma for ma in (12201, 26339, 26774) if ma in set(df.CustomerID)]
    st.session_state.setdefault('companyx_customer_id', int(df.CustomerID.iloc[0]))
    with st.container(border=True):
        col_example, col_id = st.columns([1, 1])
        if vi_du:
            def chon_khach_mau():
                ma = st.session_state['companyx_customer_example']
                if ma is not None:
                    st.session_state['companyx_customer_id'] = int(ma)
            with col_example:
                st.selectbox('Tra cứu nhanh khách minh họa', [None] + vi_du,
                             format_func=lambda x: 'Chọn một mã có trong kết quả thực nghiệm' if x is None else f'Khách hàng {x}',
                             key='companyx_customer_example', on_change=chon_khach_mau)
        with col_id:
            cid = st.number_input('Hoặc nhập mã khách (CustomerID)', min_value=int(df.CustomerID.min()),
                                  max_value=int(df.CustomerID.max()), step=1, key='companyx_customer_id')
    r = df[df.CustomerID == cid]
    if r.empty: st.markdown('<div class="canh-bao">Không có khách này tại mốc chấm điểm.</div>', unsafe_allow_html=True)
    else:
        r = r.iloc[0]
        section_caption('02 · Tổng quan hành vi & rủi ro')
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric('Ngày từ lần mua gần nhất', vn(r.Recency)); k2.metric('Số đơn đã mua', vn(r.Frequency)); k3.metric('Tổng chi tiêu', usd(r.Monetary)); k4.metric('Xác suất không mua lại', vn(r.RiskScore, 3))
        k5.metric('Mức rủi ro', r.RiskLevel, help='Cao khi phân vị rủi ro trong hạng giá trị từ 75 trở lên')
        st.progress(float(r.RiskScore), text=f'Xác suất không mua lại trong 90 ngày: {pct(r.RiskScore)} (dự đoán, không phải kết quả thực tế)')

        st.markdown(f"""<div class="cx-field-grid">
            <div class="cx-field"><div class="cx-field-label">Hạng giá trị</div><div class="cx-field-value">{r.ABC}</div></div>
            <div class="cx-field"><div class="cx-field-label">Phân vị rủi ro trong hạng {r.ABC}</div><div class="cx-field-value">{vn(r.RiskPercentile, 1)} · Cao khi từ 75</div></div>
            <div class="cx-field"><div class="cx-field-label">Nhóm hành vi</div><div class="cx-field-value">{TEN[r.Nhom]}</div></div>
            <div class="cx-field"><div class="cx-field-label">Thời gian là khách</div><div class="cx-field-value">{vn(r.Tenure)} ngày</div></div>
            <div class="cx-field"><div class="cx-field-label">Số danh mục đã mua</div><div class="cx-field-value">{vn(r.NSub)}</div></div>
            <div class="cx-field"><div class="cx-field-label">Tỷ trọng xe đạp</div><div class="cx-field-value">{pct(r.Share_Bikes, 0)}</div></div>
        </div>""", unsafe_allow_html=True)
        data_note('RiskScore là xác suất dự đoán; mức Cao/Thấp là vị trí tương đối theo phân vị 75 trong cùng hạng ABC.')
        section_caption('03 · Giải thích mô hình')
        with st.container(border=True):
            st.subheader('Hai điểm dự đoán để đối chiếu')
            altair_wide(chart_customer_scores(r))
            st.caption('RiskScore là điểm chấm chính (Naive Bayes); TreeScore từ cây đối chứng dùng để tham khảo. Biểu đồ không phải Feature Importance.')
        st.subheader('Khách này thuộc nhóm nào theo cây đối chứng')
        st.markdown(f'<div class="ghi-chu">{de_hieu(r.TopFactors)}<br><span style="color:{GREY};font-size:.85rem">Đây là mô tả nhóm khách có đặc điểm giống nhau, không phải lý do của xác suất ở trên.</span></div>', unsafe_allow_html=True)
        if r.Flag: st.markdown(f'<div class="canh-bao"><b>Cần xem xét thêm.</b> Cây đối chứng cho {vn(r.TreeScore, 3)} nhưng mô hình chấm điểm cho {vn(r.RiskScore, 3)}, lệch nhau quá {vn(C.TREE_FLAG_GAP, 1)}. Hai cách nhìn không thống nhất, nên hỏi thêm đội bán hàng trước khi quyết định.</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="on">Chênh lệch giữa hai mô hình không vượt ngưỡng {vn(C.TREE_FLAG_GAP, 1)} (TreeScore: {vn(r.TreeScore, 3)}).</div>', unsafe_allow_html=True)
        section_caption('04 · Hành động đề xuất')
        st.subheader('Khuyến nghị chăm sóc'); tags('gia_dinh')
        ten, ck, rk = CHAN[r.KenhRule]; ev = r.RiskScore * rk * r.v - ck
        st.markdown(f"""<div class="cx-action-grid">
            <div class="cx-action-item"><span class="cx-action-label">Giá trị một lần mua nếu giữ được khách</span><b>{usd(r.v)}</b><small>Lợi nhuận gộp 41,15% × giá trị đơn trung bình</small></div>
            <div class="cx-action-item"><span class="cx-action-label">Kênh liên hệ · {r.KenhRule}</span><b>{ten}</b></div>
            <div class="cx-action-item"><span class="cx-action-label">Chi phí liên hệ</span><b>{usd(ck)}</b></div>
            <div class="cx-action-item"><span class="cx-action-label">Tỷ lệ thành công giả định</span><b>{pct(rk, 0)}</b></div>
            <div class="cx-action-item"><span class="cx-action-label">Giá trị kỳ vọng chăm sóc</span><b>{vn(ev, 2)} USD</b></div>
            <div class="cx-action-item"><span class="cx-action-label">Sản phẩm gợi ý</span><b>{r.SanPhamGoiY or 'nội dung mặc định (giới thiệu chung các nhóm phụ kiện)'}</b><small>{('(quy tắc ' + r.QuyTacSP + ')') if r.QuyTacSP else ''}</small></div>
        </div><div class="cx-action-decision">{'Đủ điều kiện đưa vào danh sách' if ev > 0 else 'Không đưa vào danh sách cá nhân (quy tắc R2: chi phí lớn hơn lợi ích kỳ vọng)'}</div>""", unsafe_allow_html=True)

# ================= 3. KỊCH BẢN =================
elif man.startswith('3'):
    eyebrow('03 / MÔ HÌNH QUYẾT ĐỊNH');
    st.title('3. Phân tích kịch bản chăm sóc'); tags('gia_dinh')
    ghi_chu('Bạn nhập ba con số của chiến dịch, hệ thống chọn khách có lợi nhất trong ngân sách và cho biết <b>giá trị ròng Z</b> (lợi nhuận kỳ vọng trừ chi phí). Z là giá trị kỳ vọng theo giả định, không phải lợi nhuận chắc chắn.')
    insight('Mẹo sử dụng', 'Thử điều chỉnh từng tham số r, c hoặc B, sau đó chọn một phương pháp phân tích bên dưới để xem tác động. Chỉ số Z không phải lợi nhuận đã ghi nhận.')
    section_caption('01 · Tham số chiến dịch')
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        r = c1.slider('Tỷ lệ chăm sóc thành công r (%): trong 100 khách được chăm sóc, bao nhiêu người quay lại mua', 1, 30, int(C.BASE_SCENARIO['r'] * 100), 1, format='%d%%') / 100
        c = c2.slider('Chi phí cho mỗi khách được chăm sóc c (USD)', 1, 30, int(C.BASE_SCENARIO['c']), 1, format='%d USD') * 1.0
        B = c3.slider('Ngân sách chiến dịch B (USD)', 5000, 150000, int(C.BASE_SCENARIO['B']), 5000, format='%d USD')
    sel, ev = solve(df, r, c, B); Z = ev[sel].sum()
    section_caption('02 · Kết quả theo tham số đã chọn')
    k1, k2, k3, k4 = st.columns(4); k1.metric('Giá trị ròng Z', usd(Z)); k2.metric('Số khách được chọn', vn(len(sel))); k3.metric('Tổng chi phí', usd(c * len(sel))); k4.metric('Số khách giữ lại kỳ vọng', vn((df.RiskScore.values[sel] * r).sum()))
    cl, cr = st.columns([1, 3])
    if cl.button('Lưu kịch bản này'): st.session_state.setdefault('kich_ban', []).append({'r': pct(r, 0), 'c': usd(c), 'B': usd(B), 'Z': usd(Z), 'Số khách': vn(len(sel))}); st.toast('Đã lưu kịch bản vào bảng so sánh')
    if st.session_state.get('kich_ban'):
        cr.dataframe(pd.DataFrame(st.session_state['kich_ban']), hide_index=True, width="stretch")
        if cl.button('Xoá các kịch bản đã lưu'): st.session_state['kich_ban'] = []; st.rerun()
    section_caption('03 · Các phương pháp phân tích')
    with st.container(border=True):
        st.subheader('Kỹ thuật phân tích')
        kt = st.radio('', ['So sánh các kịch bản (what-if)', 'Độ nhạy: thay đổi từng tham số ±20%', 'Tìm mục tiêu: cần r bao nhiêu để đạt Z', 'Z theo ngân sách khi chưa biết r', 'Mô phỏng khi r không chắc chắn', 'Chi phí và tỷ lệ thành công theo kênh'], horizontal=True, label_visibility='collapsed')
    if kt.startswith('So sánh'):
        w = pd.read_csv(f'{R6}/bang_4_4_what_if.csv'); w = w.rename(columns={'kich_ban': 'Kịch bản', 'r': 'r', 'c': 'c (USD)', 'B': 'B (USD)', 'Z': 'Z (USD)', 'K': 'Số khách', 'C': 'Chi phí (USD)', 'giu_lai_ky_vong': 'Khách giữ lại kỳ vọng', 'delta_Z': 'Chênh so với cơ sở (USD)'})
        with st.container(border=True):
            st.subheader('So sánh giá trị ròng Z giữa các kịch bản')
            altair_wide(chart_what_if_z(w))
        st.dataframe(w.style.format({'r': fpct(0), 'c (USD)': fmt(), 'Z (USD)': fmt(), 'B (USD)': fmt(), 'Số khách': fmt(), 'Chi phí (USD)': fmt(), 'Chênh so với cơ sở (USD)': lambda x: ('+' if x > 0 else '') + vn(x), 'Khách giữ lại kỳ vọng': fmt()}), hide_index=True, width="stretch")
        st.caption('Kịch bản cơ sở: r = 10%, c = 10 USD, B = 40.000 USD. Mỗi dòng giải lại bài toán chọn khách.')
    elif kt.startswith('Độ nhạy'):
        rows = []
        for ten, kw in [('Tỷ lệ thành công r', dict(r=r * 1.2)), ('Xác suất không mua lại p', dict(pm=1.2)), ('Tỷ lệ lợi nhuận gộp g', dict(gm=1.2)), ('Chi phí c', dict(c=c * 1.2)), ('Ngân sách B', dict(B=B * 1.2))]:
            d = df.copy()
            if 'pm' in kw: d['RiskScore'] = (d.RiskScore * 1.2).clip(upper=1)
            if 'gm' in kw: d['v'] = d.v * 1.2
            s_, e_ = solve(d, kw.get('r', r), kw.get('c', c), kw.get('B', B)); rows.append(dict(tham_so=ten, delta=e_[s_].sum() - Z))
        t = pd.DataFrame(rows)
        altair_wide(alt.Chart(t).mark_bar(color=NAVY).encode(x=alt.X('delta:Q', title='Thay đổi của Z khi tham số tăng 20% (USD)'), y=alt.Y('tham_so:N', title='', sort='-x'), tooltip=['tham_so', alt.Tooltip('delta:Q', format=',.0f')]).properties(height=220))
        st.caption('r, p và g nhân với nhau trong doanh thu nên tác động bằng nhau khi danh sách không đổi. Chi phí c và ngân sách B đổi cả số khách được chọn.')
    elif kt.startswith('Tìm'):
        S = (df.RiskScore.values[sel] * df.v.values[sel]).sum(); zt = st.number_input('Z mục tiêu (USD)', value=100000, step=10000)
        st.markdown(f'Với danh sách **{vn(len(sel))} khách** đã chốt ở trên:\n- Tỷ lệ thành công tối thiểu để **hoà vốn** (Z = 0): **{pct(c * len(sel) / S, 2)}**\n- Tỷ lệ thành công cần có để Z đạt **{usd(zt)}**: **{pct((zt + c * len(sel)) / S, 2)}**')
        st.caption('Công thức (3.25): r* = (Z* + c·K) / Σ p·v trên K khách đã chọn.')
    elif kt.startswith('Z theo'):
        p = pd.read_csv(f'{R6}/bang_4_4_payoff.csv').rename(columns={'B': 'Ngân sách B (USD)', 'K': 'Số khách', 'r=2%': 'Z nếu r = 2% (bi quan)', 'r=10%': 'Z nếu r = 10% (cơ sở)', 'r=20%': 'Z nếu r = 20% (lạc quan)', 'gia_tri_ky_vong': 'Giá trị kỳ vọng (30/50/20%)'})
        with st.container(border=True):
            st.subheader('Z theo ngân sách ở ba mức tỷ lệ thành công')
            altair_wide(chart_payoff_by_budget(p))
        st.dataframe(p.style.format(fmt()), hide_index=True, width="stretch")
        st.markdown('- **Lạc quan** (tốt nhất trong các kết quả tốt nhất): chọn B = 100.000 USD\n- **Bi quan** (tốt nhất trong các kết quả xấu nhất): chọn B = 40.000 USD\n- **Giá trị kỳ vọng lớn nhất**: chọn B = 100.000 USD\n\nPhương án cuối cùng tuỳ mức chấp nhận rủi ro của người quản lý.')
    elif kt.startswith('Mô phỏng'):
        sim = json.load(open(f'{R6}/mo_phong.json'))
        k1, k2, k3, k4 = st.columns(4); k1.metric('Z trung bình', usd(sim['Z_mean'])); k2.metric('Z xấu nhất 5%', usd(sim['Z_P5'])); k3.metric('Z tốt nhất 5%', usd(sim['Z_P95'])); k4.metric('Xác suất lỗ (Z < 0)', pct(sim['P_Z_am']))
        st.image(f'{R6}/hinh_4_4_mo_phong.png', width="stretch")
        st.caption('10.000 lần rút r từ phân phối Beta (trung bình 9,9%, 90% khối lượng trong 2–22%) với danh sách 4.000 khách của kịch bản cơ sở.')
    else:
        selk, evk = solve(df, r, c, B, kenh=True)
        k1, k2, k3 = st.columns(3); k1.metric('Giá trị ròng Z theo kênh', usd(evk[selk].sum())); k2.metric('Số khách được chọn', vn(len(selk))); k3.metric('Tổng chi phí', usd(df.c_k.values[selk].sum()))
        kk = pd.Series(df.KenhRule.values[selk]).value_counts().rename_axis('Quy tắc').reset_index(name='Số khách'); kk['Hình thức liên hệ'] = kk['Quy tắc'].map(lambda k: CHAN[k][0]); kk['Chi phí mỗi khách (USD)'] = kk['Quy tắc'].map(lambda k: CHAN[k][1]); kk['Tỷ lệ thành công'] = kk['Quy tắc'].map(lambda k: pct(CHAN[k][2], 0))
        st.dataframe(kk[['Quy tắc', 'Hình thức liên hệ', 'Chi phí mỗi khách (USD)', 'Tỷ lệ thành công', 'Số khách']], hide_index=True, width="stretch")
        st.caption('Mỗi khách được gán một kênh theo quy tắc R3–R5 (nhóm và mức rủi ro), rồi chọn khách có lợi nhất trong ngân sách (bài toán cái túi 0–1).')

# ================= 4. DANH SÁCH =================
elif man.startswith('4'):
    eyebrow('04 / HÀNH ĐỘNG');
    st.title('4. Danh sách chăm sóc'); tags('gia_dinh')
    ghi_chu('Danh sách khách được chọn theo giá trị kỳ vọng, kèm hình thức liên hệ, sản phẩm gợi ý và lý do. Bạn có thể thêm hoặc bớt khách, hệ thống tính lại chi phí và Z. Mỗi điều chỉnh thủ công được ghi vào file xuất (cột Nguồn chọn và Lý do điều chỉnh).')
    insight('Luồng thao tác', '1. Chọn ngân sách và kênh → 2. Xem danh sách ưu tiên → 3. Điều chỉnh có lý do → 4. Xuất danh sách nếu vai trò cho phép.')
    section_caption('01 · Thiết lập danh sách')
    with st.container(border=True):
        c1, c2 = st.columns([1, 2]); B = c1.number_input('Ngân sách B (USD)', value=int(C.BASE_SCENARIO['B']), step=5000); kenh = c2.checkbox('Chi phí và tỷ lệ thành công theo kênh R3–R5 (khuyên dùng)', value=True)
    sel, ev = solve(df, C.BASE_SCENARIO['r'], C.BASE_SCENARIO['c'], B, kenh=kenh); d = df.iloc[sel].copy(); d['EV'] = ev[sel]; d = d.sort_values('EV', ascending=False)
    d['NguonChon'] = 'DSS chọn'; d['LyDo'] = ''
    section_caption('02 · Điều chỉnh có lý do')
    data_note('Nhập mã khách, cách nhau bằng dấu phẩy. Thêm dấu trừ trước mã để loại khỏi danh sách, ví dụ: 11000, -19785.')
    with st.container(border=True):
        c3, c4 = st.columns(2); them = c3.text_input('Thêm hoặc bớt khách (CustomerID)', ''); ly_do = c4.text_input('Lý do điều chỉnh (bắt buộc khi thêm hoặc bớt)', '').strip()
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
    section_caption('03 · Tổng kết danh sách')
    k1, k2, k3 = st.columns(3); k1.metric('Số khách trong danh sách', vn(len(d))); k2.metric('Tổng chi phí', usd(tong), 'vượt ngân sách' if tong > B else 'trong ngân sách', delta_color='inverse' if tong > B else 'normal'); k3.metric('Giá trị ròng Z sau điều chỉnh', usd(Z))
    if nhat_ky:
        st.markdown('**Nhật ký điều chỉnh thủ công** (đi kèm file xuất)')
        st.dataframe(pd.DataFrame(nhat_ky).rename(columns={'thao_tac': 'Thao tác', 'ma_khach': 'Mã khách', 'ly_do': 'Lý do'}), hide_index=True, width="stretch")
    section_caption('04 · Danh sách ưu tiên')
    with st.container(border=True):
        st.subheader('Phân bổ khách được chọn theo kênh chăm sóc')
        altair_wide(chart_care_channels(d))
        st.caption('Số khách ở biểu đồ phản ánh đúng danh sách hiện tại, bao gồm thao tác thêm/bớt thủ công nếu có.')
    d['GiaiThichDeDoc'] = [f'Kênh {k_} ({CHAN[k_][0].lower()}) vì khách thuộc {n_}, rủi ro {lv_.lower()}. Giá trị kỳ vọng {vn(e_, 1)} USD. ' + (f'Gợi ý {sp_}. ' if sp_ else '') + de_hieu(tf_)
                           for k_, n_, lv_, e_, sp_, tf_ in zip(d.KenhRule, d.Nhom, d.RiskLevel, d.EV, d.SanPhamGoiY, d.TopFactors)]
    t = d[['CustomerID', 'NguonChon', 'Nhom', 'ABC', 'RiskScore', 'RiskLevel', 'v', 'EV', 'KenhRule', 'SanPhamGoiY', 'GiaiThichDeDoc']].head(500).copy(); t['KenhRule'] = t.KenhRule.map(lambda k: f'{k} – {CHAN[k][0]}')
    t.columns = ['Mã khách', 'Nguồn chọn', 'Nhóm', 'Hạng', 'Xác suất không mua lại', 'Mức rủi ro', 'Giá trị một lần mua (USD)', 'Giá trị kỳ vọng (USD)', 'Hình thức liên hệ', 'Sản phẩm gợi ý', 'Giải thích']
    st.dataframe(t.style.format({'Xác suất không mua lại': fmt(3), 'Giá trị một lần mua (USD)': fmt(1), 'Giá trị kỳ vọng (USD)': fmt(1)}), hide_index=True, width="stretch", height=420)
    if len(d) > 500: st.caption(f'Hiển thị 500 dòng đầu trong {vn(len(d))} khách. Xuất CSV để lấy đủ.')
    section_caption('05 · Xuất kết quả')
    if vai_tro == 'Nhân viên phân tích dữ liệu': st.caption('Vai trò phân tích chỉ xem, không duyệt và không xuất danh sách (Bảng 3.31).')
    else:
        xuat = d[['CustomerID', 'NguonChon', 'LyDo', 'Nhom', 'ABC', 'RiskScore', 'RiskLevel', 'v', 'EV', 'KenhRule', 'SanPhamGoiY', 'QuyTacSP', 'GiaiThich']].rename(columns={'LyDo': 'LyDoDieuChinh'})
        bot_ra = [x_['ma_khach'] for x_ in nhat_ky if x_['thao_tac'] == 'Bớt']
        if bot_ra: xuat = pd.concat([xuat, pd.DataFrame({'CustomerID': bot_ra, 'NguonChon': 'Bớt thủ công (không chăm sóc)', 'LyDoDieuChinh': ly_do})])
        st.download_button('Xuất danh sách đã duyệt (CSV)', xuat.to_csv(index=False).encode('utf-8-sig'), file_name=f'danh_sach_cham_soc_{C.SCORING_DATE}.csv', disabled=thieu_ly_do)

# ================= 5. THEO DÕI =================
else:
    eyebrow('05 / QUẢN TRỊ MÔ HÌNH');
    st.title('5. Theo dõi mô hình và quy tắc'); tags('du_lieu', 'du_doan')
    ghi_chu('Mô hình còn tốt hơn quy tắc đơn giản "khách lâu không mua thì rủi ro cao" hay không. Nếu không còn hơn, cần huấn luyện lại hoặc xem lại thiết kế (quy tắc R9).')
    insight('Mục tiêu theo dõi', 'Đối chiếu mô hình chấm điểm với baseline trên bốn mốc đã đủ nhãn. Khách tại mốc 08/07/2014 chưa có nhãn tương lai, không suy diễn ROC-AUC tại mốc này.')
    t = folds[folds.mo_hinh.isin(['Naive Bayes rời rạc', 'Recency đảo chiều', 'MLP (32,16)'])][['E', 'mo_hinh', 'AUC']].copy(); t['mo_hinh'] = t.mo_hinh.map({'Naive Bayes rời rạc': 'Naive Bayes (đang dùng)', 'Recency đảo chiều': 'Recency (quy tắc đơn giản)', 'MLP (32,16)': 'MLP (so sánh)'})
    t['E'] = pd.to_datetime(t.E).dt.strftime('%d/%m/%Y'); t['AUC_vn'] = t.AUC.map(lambda x: vn(x, 3))
    section_caption('01 · Hiệu năng dự đoán')
    with st.container(border=True):
        st.subheader('Khả năng xếp hạng (ROC-AUC) ở bốn mốc đã đủ nhãn')
        altair_wide(alt.Chart(t).mark_line(point=True).encode(x=alt.X('E:N', title='Mốc đánh giá', sort=None, axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('AUC:Q', scale=alt.Scale(domain=[0.6, 0.8]), title='ROC-AUC', axis=alt.Axis(labelExpr="replace(format(datum.value, '.2f'), '.', ',')")),
                    color=alt.Color('mo_hinh:N', title='', scale=alt.Scale(domain=['Naive Bayes (đang dùng)', 'Recency (quy tắc đơn giản)', 'MLP (so sánh)'], range=[NAVY, '#8A94A6', '#C57B2A']), legend=alt.Legend(orient='bottom', labelLimit=300)), tooltip=[alt.Tooltip('E', title='Mốc'), alt.Tooltip('mo_hinh', title='Mô hình'), alt.Tooltip('AUC_vn', title='ROC-AUC')]).properties(height=300))
    st.caption('0,5 là đoán ngẫu nhiên, 1,0 là hoàn hảo. Mô hình đang dùng bằng hoặc hơn quy tắc đơn giản ở cả bốn mốc và cho xác suất chính xác hơn (Brier 0,125 so với 0,269).')
    section_caption('02 · Biến động dữ liệu')
    with st.container(border=True):
        st.subheader('Cơ cấu khách thay đổi theo thời gian (vì sao phải huấn luyện lại mỗi kỳ)')
        m = moc.rename(columns={'T': 'Mốc', 'so_khach': 'Số khách', 'ty_le_y1': 'Tỷ lệ không mua lại', 'mot_don': 'Tỷ lệ khách mới mua 1 đơn', 'bike': 'Tỷ lệ mua xe đạp', 'nsub2': 'Tỷ lệ mua từ 2 danh mục'})[['Mốc', 'Số khách', 'Tỷ lệ không mua lại', 'Tỷ lệ khách mới mua 1 đơn', 'Tỷ lệ mua xe đạp', 'Tỷ lệ mua từ 2 danh mục']]
        altair_wide(chart_matured_snapshot_trends(moc))
        st.caption('Đường tỷ lệ không mua lại chỉ dùng các Snapshot đã có nhãn; không tính kết quả thực tế cho ngày chấm điểm 08/07/2014.')
        st.dataframe(m.style.format({'Số khách': fmt(), 'Tỷ lệ không mua lại': fpct(), 'Tỷ lệ khách mới mua 1 đơn': fpct(), 'Tỷ lệ mua xe đạp': fpct(), 'Tỷ lệ mua từ 2 danh mục': fpct()}), hide_index=True, width="stretch", height=300)
        st.caption('Mốc 08/07/2014 là mốc chấm điểm nên chưa có tỷ lệ không mua lại (dấu —).')
    section_caption('03 · Phiên bản & quy tắc')
    st.subheader('Phiên bản mô hình và quy tắc đang dùng')
    km = json.load(open(f'{ROOT}/models/kmeans_E{C.SCORING_DATE.replace("-", "")}.json'))
    st.dataframe(pd.DataFrame([{'Thành phần': 'Mô hình chấm điểm', 'Phiên bản': f'NB_T{C.SCORING_TRAIN_DATE.replace("-", "")}_v1', 'Học ở mốc': '01/03/2014', 'Ghi chú': 'Naive Bayes, 5 thuộc tính rời rạc'}, {'Thành phần': 'Cây đối chứng', 'Phiên bản': f'TREE_T{C.SCORING_TRAIN_DATE.replace("-", "")}_v1', 'Học ở mốc': '01/03/2014', 'Ghi chú': '11 lá, cho TopFactors'}, {'Thành phần': 'Phân nhóm', 'Phiên bản': f'KMEANS_E{C.SCORING_DATE.replace("-", "")}_v1', 'Học ở mốc': '08/07/2014', 'Ghi chú': f'k = 5, silhouette {km["silhouette"]:.3f}'.replace('.', ',')}, {'Thành phần': 'Kho quy tắc', 'Phiên bản': 'R1–R9 bản 1', 'Học ở mốc': '—', 'Ghi chú': 'R1, R9 tạm tắt vì chưa có dữ liệu CRM'}]), hide_index=True, width="stretch")
    if vai_tro != 'Nhân viên chăm sóc khách hàng':
        st.subheader('Đề xuất quy tắc mới (trạng thái chờ duyệt)')
        c1, c2 = st.columns(2); dk = c1.text_input('Điều kiện (IF)', placeholder='ví dụ: Nhóm N2 và đã mua Road Bikes'); kn_ = c2.text_input('Khuyến nghị (THEN)', placeholder='ví dụ: Gợi ý Helmets')
        if st.button('Gửi duyệt'):
            if dk.strip() and kn_.strip(): st.markdown(f'<div class="on">Đã ghi nhận đề xuất "NẾU {dk.strip()} THÌ {kn_.strip()}" ở trạng thái chờ duyệt. Bản trình diễn chưa lưu đề xuất vào kho, quản lý duyệt rồi nhân viên phân tích thêm vào analytics.CareRule.</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="canh-bao">Cần nhập cả điều kiện và khuyến nghị.</div>', unsafe_allow_html=True)
    st.caption('Nhóm đối chứng và quy tắc R1, R9 cần dữ liệu chiến dịch từ CRM, chưa có trong phạm vi đề tài (mục 3.5.6).')
