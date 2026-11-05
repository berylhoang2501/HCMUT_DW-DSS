# CompanyX DSS

Bài tập lớn môn Kho dữ liệu và Hệ hỗ trợ ra quyết định (CO5113, ĐH Bách Khoa TP.HCM): dự đoán khách hàng cá nhân rời bỏ và hệ hỗ trợ ra quyết định giữ chân khách cho CompanyX (nhà sản xuất xe đạp, dữ liệu kiểu AdventureWorks, SQL Server).

Trước khi sửa gì, đọc `HANDOVER.md` (quy tắc, thiết kế đã chốt, việc còn lại).

## Có gì trong repo

| Thư mục | Nội dung |
|---|---|
| `latex/` | Báo cáo (pdflatex). Chương 1–4 xong, 5–8 còn khung |
| `sql/` | Script T-SQL: kho `CompanyX_DW`, ETL `etl.usp_FullLoad`, bảng Snapshot, bảng DSS |
| `python/` | Chuỗi phân tích `cum3b` → `cum4` → `cum4b` → `cum5` → `cum6` → `cum6b`, app DSS, script sinh bảng và hình cho báo cáo |
| `results/` | Bảng, hình, file SQL điểm rủi ro do các script sinh ra |
| `docs/` | Bản nháp, biên bản chuẩn hoá, ghi chú làm việc |

Không đưa lên git: `data/*.csv`, `models/*.joblib`, `backup/*.bak`, slide môn học, báo cáo mẫu.

## Chạy lại

1. Dựng kho: chạy các file trong `sql/` theo thứ tự ở `docs/README_THU_TU_CHAY.txt`, hoặc restore bản sao lưu trong `backup/`.
2. Cài môi trường (Python 3.9–3.11):
   ```bash
   python3 -m venv .venv && .venv/bin/pip install -r python/requirements.txt
   ```
3. Đặt biến môi trường kết nối SQL Server (xem đầu `python/config.py`), rồi chạy chuỗi phân tích:
   ```bash
   for s in cum3b_nhan_va_dac_trung cum4_huan_luyen cum4b_bo_sung_chuong3 cum5_cham_diem_sinh_sql cum6_phan_tich_dss cum6b_bo_sung_chuong3; do .venv/bin/python python/$s.py || break; done
   ```
4. Mở giao diện DSS (đọc `results/cum6/dss_khach.csv`):
   ```bash
   .venv/bin/python -m streamlit run python/app_dss.py
   ```

## Biên dịch báo cáo

```bash
cd latex && pdflatex main.tex && pdflatex main.tex
```

Bảng và hình của chương 3 và 4 sinh bằng `python/tao_bang_tex_*.py` và `python/ve_*.py`, không sửa tay trong `latex/bang/` và `latex/IMAGE/`.
