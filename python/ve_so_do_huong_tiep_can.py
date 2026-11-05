"""Vẽ sơ đồ hướng tiếp cận bài toán churn (năm bước nối tiếp, mỗi bước là một chương) cho báo cáo LaTeX.

Chỉ có chữ giải thích, không có số liệu. Ra: latex/IMAGE/huong_tiep_can.png
Chạy: .venv/bin/python python/ve_so_do_huong_tiep_can.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plt.rcParams["font.family"] = "Arial"
NAVY, XAM = "#1f3a5f", "#5a6b7d"

BUOC = [
    ("1. Kho dữ liệu", ["Gom dữ liệu bán hàng", "vào kho hình sao,", "chụp hành vi từng", "khách tại 20 mốc"],
     "Chương 3", "Giải: dữ liệu rải rác, thiếu\ntheo dõi theo thời gian"),
    ("2. Xác định churn", ["Khách không đặt đơn", "trong 90 ngày sau", "một mốc là có nguy cơ", "rời bỏ, tính thuộc tính"],
     "Chương 4", "Giải: dữ liệu\nchưa có nhãn churn"),
    ("3. Dự đoán", ["Chấm điểm rủi ro", "cho từng khách,", "thử mô hình theo", "đúng trình tự thời gian"],
     "Chương 5", "Trả lời: khách nào\ncó nguy cơ rời bỏ"),
    ("4. Ra quyết định", ["Kết hợp rủi ro với", "giá trị khách, chọn", "khách trong ngân sách,", "gợi ý cách chăm sóc"],
     "Chương 6", "Giải: ưu tiên ai,\nchi bao nhiêu"),
    ("5. Đánh giá", ["So với cách chọn khách", "đơn giản, nêu rõ", "chỗ làm được, chỗ", "chưa làm được"],
     "Chương 7", "Kiểm tra: có tốt hơn\ncách đơn giản không"),
]

fig, ax = plt.subplots(figsize=(12.6, 3.7))
ax.set_xlim(-1.5, 127.5)
ax.set_ylim(6, 42)
ax.axis("off")

W, GAP, Y, H = 22, 4, 14, 26
for i, (tieu_de, dong, chuong, giai) in enumerate(BUOC):
    x = i * (W + GAP)
    ax.add_patch(FancyBboxPatch((x, Y), W, H, boxstyle="round,pad=0.2,rounding_size=1.2", fc="white", ec=NAVY, lw=1.6))
    ax.text(x + W / 2, Y + H - 2.4, tieu_de, ha="center", va="top", fontsize=10.2, fontweight="bold", color=NAVY)
    for k, d in enumerate(dong):
        ax.text(x + W / 2, Y + H - 7.6 - k * 3.2, d, ha="center", va="top", fontsize=8.4, color="#222")
    ax.text(x + W / 2, Y + 1.6, chuong, ha="center", va="bottom", fontsize=8.4, fontweight="bold", color=XAM)
    ax.text(x + W / 2, Y - 2.2, giai, ha="center", va="top", fontsize=8.2, color="#b03a2e", linespacing=1.3)
    if i < len(BUOC) - 1:
        ax.add_patch(FancyArrowPatch((x + W + 0.4, Y + H / 2), (x + W + GAP - 0.4, Y + H / 2),
                                     arrowstyle="-|>", mutation_scale=14, lw=1.6, color="#444"))

out = os.path.join(GOC, "latex", "IMAGE", "huong_tiep_can.png")
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print("đã vẽ", out)
