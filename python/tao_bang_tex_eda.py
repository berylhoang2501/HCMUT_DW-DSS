"""Sinh các bảng LaTeX cho chương "Tiền xử lý và khám phá dữ liệu" từ file kết quả.

Mọi con số trong bảng lấy thẳng từ results/ nên không gõ tay.
Ra: latex/bang/*.tex (được \\input trong latex/4_tien_xu_ly_eda.tex)
Chạy: .venv/bin/python python/tao_bang_tex_eda.py
"""
import os
import numpy as np
import pandas as pd

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, "latex", "bang")
os.makedirs(RA, exist_ok=True)
R = lambda *p: os.path.join(GOC, "results", *p)


def so(x, nd=0):
    """Số kiểu Việt."""
    if pd.isna(x):
        return "--"
    s = f"{x:,.{nd}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return "$-$" + s[1:] if s.startswith("-") else s


def pct(x, nd=1):
    """Phần trăm, làm tròn nửa lên (tránh lệch do làm tròn nhị phân)."""
    if pd.isna(x):
        return "--"
    from decimal import Decimal, ROUND_HALF_UP
    v = (Decimal(str(round(float(x), 6))) * 100).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return so(float(v), nd) + "\\%"


def ngay(s):
    """2013-12-15 hoặc 15/12/2013 -> 15/12/2013."""
    s = str(s)
    if "-" in s:
        y, m, d = s.split("-")
        return f"{d}/{m}/{y}"
    return s


def ghi(ten, dong_tieu_de, cot, dong, ghi_chu_cot=None):
    spec = cot
    out = [f"\\begin{{tabular}}{{{spec}}}", "\\toprule", dong_tieu_de + " \\\\", "\\midrule"]
    for r in dong:
        out.append(" & ".join(r) + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}"]
    with open(os.path.join(RA, ten), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


# Bảng 20 mốc
m = pd.read_csv(R("cum3b", "bang_4_3_1a_moc.csv")) if os.path.exists(R("cum3b", "bang_4_3_1a_moc.csv")) else None
assert m is not None, "thiếu results/cum3b/bang_4_3_1a_moc.csv"
dong = []
for _, r in m.iterrows():
    dong.append([ngay(r.iloc[0]), so(r["so_khach"]),
                 so(r["y1"]) if not pd.isna(r["y1"]) else "--",
                 pct(r["y1"] / r["so_khach"]) if not pd.isna(r["y1"]) else "--",
                 pct(r["mot_don"]), pct(r["bike"]), pct(r["nsub2"])])
ghi("moc.tex",
    "Mốc $T$ & Số khách & Số khách $y=1$ & Tỷ lệ $y=1$ & Chỉ 1 đơn & BikeBuyer & NSub $\\geq 2$",
    "lrrrrrr", dong)
assert len(dong) == 20

# Bảng bốn fold + mốc chấm điểm
f = pd.read_csv(R("cum3b", "bang_4_3_1b_fold.csv"))
dong = []
for _, r in f.iterrows():
    cs = str(r["cua_so_nhan"]).split("→")
    dong.append([ngay(r["moc_huan_luyen"]), so(r["khach_huan_luyen"]), pct(r["ty_le_y1_huan_luyen"]),
                 ngay(r["moc_danh_gia"]), so(r["khach_danh_gia"]),
                 pct(r["ty_le_y1_danh_gia"]) if not pd.isna(r["ty_le_y1_danh_gia"]) else "--",
                 f"{ngay(cs[0].strip())} đến {ngay(cs[1].strip())}"])
ghi("fold.tex",
    "Mốc huấn luyện & Số khách & $y=1$ & Mốc đánh giá & Số khách & $y=1$ & Cửa sổ nhãn của mốc huấn luyện",
    "lrrlrrl", dong)

# Bảng khoảng rời rạc hóa
k = pd.read_csv(R("cum3b", "bang_4_3_1c_khoang.csv"))
dong = []
for _, r in k.iterrows():
    kh = str(r["khoang"]).replace("<", "$<$").replace("≥", "$\\geq$")
    dong.append([str(r["thuoc_tinh"]), kh, so(r["so_khach"]), pct(r["ty_le_y1"])])
ghi("khoang.tex", "Thuộc tính & Khoảng & Số khách & Tỷ lệ $y=1$", "llrr", dong)

# Thống kê mô tả tại mốc chấm điểm
d = pd.read_csv(R("cum6", "dss_khach.csv"))
assert len(d) == 18360
dong = []
for c, nd in [("Recency", 0), ("Frequency", 0), ("Monetary", 2), ("AOV", 2), ("Tenure", 0), ("NSub", 0)]:
    s = d[c]
    dong.append([c, so(s.mean(), 2), so(s.std(), 2), so(s.min(), nd), so(s.quantile(.25), nd),
                 so(s.median(), nd), so(s.quantile(.75), nd), so(s.max(), nd)])
ghi("thong_ke.tex", "Thuộc tính & Trung bình & Độ lệch chuẩn & Nhỏ nhất & Q1 & Trung vị & Q3 & Lớn nhất",
    "lrrrrrrr", dong)

# Cặp tương quan hạng mạnh nhất (trung bình 5 mốc huấn luyện)
t = pd.read_csv(R("cum4b", "bang_4_3_2g_tuong_quan.csv")).head(8)
dong = [[r["thuoc_tinh_1"].replace("_", "\\_"), r["thuoc_tinh_2"].replace("_", "\\_"),
         so(r["rho_spearman_TB"], 3), f"{so(r['rho_min'], 3)} đến {so(r['rho_max'], 3)}"]
        for _, r in t.iterrows()]
ghi("tuong_quan.tex", "Thuộc tính 1 & Thuộc tính 2 & $\\rho$ trung bình & Khoảng giữa 5 mốc", "llrr", dong)

print("đã ghi:", sorted(os.listdir(RA)))



# Bảng thử bỏ BikeBuyer khỏi Naive Bayes: ROC-AUC, Brier và sai số hiệu chỉnh (ECE) ở bốn cặp mốc kiểm định
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import roc_auc_score, brier_score_loss

ds_ = pd.read_csv(os.path.join(GOC, "data", "dataset.csv"), parse_dates=["T"])
B_REC = [-1, 89, 179, 269, 364, 539, 1e6]


def x_nb(df, q, cols):
    m = {"R": pd.cut(df.Recency, B_REC, labels=False).values, "F": pd.cut(df.Frequency, [0, 1, 2, 1e6], labels=False).values,
         "M": np.searchsorted(q, df.Monetary.values), "B": df.BikeBuyer.values, "N": pd.cut(df.NSub, [-1, 1, 2, 4, 1e6], labels=False).values}
    return np.column_stack([m[c] for c in cols])


def ece(y, p, k=10):
    b = np.minimum((p * k).astype(int), k - 1)
    return sum((b == i).mean() * abs(y[b == i].mean() - p[b == i].mean()) for i in range(k) if (b == i).any())


kq = {"du": [], "bo": []}
dong = []
for T, E in [("2013-09-01", "2013-12-15"), ("2013-10-01", "2014-01-15"), ("2013-11-01", "2014-02-15"), ("2013-11-15", "2014-03-01")]:
    tr, te = ds_[ds_["T"] == T], ds_[ds_["T"] == E]
    q = tr.Monetary.quantile([.25, .5, .75]).values
    res = {}
    for k, cols in (("du", ["R", "F", "M", "B", "N"]), ("bo", ["R", "F", "M", "N"])):
        xa, xb = x_nb(tr, q, cols), x_nb(te, q, cols)
        nb = CategoricalNB(alpha=1, min_categories=[int(max(xa[:, i].max(), xb[:, i].max()) + 1) for i in range(xa.shape[1])]).fit(xa, tr.y.values)
        p_ = nb.predict_proba(xb)[:, 1]
        y_ = te.y.values
        res[k] = (roc_auc_score(y_, p_), brier_score_loss(y_, p_), ece(y_, p_))
        kq[k].append(res[k])
    dong.append([f"{ngay(E)} ← {ngay(T)}"] + [so(res[k][j], 3 if j != 1 else 4) for j in (0, 1, 2) for k in ("du", "bo")])
tb = {k: np.mean(v, axis=0) for k, v in kq.items()}
dong.append(["\\textbf{Trung bình}"] + [so(tb[k][j], 3 if j != 1 else 4) for j in (0, 1, 2) for k in ("du", "bo")])
assert abs(tb["du"][0] - 0.7199) < 5e-4 and abs(tb["bo"][0] - 0.7289) < 5e-4      # khớp bảng thử tập thuộc tính của chuỗi phân tích
ghi("bo_bikebuyer.tex", "Cặp mốc ($E \\leftarrow T$) & AUC đủ 5 & AUC bỏ BB & Brier đủ & Brier bỏ BB & ECE đủ & ECE bỏ BB",
    "lrrrrrr", dong)
print("bỏ BikeBuyer: trung bình", {k: [round(float(x), 4) for x in v] for k, v in tb.items()})
