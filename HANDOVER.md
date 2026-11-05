# HANDOVER – Dự án TA_DSS (cập nhật 04/11/2026, máy Mac)

> **Cập nhật 04/11 (tối):** báo cáo chính thức nay viết bằng **LaTeX trong `latex/`** (chương 1–4 xong, 5–8 còn khung). Nhóm **không sửa Google Doc nữa**, các mục về Doc ở dưới chỉ để tham khảo. Gói bàn giao `0_BAT_DAU_O_DAY/`, các script sinh HTML dán Doc, `so_bang_hinh.py`, `tao_huong_dan.py`, `tinh_kha_dung.py` đã xoá khỏi repo (lấy lại từ lịch sử git, commit trước `Don repo`). Slide môn học và báo cáo mẫu `latex_mau/` chỉ còn trên máy, không đưa lên git.

Tài liệu bàn giao cho agent hoặc người làm tiếp. **Đọc hết file này trước khi sửa repo hay Google Doc.** Lịch sử chi tiết từng ngày ở `docs/NOTES_WORKING.md`, biên bản chuẩn hoá dữ liệu ở `docs/BIEN_BAN_CHUAN_HOA.md`.

---

## 0. Bắt đầu phiên mới
1. `git fetch origin` rồi `git pull` nhánh `main`. GitHub là nơi đồng bộ giữa máy Mac và PC.
2. Đọc mục 2 (quy tắc của Bảo) và mục 8 (việc còn lại).
3. Mở Doc ở tab `t.0`, xuất HTML để lấy số comment và số ảnh hiện tại (mục 2.3). Hiện là **89 comment, 40 ảnh**. Sau mỗi đợt sửa phải giữ nguyên hai số này (trừ khi chủ ý thêm ảnh).
4. Trả lời Bảo bằng **tiếng Việt, ngắn**.

## 1. Dự án là gì
- **Môn:** Hệ hỗ trợ ra quyết định (Data Warehouses and Decision Support Systems), ĐH Bách Khoa TP.HCM. **Đề tài:** Customer Churn Prediction and Retention Decision Support System – CompanyX (dữ liệu bán xe đạp kiểu AdventureWorks).
- **Sản phẩm nộp:** báo cáo nhóm trên Google Doc **"TA_DSS"**, cộng demo, slide, danh sách thành viên kèm % đóng góp và tài nguyên hệ thống, nén thành một file zip (mục 1.3). Bản LaTeX trong `latex/` đang tạm dừng.

### 1.1. Đường link
| Thứ | Link |
|---|---|
| Google Doc báo cáo | https://docs.google.com/document/d/18LCYtxYRWqz9Dqq9iuiSXKTlC2ND2yQOuJmVn8RZXYA/edit?tab=t.0 |
| Xuất HTML của tab t.0 (đọc bằng `fetch` trong trình duyệt đã đăng nhập) | https://docs.google.com/document/d/18LCYtxYRWqz9Dqq9iuiSXKTlC2ND2yQOuJmVn8RZXYA/export?format=html&tab=t.0 |
| Repo GitHub | https://github.com/zafkiel-ltb/HCMUT_DWH (nhánh `main`) |
| Notebook môn học (Gemini Notebook, nguồn là slide Lecture 0–7) | https://notebook.google.com/notebook/4d5a7c2c-b1b7-4228-86b7-fa7672b6fb6f |
| Gemini (dùng để phản biện) | https://gemini.google.com/app?hl=vi |
| Slide môn học (bản PDF, chỉ trên máy, không có trên git) | `tai_lieu_mon_hoc/Lecture 0-Overview.pdf` … `Lecture 7-MSS Modeling.pdf` |
| Báo cáo mẫu của nhóm khác (LaTeX, chỉ trên máy, không có trên git) | `latex_mau/` (xem mục 10) |

### 1.2. Tab của Doc
| Tab | ID | Nội dung | Được sửa? |
|---|---|---|---|
| Phần 345_Ver sả… | `t.0` | Bảng thang điểm, Chương 3, 4, 5, 6 | Có, theo quy tắc ở mục 2 |
| Chương 1 + 2 | `t.75iauuo2dbud` | Chương 1 (Giới thiệu), Chương 2 (Xác định bài toán kinh doanh, câu hỏi Q1–Q4 ở 2.2) | Không |
| Thương | `t.il6cqlh308gx` | Bản nháp của thành viên khác, nhiều câu và chú thích trùng với t.0 | Không |
| Chương 1 + 2 (Up…) | chưa ghi | Bản cập nhật Chương 1–2 | Không |

- **Người trong nhóm:** Lương Thiên Bảo (chủ repo, chủ báo cáo), Phạm Nguyễn Thùy Dương, Phan Thị Hồng Nhung, Hoàng Ngọc Thủy Thương, và Nguyễn Thái Ngọc Giao (MSSV 2670206). Thành viên viết 3.2–3.3 giữ phần đó, người khác không sửa.

### 1.3. Yêu cầu của môn (slide `Lecture 0-Overview.pdf`)
- **Thang điểm bài nhóm (slide 12), đã có ở đầu tab t.0:**

| Tiêu chí | Điểm | Mục đáp ứng |
|---|---|---|
| Giải bài toán (How to solve the goal challenges) | 2 | Chương 1–3 |
| Kho dữ liệu (DW design and management) | 2 | 3.2–3.3, 4.2 |
| Thiết kế DSS | 2 | 3.5 |
| Hiện thực DSS | 2 | 4.4–4.5 |
| Trình bày kết quả | 1 | Demo, slide |
| Báo cáo | 1 | Toàn bài |
| Thưởng: mô hình, kỹ thuật AI, phương pháp hỗ trợ quyết định thêm | tối đa +2 | 3.4, 4.3, 5.2 |

- **Slide 12–13:** phải ghi rõ **% đóng góp của từng thành viên**. Nộp một file zip tên `<GroupNo>_<TeamNo>_<SubmitterFullName>_<SubmitterStudentNo>.zip` gồm báo cáo, danh sách thành viên kèm % đóng góp, tài nguyên hệ thống. Một người đại diện nộp lên LMS và nhớ bấm "submit".
- **Slide 15:** dùng công cụ AI chỉ để hỗ trợ (tìm tài liệu, gợi ý ý tưởng, kiểm ngữ pháp, trình bày). **Khi có dùng phải ghi rõ công cụ và cách dùng trong tài liệu tham khảo hoặc chú thích.** Doc hiện **chưa có** dòng khai báo này (mục 8).
- **Thầy đã dặn thêm:** có luật xác định churn. Cây quyết định học từ dữ liệu và có đủ R, F, M. Mọi lựa chọn phải có lập luận. Dùng các chỉ số cơ bản (ma trận nhầm lẫn, accuracy, tỷ lệ lỗi, precision, recall, specificity, F1), chỉ số nào không dùng được thì nói rõ. Slide môn học có demo churn (Lecture 5, slide 71), không có ROC-AUC.

## 2. Quy tắc của Bảo (bắt buộc)
### 2.1. Nội dung
1. **Số liệu phải bám bài làm:** mọi con số lấy từ Chương 4 trên Doc hoặc `results/`, không tự tính số mới mà không ghi rõ cách tính. **Không bao giờ bịa số liệu** (ví dụ kết quả thử nghiệm người dùng khi chưa thử).
2. **Lý thuyết phải trích từ slide môn học** (`tai_lieu_mon_hoc/Lecture*.pdf`, đọc bằng `pypdf` trong `.venv`, hoặc hỏi Notebook). Trong thân bài chỉ ghi "theo tài liệu môn học" hoặc số tài liệu [n] trong danh mục "Tài liệu tham khảo chương 3" ([1] Turban, [3] Han, [15] Simon, [16] Sprague, [21] ISO 9241-11, [22] Sharda…). Phần vượt môn học thì ghi "ngoài nội dung môn học".
3. **Quy trình trước khi sửa nội dung Doc:** hỏi Notebook về slide → viết nháp vào repo (`docs/DRAFT_*.md`, có phần đối chiếu từng số và từng câu lý thuyết) → nhờ Notebook hoặc Gemini phản biện → **tự kiểm từng ý phản biện với dữ liệu** (Gemini từng nói sai) → báo Bảo → chỉ dán khi Bảo đồng ý.

### 2.2. Khi sửa Google Doc
1. Chỉ sửa tab t.0. Không sửa mục 3.2 và 3.3.
2. **Không đóng, xoá hay trả lời comment có sẵn.** Xoá chữ đang mang comment cũng làm mất comment, nên kiểm trong bản xuất HTML (dấu `[a]`, `[bt]`…) trước khi xoá. Muốn đính chính thì thêm comment mới (Chèn → Nhận xét, bấm nút "Nhận xét" của ô mới, không bấm "Trả lời nhận xét").
3. Thân bài **không dùng dấu chấm phẩy**, không viết "bài giảng" hay "Lecture". Arial 11, giãn dòng 1,5, số kiểu Việt (0,837 và 18.360). Chú thích bảng và hình in nghiêng, canh giữa, không đậm. Chú thích bảng đặt trên bảng, chú thích hình đặt dưới hình.
4. Chú thích bảng và đoạn chứa ảnh bật "Giữ với đoạn tiếp theo". **Bảng không bị tách trang, không để chú thích hay tiêu đề mồ côi cuối trang.**
5. Kiểu tiêu đề: CHƯƠNG là Heading 2, mục x.y là Heading 3, mục x.y.z là Heading 4, tất cả Arial 11 đậm.
6. Ô tìm Ctrl+F của Docs tìm qua mọi tab, mà tab Thương có nhiều câu trùng t.0. Dùng **Chỉnh sửa → Tìm và thay thế**, mỗi lần mở hộp thoại phải chọn lại phạm vi **"Thẻ hiện tại"** (nó tự đặt lại "Tất cả thẻ") và bỏ chọn **"Bỏ qua các dấu"**. Trước khi bấm Thay thế phải thấy "1 trong tổng số 1" (hoặc đúng số chỗ đã đếm).
7. **Trước mỗi đợt sửa lớn, đặt tên phiên bản** (Tệp → Nhật ký phiên bản → Đặt tên cho phiên bản hiện tại). Sau khi sửa, kiểm lại số comment, số ảnh, dấu chấm phẩy, và so chữ trên Doc với bản nháp.
8. Không sửa các tab khác. **Tải file về máy phải hỏi Bảo trước.**

### 2.3. Khi sửa repo và commit
1. Các file `docs/HUONG_DAN_CUM5.md`, `HUONG_DAN_CUM6.md`, `DRAFT_4_3_2_BO_SUNG.md`, `DOI_CHIEU_CHUONG_3.md` từng được sinh tự động, nay là bản tĩnh (script sinh đã xoá), dùng làm nguồn tham khảo khi viết Chương 5–8 LaTeX.
2. Bảng và hình của báo cáo LaTeX do `python/tao_bang_tex_*.py` và `python/ve_*.py` sinh vào `latex/bang/` và `latex/IMAGE/`, không sửa tay số liệu trong các file đó.
3. Hằng số thiết kế chỉ ở `python/config.py`. Không đổi nếu chưa sửa Chương 3 trên Doc trước.
4. Không chạy lại `python/cum4_huan_luyen.py` nếu không cần (ghi đè `models/*.joblib`). Sau mọi lần chạy, `git diff --stat results/cum5/*.sql results/cum6/*.sql` phải rỗng.
5. **Chỉ commit khi Bảo đồng ý.** Tác giả và người commit là **tài khoản GitHub `zafkiel-ltb` của Bảo**: dùng `git config user.name` và `user.email` sẵn có trên máy (kiểm bằng `git config user.name`, phải ra `zafkiel-ltb`), không dùng `-c user.name=...` khác. **Không thêm dòng `Co-Authored-By` của Claude hay bất kỳ AI nào** vào commit hay PR. Nhánh làm việc là `main` (đồng bộ Mac và PC).

## 3. Thiết kế đã chốt (đừng đổi nếu nhóm không thống nhất lại)
- **Kho dữ liệu:** CompanyX_DW sao Kimball (4 Dim, 2 Fact). ETL T-SQL `etl.usp_FullLoad` (11 bước: Extract.Customer, Extract.Order, Extract.OrderLine, Extract.Product, Extract.Territory, Load.DimCustomer, Load.DimDate, Load.DimProduct, Load.DimTerritory, Load.FactSalesOrder, Load.FactSalesOrderLine) gọi từ `sql/2_Cum2_ETL_moi/C2_02_Run_ETL_ONLY.py`. Bảng `analytics.CustomerSnapshot` có 20 mốc, 196.985 dòng, vân tay SHA-256 `0x044F3D49…` (đủ chuỗi trong `sql/VERIFY_STATE.sql`).
- **Nhãn:** y = 1 nếu khách không có đơn trong [T, T+90). Nhãn chỉ dùng khi T + 97 ≤ E. Cửa sổ nhãn kết thúc trước 01/06/2014, vì tháng 6/2014 có 930 đơn nhưng không có đơn xe đạp.
- **Bốn fold (Bảng 3.12), cặp (E ← T):** 15/12/2013 ← 01/09/2013, 15/01/2014 ← 01/10/2013, 15/02/2014 ← 01/11/2013, 01/03/2014 ← 15/11/2013. Chấm điểm ngày 08/07/2014 bằng mô hình học ở 01/03/2014.
- **Mô hình:** chấm điểm bằng Naive Bayes rời rạc (R, F, M, BikeBuyer, NSub). Cây Gini (sâu 4, 400 khách mỗi lá, m = 50) sinh luật IF-THEN và TopFactors. So sánh với MLP (32,16), Logistic Regression, Recency đảo chiều, lớp đa số. Ngoài nội dung môn học: Random Forest, gradient boosting, kNN. Chọn mô hình theo ba điều kiện ở 3.4.6 (điều kiện 1 là ROC-AUC **không thấp hơn** Recency đảo chiều), hoà thì so Z. Naive Bayes thắng MLP về Z ở 4/4 fold.
- **RiskLevel Cao:** RiskPercentile ≥ 75 tính **trong từng hạng ABC** (80%/95% Monetary), đồng điểm xếp theo Recency giảm dần.
- **DSS:** EV = p·r·v − c, kịch bản cơ sở r = 10%, c = 10 USD, B = 40.000 USD. ABC, K-means k = 5 (N1–N5), kho quy tắc R1–R9 (R1, R9 tắt vì chưa có dữ liệu CRM). What-if, độ nhạy ±20%, tìm mục tiêu, Z theo ngân sách và r, mô phỏng Beta, bài toán cái túi theo kênh R3/R4/R5, dự báo hồi quy tuyến tính. Giao diện Streamlit 5 màn hình (`python/app_dss.py`).
- **Thử nghiệm người dùng (SUS):** đã bỏ theo quyết định của Bảo ngày 04/11. Đánh giá khả dụng chỉ có rà soát nội bộ theo 10 nguyên tắc Nielsen (Bảng 4.33).

## 4. Repo
| Đường dẫn | Nội dung |
|---|---|
| `sql/0_…` đến `sql/3_…` | Kho dữ liệu, ETL, Snapshot (thứ tự chạy trong `docs/README_THU_TU_CHAY.txt`) |
| `sql/4_Cum1b_Schema_DSS_DE_XUAT.sql` | Thêm giá vốn và 3 bảng DSS |
| `sql/VERIFY_STATE.sql`, `RESET_SCORES.sql`, `RESET_DSS.sql` | Kiểm vân tay kho, xoá điểm, xoá kết quả DSS |
| `python/config.py` | Kết nối (qua biến môi trường) và mọi hằng số thiết kế |
| `python/models_def.py` | Lớp mô hình dùng chung (để joblib nạp được) |
| `python/cum3b…` → `cum4…` → `cum4b…` → `cum5…` → `cum6…` → `cum6b…` | Chuỗi phân tích, mỗi script ghi vào `results/<cụm>/` và tự kiểm |
| `python/tao_bang_tex_eda.py`, `tao_bang_tex_etl.py`, `ve_hinh_eda.py`, `ve_so_do_etl.py`, `ve_luoc_do_sao.py`, `etl_nhat_ky.py` | Sinh bảng và hình cho báo cáo LaTeX (chương 3 và 4) |
| `python/tao_ipynb_kiem_chung_4.py` → `python/kiem_chung_chuong_4.ipynb` | Notebook kiểm chứng số liệu Chương 4 trực tiếp trên kho (chỉ đọc), xuất `results/doc/kiem_chung_chuong_4.html` |
| `python/app_dss.py`, `.streamlit/config.toml` | Giao diện DSS |
| `data/*.csv`, `models/`, `backup/*.bak` | Dữ liệu trích từ kho, mô hình đã học, bản sao lưu kho sau cụm 3A (không đưa lên GitHub) |
| `results/` | Toàn bộ bảng, hình, SQL sinh ra. Ảnh dán lên Doc ở `results/doc/hinh_app/` |
| `docs/DRAFT_CHUONG_5.md` | Bản nháp Chương 5 đúng như trên Doc. Phần A là chữ đã dán, phần B đối chiếu từng số với Chương 4 và từng câu lý thuyết với slide |
| `latex/` | **Báo cáo chính thức** (pdflatex): bìa, chương 1–4 đã viết, chương 5–8 còn khung, tài liệu tham khảo |
| `docs/` | Bản nháp Chương 4–5 trên Doc, đối chiếu, ghi chú làm việc |

## 5. Môi trường
1. **Mac (máy của Bảo):** `.venv` Python 3.9.6 trong repo, có pandas, scikit-learn, pypdf. Chạy script: `.venv/bin/python python/<script>.py`. Không có SQL Server trên Mac.
2. **Chuỗi phân tích trên Windows:** Python 3.9–3.11 với `scikit-learn==1.6.1` (bắt buộc để nạp `.joblib`).
   ```
   py -m venv .venv
   .venv\Scripts\pip install -r python\requirements.txt
   for %s in (cum4b_bo_sung_chuong3 cum5_cham_diem_sinh_sql cum6_phan_tich_dss cum6b_bo_sung_chuong3) do .venv\Scripts\python python\%s.py
   ```
3. **App và notebook trên PC:** venv `C:\Users\bdz24\vdss` (Python 3.14, có streamlit, pandas, pyodbc, jupyter). Đặt venv ở đường dẫn ngắn vì Windows chặn đường dẫn dài khi cài streamlit.
   ```
   C:\Users\bdz24\vdss\Scripts\python -m streamlit run python\app_dss.py
   C:\Users\bdz24\vdss\Scripts\python python\tao_ipynb_kiem_chung_4.py
   ```
   App chạy ở http://localhost:8501 và chỉ đọc `results/cum6/dss_khach.csv`. Notebook cần SQL Server `.\SQLEXPRESS` có CompanyX_DW (ODBC Driver 18).
4. **SQL Server trên PC:** đã restore `backup/CompanyX_DW_after_C3A_20261101.bak` vào `.\SQLEXPRESS`, `VERIFY_STATE` khớp, đã chạy `4_Cum1b`, `CUM5_01..04`, `CUM6_01..04`. Script ghi vào schema analytics cần `SET QUOTED_IDENTIFIER ON` (đã có trong file), với sqlcmd thêm cờ `-I`.
5. **Quy ước:** chỉ một máy huấn luyện và ghi điểm vào kho. Bộ điểm chuẩn là các file SQL trong `results/cum5`.

## 6. Số liệu chính (đã đối chiếu trên Doc ngày 04/11)
| Đại lượng | Giá trị |
|---|---|
| ETL lần chạy cuối | 11 bước, SUCCESS. 19.820 bản ghi khách trích ra, 18.484 khách cá nhân, 1.336 ngoài phạm vi. Staging 31.465 đơn, 121.317 dòng. Kho 27.382 đơn, 59.795 dòng |
| Kiểm tra chất lượng | 44/44 phép sau ETL (7 nhóm, Bảng 4.3), 21/21 phép Customer Snapshot. 6 đơn và 75 dòng chi tiết ngoài phạm vi trong `etl.RejectedRow`. SubTotal 29.052.549,9450, TotalDue 32.103.068,4755 khớp nguồn |
| Khách chấm điểm (08/07/2014) | 18.360 |
| Khách rủi ro Cao | 4.592, tức 25,0% (A 1.285, B 646, C 2.661) |
| Khách có cờ lệch giữa hai mô hình | 2.560 (13,9%) |
| Naive Bayes, trung bình 4 fold (Bảng 4.7) | ROC-AUC 0,720, Brier 0,125, Z 291.883 USD. MLP 0,751 nhưng Z thấp hơn ở 4/4 mốc (chênh 3.504 USD). Recency đảo chiều 0,717, Brier 0,269 |
| Fold cuối 01/03/2014 (Bảng 4.15–4.16) | ROC-AUC 0,7207 so với Recency 0,7191. Brier 0,1176 so với 0,1480. Precision@4.000 89,33%. Z theo p·v 289.245,54 USD, chỉ theo v 254.292,63 USD (+13,7%), trần 339.886,26 USD. Ở RiskLevel Cao: precision 0,898 so với nền 0,820, sensitivity 0,274 |
| Nhãn 90 so với 180 ngày | 26,2% khách y = 1 mua lại trong ngày 90–180. Trừ nhóm này Z cơ sở còn 205.555 USD (r hoà vốn 1,63%) |
| Kịch bản cơ sở | 4.000 khách, Z 292.595 USD, r hoà vốn 1,20%, r để Z đạt 100.000 USD là 4,21%. Mô phỏng 10.000 lần: Z trung bình 290.490 USD, xác suất lỗ 1,7% |
| Theo kênh | 6.124 khách (R3 983, R5 5.141, R4 0 khi ngân sách dưới khoảng 61.213 USD), chi 39.998 USD, Z 256.502 USD (+6,9% so với bỏ qua chi phí kênh) |
| Apriori, dự báo | 164 luật, 26 luật dùng làm gợi ý. MAPE tháng 4–5/2014: 8,2% số đơn, 15,4% doanh thu |
| Giao diện | Rà soát Nielsen 16 vấn đề, sửa 13. Bảng 4.34 (14 đặc điểm DSS): 4 đầy đủ, 9 một phần, 1 hạn chế |

## 7. Trạng thái Doc tab t.0 (04/11/2026)
- **Chương 3:** xong, khoảng 25.900 chữ.
- **Chương 4:** đủ 4.1–4.5, Bảng 4.1–4.34, Hình 4.1–4.29.
  - Ngày 04/11 bỏ thử nghiệm người dùng: ở 4.4.4 thay đoạn "Bước hai…", chú thích bảng thử nghiệm và ô trống bằng một câu nêu giới hạn. Bảng 14 đặc điểm DSS đổi số từ 4.35 thành 4.34, dòng 8 ghi "chưa thử nghiệm với người dùng".
  - Hình 4.25–4.29 là 5 màn hình app. Hình 4.22 và Hình 4.7 lấy từ notebook kiểm chứng.
- **Chương 5:** xong ngày 04/11, khoảng 3.390 từ. Mục 5.1 sáu chiều chất lượng dữ liệu (Bảng 5.1), 5.2 Machine Learning, 5.3 DSS (Bảng 5.2 câu hỏi Q1–Q4, ba tình huống), 5.4 Bảng 5.3 với 9 hạn chế khớp cột "Giới hạn" ở Bảng 3.0.
  - Ba bảng mỗi bảng nằm trọn một trang nhờ thuộc tính "Thêm ngắt trang trước" ở chú thích Bảng 5.1, tiêu đề 5.3.1 và chú thích Bảng 5.3. Hai đoạn bàn luận của 5.1 đã đưa lên trước Bảng 5.1.
  - Chữ trên Doc khớp từng từ với phần A của `docs/DRAFT_CHUONG_5.md`.
- **Chương 6:** mới có dàn ý (6.1 Tổng kết, 6.2 Đóng góp của đề tài, 6.3 Định hướng phát triển).
- **Phiên bản đã đặt tên ngày 04/11:** "Truoc khi dan Chuong 5 (04/11)", "Truoc khi sua Bang 5.3 (04/11)", "Truoc khi dan trang Chuong 5 (04/11)", "Truoc khi bo thu nghiem nguoi dung (04/11)".

## 8. Việc còn lại (theo thứ tự nên làm)
1. **Bảng % đóng góp của từng thành viên** (môn bắt buộc, slide 12–13). Phần trăm do nhóm thống nhất, **không tự điền**. Hỏi Bảo số liệu và chỗ đặt.
2. **Khai báo dùng công cụ AI** (slide 15): ghi tên công cụ (Claude, Gemini, Gemini Notebook/NotebookLM) và dùng vào việc gì, đặt trong tài liệu tham khảo hoặc chú thích. Hỏi Bảo câu chữ trước khi dán.
3. **Chương 6 (kết luận):** theo khung chương Kết luận của báo cáo mẫu (mục 10) nhưng có số thật.
   - 6.1: danh sách kết quả, mỗi mục một thành phần (kho và ETL, mô hình, DSS, giao diện), gắn với Q1–Q4.
   - 6.2: khoảng 3 ý.
   - 6.3: lấy từ Bảng 5.3 (CRM, nhãn 180 ngày, đo r bằng chiến dịch có nhóm đối chứng, SCD Type 2…), không thêm hướng không liên quan.
   - Làm theo quy trình ở mục 2.1: nháp vào `docs/DRAFT_CHUONG_6.md`, phản biện, tự kiểm, hỏi Bảo rồi mới dán.
4. **Hình còn thiếu** (so với báo cáo mẫu và slide khai phá dữ liệu):
   - Sơ đồ luồng ETL 11 bước: nguồn → staging → kiểm tra và loại (RejectedRow) → Dim → Fact → nhật ký RunLog/StepLog. Chương 3 và 4 đều chưa có.
   - Biểu đồ khám phá dữ liệu: histogram hoặc boxplot của Recency, Frequency, Monetary và ma trận tương quan. Dữ liệu ở `results/cum5/customer_risk_score_20140301.csv` (mốc 01/03/2014) và `results/cum6/dss_khach.csv` (mốc 08/07/2014).
   - Biểu đồ hồ sơ năm nhóm K-means (từ `dss_khach.csv`, cột `Nhom`).
   - Tuỳ chọn: biểu đồ dự báo theo tháng (`results/cum6/chuoi_thang.csv`) và biểu đồ support–confidence của luật kết hợp (`results/cum6/bang_4_4_luat_ket_hop.csv`).
5. **Tuỳ chọn, viết theo bước như báo cáo mẫu:** bảng "Bước 1–11" của ETL ở 4.2.2 (tên bước, đầu vào, xử lý, số dòng theo `etl.StepLog`).
6. **Cần nhóm đồng ý vì đụng comment có sẵn:**
   - Khối "Nguồn tham khảo cho 4.2–4.3.2" (comment [bt]) có chữ "Bài giảng Lecture 4". Các số [1]–[4] không được trích ở đâu trong bài, nên nên bỏ cả khối.
   - Các dòng tiêu đề nháp cũ của 4.3.3–4.3.5 (comment bu–ce) và comment hướng dẫn cũ ở 4.4, 4.5 (cf–ck).
7. **Kiểu tiêu đề Chương 4:** 4.1.1–4.1.4 và 4.2.1 đang là chữ đậm thường (chưa lên mục lục). 4.2.3, 4.3.3–4.3.5, 4.4.1–4.4.4 đang là Heading 3, đúng ra là Heading 4 (4.4.1–4.4.4 còn cỡ 13pt).
8. **Bảng bị tách trang ở Chương 4** (ví dụ Bảng 4.13, 4.14, 4.17): xử lý ở lần dàn trang cuối. Nếu Chương 3–4 dài ngắn đi thì xem lại khoảng trắng trước Bảng 5.1, mục 5.3.1 và Bảng 5.3.
9. **Rút gọn Chương 3** (khoảng 25.900 chữ). Bảo chưa quyết.
10. **Slide và kịch bản demo khoảng 10 phút.** Kịch bản demo đã có ở mục 4.5.
11. **Một trang câu hỏi vấn đáp:** vì sao Naive Bayes chứ không phải cây, vì sao cây không tách theo Frequency, vì sao phân vị trong từng hạng ABC, vì sao accuracy chỉ 0,379 ở ngưỡng DSS, vì sao nhãn 90 ngày, Z là gì, vì sao ROC-AUC chỉ ngang Recency mà vẫn dùng mô hình.
12. **Báo cáo LaTeX** (`latex/`): đang là bản chính. Chương 1–4 xong, bìa đủ năm thành viên. Còn chương 5–8, bảng % đóng góp, khai báo dùng AI, danh mục tài liệu tham khảo.

## 9. Cách thao tác Google Doc đã kiểm chứng (Claude in Chrome)
- **Đọc Doc:** chạy `fetch` link xuất HTML (mục 1.1) với `credentials:'include'` trong tab Doc, rồi giải mã thực thể:
  ```js
  const dec = (h) => { const acc={acute:'\u0301',grave:'\u0300',circ:'\u0302',tilde:'\u0303',uml:'\u0308'};
    return h.replace(/<style[\s\S]*?<\/style>/g,'').replace(/<br[^>]*>/g,'\n').replace(/<\/p>|<\/h\d>|<\/li>|<\/tr>/g,'\n')
     .replace(/<\/td>/g,' | ').replace(/<[^>]+>/g,'').replace(/&#(\d+);/g,(m,d)=>String.fromCharCode(+d))
     .replace(/&([a-zA-Z])(acute|grave|circ|tilde|uml);/g,(m,l,a)=>(l+acc[a]).normalize('NFC'))
     .replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&middot;/g,'·').replace(/&times;/g,'×').replace(/&[a-z]+;/g,'?'); };
  ```
  Đếm comment bằng `id="cmnt\d+"`, đếm ảnh bằng `<img`. Phần comment nằm sau dòng `[a]` đầu tiên. Kết quả công cụ bị chặn nếu chứa `= & ?`, nên thay các ký tự này trước khi in.
- **Dán nội dung mới:** viết nháp markdown → sinh HTML (script `tao_html_*.py` đã xoá, xem lịch sử git) → chạy `python3 -m http.server 8766 --bind 127.0.0.1` trong `results/doc` → mở trang trong tab mới, chọn hết (hoặc chọn riêng một bảng bằng `Range.selectNode`), cmd+C → trong Doc đặt con trỏ ở một dòng trống kiểu "Văn bản thường", cmd+V.
  - Sau khi dán: xoá dòng trống thừa trước và sau bảng. Nếu đoạn mới nhận kiểu căn giữa thì cmd+shift+J. Nếu ô bảng nhận giãn cách 11pt thì chọn cả bảng (click ô đầu, shift+click ô cuối) rồi Định dạng → Giãn cách dòng và đoạn → Xoá dấu cách trước đoạn, rồi Xoá dấu cách sau đoạn.
- **Xoá một khối đoạn:** Tìm và thay thế để tới đoạn đầu → đóng hộp thoại bằng nút X (giữ vùng chọn) → Home → alt+shift+Down n lần → chụp màn hình kiểm vùng chọn → BackSpace.
- **Độ rộng cột:** Định dạng → Bảng → Tuỳ chọn cho bảng → Cột. Ô "Chiều rộng cột" chỉ nhận khi click vào ô theo ref (tìm bằng `find`), cmd+A, gõ số, Enter. Bấm toạ độ ba lần không ăn. Tổng bề rộng trang là 15,92 cm.
- **Ngắt trang:** Định dạng → Giãn cách dòng và đoạn → "Thêm ngắt trang trước" hoặc "Giữ với đoạn tiếp theo". Xem bố cục bằng khung 50% (ô zoom trên thanh công cụ), sau đó trả về 100%.
- **Xoá bảng:** đặt con trỏ trong bảng → Định dạng → Bảng → Xoá bảng.
- Cửa sổ kiểm tra chính tả bật lên thì bấm Esc. Hoàn tác bằng menu Chỉnh sửa → Hoàn tác. Kéo viền cột bằng chuột dễ làm hỏng bảng, không dùng.
- **Notebook và Gemini:** gửi câu hỏi thành một đoạn liền (gõ có xuống dòng sẽ gửi sớm), đọc câu trả lời qua `document.body.innerText` (Notebook) hoặc phần tử `model-response` cuối (Gemini).

## 10. Báo cáo mẫu `latex_mau/` (chỉ trên máy) và cách áp dụng
- Báo cáo LaTeX của một nhóm Bách Khoa khác, đề tài kho dữ liệu, ETL bằng Pentaho và học máy dự báo độ an toàn nguồn nước. Khoảng 18.800 từ, không có file PDF.
- Thứ tự chương: Đóng góp (bảng thành viên) → Giới thiệu đề tài → Cơ sở lý thuyết (khoảng 9.000 từ) → Tiền xử lý và EDA (9 biểu đồ) → ETL Pentaho viết theo "Bước 1–8", mỗi bước một câu mục đích, một bảng cấu hình, một câu kết quả → Mô hình dự đoán → Giao diện web → Kết luận và hướng phát triển.
- **Cách nhóm dùng mẫu:** giữ khung chương hiện tại (Chương 3 thiết kế, 4 triển khai, 5 đánh giá), vì khung này khớp thang điểm của thầy và đã có 89 comment. Chỉ học cách viết theo bước trong từng mục và bổ sung các phần mẫu có mà nhóm thiếu (bảng đóng góp, hình EDA, sơ đồ ETL, khung chương Kết luận).
- Nội dung khai phá dữ liệu nhóm đã làm đủ cả bốn loại demo của slide khai phá dữ liệu (phân lớp churn, gom cụm, giỏ hàng, hồi quy). Bảo **không cần** viết thêm chương lý thuyết khai phá dữ liệu riêng trên Doc (04/11).

## 11. Quyết định quan trọng đã chốt
- Naive Bayes là mô hình chấm điểm, cây Gini là mô hình đối chứng sinh luật, MLP chỉ để so sánh. Lý do: Z cao hơn ở 4/4 mốc, xác suất tốt hơn, dễ đọc, còn MLP không ổn định theo hạt giống.
- RiskLevel tính trong từng hạng ABC. Nếu tính chung, toàn bộ khách Cao rơi vào hạng C, ma trận Rủi ro × Giá trị mất tác dụng và R3 không chọn được ai.
- Giữ nhãn 90 ngày. Nhãn 180 ngày không kiểm định được theo thời gian với dữ liệu kết thúc 30/06/2014.
- Bốn bảng bổ sung đặt cuối 4.3.2 để không phải đánh số lại Bảng 4.4–4.10.
- Nhóm Customer Snapshot và RFM của Bảng 3.7 được kiểm riêng (21 phép), 44 phép sau ETL dùng nhóm bản ghi bất thường ở vị trí đó.
- Không thử nghiệm người dùng (04/11). Không viết chương lý thuyết khai phá dữ liệu riêng trên Doc (04/11).
