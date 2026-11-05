# HƯỚNG DẪN CỤM 6 – DSS: phân nhóm, kho quy tắc, mô hình quyết định, giao diện và đánh giá khả dụng (mục 4.4, 4.5)
> File này SINH TỰ ĐỘNG bởi `python/tao_huong_dan.py` từ số liệu đã chạy. Không sửa tay, số bảng và số hình lấy từ `python/so_bang_hinh.py`.

Trạng thái: mọi tính toán đã chạy xong, giao diện 5 màn hình đã chạy được và đã qua một vòng rà soát nội bộ theo 10 nguyên tắc Nielsen. Việc còn lại là ghi vào kho trên máy Windows, chụp hình, thử giao diện với 5 người dùng và viết chữ. Làm sau cụm 5.

## 0. Điều kiện
1. Đã xong cụm 5 (CustomerRiskScore có 18.360 dòng).
2. Đã chạy `sql/4_Cum1b_Schema_DSS_DE_XUAT.sql` một lần (Bước 2 của gói bàn giao). Kết quả có `CLUSTER_1B_OK`, g toàn kho = 4115.
3. Muốn chạy lại cụm 6 từ đầu: `sql/RESET_DSS.sql` (không chạm điểm rủi ro).

## 1. Ghi vào kho (SSMS, CompanyX_DW, theo thứ tự)
| Bước | File | Kết quả mong đợi |
|---|---|---|
| 1.1 | `results/cum6/CUM6_01_ModelRegistry_CareRule.sql` | Đăng ký `KMEANS_E20140708_v1` (CLUSTERING) và 9 quy tắc R1–R9, R1 và R9 tạm tắt (chưa có dữ liệu CRM). `CUM6_01_OK` |
| 1.2 | `CUM6_02_CustomerSegment.sql` | 18.360 khách có hạng ABC và nhóm N1–N5. `CUM6_02_OK` |
| 1.3 | `CUM6_03_CareRecommendation.sql` | Kịch bản cơ sở theo kênh: 6.124 khuyến nghị, R3 983 và R5 5.141, chi 39.998 USD, Z = 256.502 USD. `CUM6_03_OK` |
| 1.4 | `CUM6_04_Verify_READ_ONLY.sql` | 18.360 khách / 5 nhóm — bảng nhóm × RiskScore — 9 quy tắc, 7 đang bật — 1 kịch bản (6.124 khách, Z 256.502) — hồ sơ khách 19785 |

## 2. Giao diện DSS
Bấm đúp `Mo_giao_dien_DSS.bat` (Windows) hoặc `Mo_giao_dien_DSS.command` (Mac) trong `0_BAT_DAU_O_DAY/Buoc_5_Mo_giao_dien_DSS`. Trình duyệt mở http://localhost:8501, mặc định vào tab "Hướng dẫn sử dụng". Thanh bên chọn màn hình 1–5 và vai trò (Bảng 3.31).

## 3. Hình cần chụp
| Hình | Nội dung | Mục |
|---|---|---|
| Hình 4.21 | `results/cum6/hinh_4_4_chon_k.png` (Elbow và Silhouette) | 4.4.1 |
| Hình 4.22 | Kết quả bước 1.4 trong SSMS (bảng nhóm và kịch bản) | 4.4.2 |
| Hình 4.23 | `results/cum6/hinh_4_4_do_nhay.png` (độ nhạy ±20%) | 4.4.3 |
| Hình 4.24 | `results/cum6/hinh_4_4_mo_phong.png` (phân phối Z khi r ~ Beta) | 4.4.3 |
| Hình 4.25 → Hình 4.29 | Chụp màn hình app, mỗi màn hình một hình thấy bộ lọc và kết quả chính (Bảng 3.32). Màn hình 3 chụp ở kỹ thuật "Chi phí và tỷ lệ thành công theo kênh". Màn hình 4 chụp sau khi bớt một khách có ghi lý do (thấy bảng nhật ký) | 4.4.4 |

## 4. Bảng cần dán
| Bảng | Tên | File | Mục |
|---|---|---|---|
| Bảng 4.19 | Phân hạng ABC | `results/cum6/bang_4_4_abc.csv` → gói bàn giao `Bang_4_19_Phan_hang_ABC.csv` | 4.4.1 |
| Bảng 4.20 | Độ nhạy theo ngưỡng ABC: 80%/95% so với 70%/90% | `results/cum6b/bang_4_4_abc_do_nhay.csv` → gói bàn giao `Bang_4_20_ABC_do_nhay_nguong.csv` | 4.4.1 |
| Bảng 4.21 | Chọn số cụm k: WCSS và Silhouette | `results/cum6/bang_4_4_chon_k.csv` → gói bàn giao `Bang_4_21_Chon_so_cum_k.csv` | 4.4.1 |
| Bảng 4.22 | Hồ sơ năm nhóm khách hàng | `results/cum6/bang_4_4_ho_so_nhom.csv` → gói bàn giao `Bang_4_22_Ho_so_5_nhom.csv` | 4.4.1 |
| Bảng 4.23 | Ma trận Rủi ro × Giá trị | `results/cum6/bang_4_4_ma_tran_rui_ro_gia_tri.csv` → gói bàn giao `Bang_4_23_Ma_tran_rui_ro_gia_tri.csv` | 4.4.1 |
| Bảng 4.24 | Cơ cấu sản phẩm theo nhóm | `results/cum6/bang_4_4_co_cau_san_pham.csv` → gói bàn giao `Bang_4_24_Co_cau_san_pham_theo_nhom.csv` | 4.4.2 |
| Bảng 4.25 | Luật kết hợp khai phá bằng Apriori dùng được làm gợi ý sản phẩm | `results/cum6b/bang_4_4_apriori_luat_goi_y.csv` → gói bàn giao `Bang_4_25_Apriori_luat_goi_y.csv` | 4.4.2 |
| Bảng 4.26 | Năm luật ứng viên Bảng 3.29 và vị trí trong kết quả Apriori | `results/cum6b/bang_4_4_apriori_doi_chieu.csv` → gói bàn giao `Bang_4_26_Luat_ung_vien_trong_Apriori.csv` | 4.4.2 |
| Bảng 4.27 | Các đại lượng của mô hình giá trị kỳ vọng đo từ dữ liệu | `results/cum6b/bang_4_4_tham_so_do_duoc.csv` → gói bàn giao `Bang_4_27_Tham_so_do_tu_du_lieu.csv` | 4.4.3 |
| Bảng 4.28 | Phân tích what-if | `results/cum6/bang_4_4_what_if.csv` → gói bàn giao `Bang_4_28_What_if.csv` | 4.4.3 |
| Bảng 4.29 | Độ nhạy ±20% | `results/cum6/bang_4_4_do_nhay.csv` → gói bàn giao `Bang_4_29_Do_nhay.csv` | 4.4.3 |
| Bảng 4.30 | Z theo ngân sách và tỷ lệ chăm sóc thành công | `results/cum6/bang_4_4_payoff.csv` → gói bàn giao `Bang_4_30_Z_theo_ngan_sach_va_r.csv` | 4.4.3 |
| Bảng 4.31 | Danh sách chăm sóc theo kênh | `results/cum6/bang_4_4_theo_kenh.csv` → gói bàn giao `Bang_4_31_Theo_kenh.csv` | 4.4.3 |
| Bảng 4.32 | Dự báo hồi quy tuyến tính số đơn và doanh thu | `results/cum6/bang_4_4_du_bao.csv` → gói bàn giao `Bang_4_32_Du_bao.csv` | 4.4.3 |
| Bảng 4.33 | Rà soát nội bộ giao diện theo 10 nguyên tắc Nielsen | `results/kha_dung/bang_danh_gia_heuristic.csv` → gói bàn giao `Bang_4_33_Ra_soat_noi_bo_Nielsen.csv` | 4.4.4 |
| Bảng 4.34 | Đối chiếu bản triển khai với 14 đặc điểm DSS | Tự lập từ Bảng 3.33 (mục 5 bên dưới) | 4.5 |

## 5. Dàn ý và số liệu
### 4.4.1. Phân nhóm khách hàng
- **ABC (Bảng 4.19).** Hạng A 5.137 khách (28,0%) giữ 80% Monetary, B 2.581 (14,1%) giữ 15%, C 10.642 (58,0%) giữ 5%.
- **Độ nhạy ngưỡng ABC (Bảng 4.20).** Mục 3.5.3 hẹn thử 70% và 90%. Với 70%/90%: A 4.019, B 2.539, C 11.802 khách, 2.278 khách đổi hạng. Khách đủ điều kiện R3 còn 1.499 (so với 1.647), danh sách theo kênh chọn 6.480 khách, Z = 254.700 USD, thấp hơn thiết kế 1.802 USD (−0,7%). Kết luận: quyết định không nhạy với ngưỡng ABC, giữ 80%/95%.
- **K-means.** Hopkins H = 0,004 (có cấu trúc cụm). Elbow gãy ở k = 3–5, Silhouette k = 5 là 0,466 (Bảng 4.21, Hình 4.21). Chọn k = 5 vì đủ ít để diễn giải. Ổn định: ARI = 1,0 với 3 khởi tạo khác, ARI = 0,995 với Ward.
- **Hồ sơ năm nhóm (Bảng 4.22).** N1 4.926 khách (26,8%), F trung bình 2,2, M trung vị 4.910 USD, giữ 75,6% giá trị, 4.280 khách hạng A. N2 3.741 (20,4%), mua 1 lần, M 1.298. N3 428 (2,3%), Recency trung vị 918 ngày, M 3.954. N4 1.839 (10,0%), F 2,7 nhưng M 118 (mua lặp phụ kiện). N5 7.426 (40,4%), mua 1 lần, M 44 USD.
- **Mức khớp với mô hình giá trị kỳ vọng (hai cột cuối Bảng 4.22, mục 3.5.3 hẹn).** Tỷ lệ khách có EV > 0 ở kịch bản cơ sở: N1 98,7%, N2 91,6%, N3 62,6%, N4 0,0%, N5 0,0%. Số khách vào danh sách theo kênh: N1 3.964, N2 2.160, N3 0, N4 0, N5 0. N4 và N5 không có khách nào có EV dương nên bị loại toàn bộ theo R2, vì giá trị một lần mua quá nhỏ so với chi phí chăm sóc. N3 có 62,6% khách EV dương ở kịch bản chi phí chung, và khi tính theo kênh R4 (15 USD, tỷ lệ thành công 12%) vẫn còn 268 khách EV dương, nhưng không khách nào được chọn vì lợi trên mỗi USD chi phí tối đa chỉ 0,40, thấp hơn mức cắt 2,83 của danh sách khi ngân sách đã dùng hết. Danh sách cuối chỉ gồm N1 và N2, đúng ý đồ của mô hình giá trị kỳ vọng: ngân sách dồn vào khách có giá trị.
- **Ma trận Rủi ro × Giá trị (Bảng 4.23).** Cao: A 1.285, B 646, C 2.661. Giải thích vì sao RiskLevel tính trong từng hạng: xác suất không mua lại giảm theo chi tiêu, nếu tính chung thì khách Cao rơi hết vào hạng C, ma trận mất tác dụng và R3 không chọn được ai. Khách Cao ở mọi hạng đều có RiskScore từ 0,886 trở lên.

### 4.4.2. Kho quy tắc và tri thức
- **Cơ cấu sản phẩm (Bảng 4.24).** N1, N2, N3 gần như 100% xe đạp, N4 và N5 không có xe đạp (73–77% phụ kiện).
- **Khai phá luật bằng Apriori (Bảng 4.25, Bảng 4.26).** Mục 3.5.5 hẹn chọn hai ngưỡng ở Chương 4. Giỏ là tập danh mục con mỗi khách đã mua trước mốc chấm điểm (18.360 khách, 17 danh mục con). Chọn giỏ theo khách thay vì theo từng đơn vì mục đích là gợi ý sản phẩm khách **chưa từng mua** trong nội dung chăm sóc, không phải gợi ý mua kèm tại quầy. Nói rõ điểm này vì định nghĩa support trong tài liệu môn học tính theo giao dịch. Chọn min support 1% (khoảng 184 khách, đủ để luật có ý nghĩa thống kê) và min confidence 20% (cứ 5 khách mua vế trái có 1 khách mua vế phải, đủ để làm gợi ý), lift > 1. Apriori tìm được 17 tập 1 mục , 55 tập 2 mục , 48 tập 3 mục , 6 tập 4 mục phổ biến và 164 luật. Các luật lift cao nhất là giữa các dòng xe đạp (khách đã mua nhiều loại xe), không dùng làm gợi ý vì giá trị cao. Lọc luật một mục mỗi vế với vế phải là phụ kiện hoặc quần áo còn 26 luật. Năm luật ứng viên của Bảng 3.29 đều có trong kết quả, xếp hạng 10, 12, 4, 9, 3 trong 26 luật gợi ý. Đối chiếu theo từng đơn (27.382 đơn, cột "theo đơn" của Bảng 4.26): cả năm luật vẫn có lift lớn hơn 1 (1,48 đến 2,63), tức khách còn hay mua kèm ngay trong một lần thanh toán. Luật R7 có confidence theo đơn dưới 20% nên chỉ mạnh khi xét theo khách. Luật mạnh chưa dùng: Shorts → Caps (lift 2,15), Shorts → Jerseys (lift 2,13), có thể bổ sung vào kho quy tắc ở phiên bản sau.
- **Kho quy tắc.** 9 quy tắc nạp vào analytics.CareRule, R1 và R9 tắt vì chưa có nhật ký CRM (Hình 4.22).

### 4.4.3. Phân tích mô hình
- **Các đại lượng đo từ dữ liệu (Bảng 4.27).** Đây là các số Chương 3 hẹn đo ở Chương 4 (mục 3.5.1, 3.5.2):
  - g = 0,4115. Theo nhóm: Bikes 0,406, Accessories 0,626, Clothing 0,402. Dùng g theo nhóm làm Z cơ sở đổi −0,9% và 99,7% khách trong danh sách giữ nguyên, nên giữ g chung.
  - Quy mô vấn đề: khách y = 1 chiếm 81,2% số khách và 78,0% tổng Monetary (trung bình 19 mốc), không thể chăm sóc tất cả.
  - Khách quay lại trong 90 ngày đặt trung bình 1,12 đơn (93,5% chỉ một đơn), nên tính v theo một lần mua là xấp xỉ hợp lý. Giá trị đơn khi quay lại bằng khoảng 0,87 lần AOV trước đó (trung vị), đúng với kịch bản "khách quay lại chi ít hơn" ở 3.5.4.
  - 50,5% khách có v < c/r = 100 USD, chăm sóc riêng không bù được chi phí (trường hợp khách B ở 3.5.2).
  - Khách chưa đến kỳ: 26,2% khách bị gắn y = 1 theo nhãn 90 ngày tự mua lại trong ngày 90–180 (Bảng 4.13). Nếu coi phần lợi ích từ nhóm này là không nhờ chăm sóc, Z cơ sở còn 205.555 USD và r hoà vốn tăng lên 1,63%. Chiến dịch vẫn có lãi kỳ vọng, nhưng nên viết Z cơ sở là cận trên.
- **Kịch bản cơ sở** (r 10%, c 10, B 40.000): Z = 292.595 USD, chọn 4.000 khách, 358 khách giữ lại kỳ vọng, 8.554 khách có EV > 0.
- **What-if (Bảng 4.28).** r = 5% → Z 126.297, r = 20% → 625.189, c = 5 → 424.359 (8.000 khách), c = 20 → 152.066, B = 20.000 → 172.066, B = 60.000 → 359.388, B = 100.000 → 386.235 (chỉ dùng 85.540 vì hết khách EV > 0).
- **Độ nhạy ±20% (Bảng 4.29, Hình 4.23).** r và g cho ±22,7% vì nhân với nhau trong doanh thu. c cho −13,9% / +17,2%, B cho +11,5% / −14,1%.
- **Tìm mục tiêu.** r* hoà vốn 1,20%, r* để Z = 100.000 USD là 4,21%.
- **Z theo B × r (Bảng 4.30).** Lạc quan và giá trị kỳ vọng chọn B = 100.000, bi quan chọn B = 40.000.
- **Mô phỏng r ~ Beta (Hình 4.24).** r trung bình 9,9%, P5 2,1%, P95 21,7%. Z trung bình 290.490, P5 29.774, P95 683.192, P(Z < 0) = 1,7%. Kiểm định tại r = 10% trùng kịch bản cơ sở.
- **Theo kênh (Bảng 4.31).** R2 loại 9.588 khách, chọn 6.124 khách (R3 983, R5 5.141, R4 không ai vì lợi trên mỗi USD chi phí của khách N3 tối đa 0,40, dưới mức cắt 2,83 của danh sách), chi 39.998 USD, Z = 256.502 USD, cao hơn 6,9% so với xếp theo p·v bỏ qua chi phí kênh (239.997 USD). Quy hoạch nguyên và tham lam cho cùng lời giải. Cách chọn đúng khi ngân sách có hạn là xếp theo lợi trên mỗi USD chi phí, không phải chọn mọi khách có EV dương. Kênh R4 (nhóm N3) chỉ bắt đầu có khách khi ngân sách từ khoảng 61.213 USD.
- **Dự báo (Bảng 4.32).** Hồi quy tuyến tính dự báo số đơn tháng 4–5/2014 sai 8,2% (mức nền cùng tháng năm trước 84,9%), doanh thu sai 15,4% so với 70,1%. Tháng 6/2014 lệch mạnh vì tháng này không có đơn xe đạp, đúng vai trò phát hiện bất thường.

### 4.4.4. Giao diện và đánh giá khả dụng
- **Mô tả 5 màn hình** theo Bảng 3.32 (Hình 4.25 → Hình 4.29): nhãn loại thông tin (dữ liệu thực tế, dự đoán, theo giả định), phân quyền theo vai trò, tab Hướng dẫn sử dụng, điều chỉnh thủ công bắt buộc có lý do (lý do và nguồn chọn được ghi vào file xuất), xuất CSV.
- **Đánh giá khả dụng.** Mục 3.5.7 hẹn đánh giá khả dụng. Khả dụng gồm ba mặt: hiệu quả, hiệu suất và mức độ hài lòng của người dùng khi dùng hệ thống. Làm hai bước:
  - Rà soát nội bộ theo 10 nguyên tắc của Nielsen trước khi thử nghiệm (Bảng 4.33). Gọi đúng là rà soát nội bộ vì do chính nhóm làm, không phải chuyên gia độc lập. Tìm 16 vấn đề, đã sửa 13, còn 3 vấn đề mức nhẹ hoặc thuộc giới hạn phạm vi. Ba vấn đề nặng nhất đã sửa: mô tả nhóm dùng tên biến tiếng Anh, xuất danh sách khi chưa có lý do điều chỉnh, và tên nhóm bị cắt trong bộ lọc.
  - Không thử nghiệm với người dùng (quyết định ngày 04/11/2026). Ghi là giới hạn, nêu lại ở mục 5.4.
- **Giới hạn.** R1, R9 và nhóm đối chứng cần dữ liệu CRM. Đề xuất quy tắc mới ở màn hình 5 mới là bản trình diễn, chưa lưu vào kho.

### 4.5. Đối chiếu 14 đặc điểm DSS (Bảng 4.34)
Lấy Bảng 3.33, thêm cột "mức đáp ứng của bản triển khai" và "bằng chứng" (số bảng, số hình ở 4.4). Đặc điểm 1, 10, 12 có bằng chứng ở 4.4.3–4.4.4. Đặc điểm "dễ sử dụng và tương tác" (đặc điểm số 8 trong danh sách đặc điểm DSS) có bằng chứng ở Bảng 4.33, không có thử nghiệm người dùng. Các đặc điểm cần CRM (R1, R9) ở mức một phần.

## 6. Trên Doc
- Mục 4.4 hiện là 1 câu, 4.5 là 4 gạch đầu dòng. Comment [ce]–[ch] gắn ở dòng tiêu đề 4.4, comment [ci] gắn ở dòng tiêu đề 4.5. Viết mới toàn bộ phần thân, **không sửa chữ của dòng tiêu đề**.
- Comment cũ có thể còn số cũ (8.772 khuyến nghị, Z 210.432, số bảng 4.14–4.24). Theo file này.
- Không dùng dấu chấm phẩy, không viết "bài giảng". Số kiểu Việt. Chú thích nghiêng canh giữa.
