# HƯỚNG DẪN CỤM 5 – Đánh giá, giải thích và ghi kết quả mô hình vào kho (mục 4.3.3 → 4.3.5)
> File này SINH TỰ ĐỘNG bởi `python/tao_huong_dan.py` từ số liệu đã chạy. Không sửa tay, số bảng và số hình lấy từ `python/so_bang_hinh.py`.

Người thực hiện: bạn phụ trách Chương 4. Máy Windows có SSMS và CompanyX_DW đã chạy đủ cụm 0 → 3A.
Mọi thứ cần chạy đã sinh sẵn, **không cần Python**: mở 4 file SQL trong SSMS, chạy, chụp hình, dán bảng. Phần chữ có dàn ý và số liệu sẵn, chỉ cần viết thành đoạn.

## 0. Điều kiện trước khi bắt đầu (5 phút)
1. Chạy `sql/VERIFY_STATE.sql`. Mọi dòng phải khớp cột MongDoi (196.985 dòng Snapshot, hash `0x044F3D49…`). Khớp thì máy bạn và máy Bảo cùng dữ liệu, kết quả cụm 5 sẽ giống hệt.
2. Bảng `analytics.CustomerRiskScore` phải đang **trống** (dòng CustomerRiskScore trong VERIFY_STATE = 0). Nếu không trống, chạy `sql/RESET_SCORES.sql`.
3. Sau bước 1.3 bên dưới, Snapshot bị khoá (C3_01 từ chối tính lại). Đây là chủ ý của thiết kế. Muốn tính lại Snapshot: `RESET_SCORES.sql` → C3_02 → chạy lại cụm 5.

## 1. Ghi kết quả vào kho (10 phút)
Mở từng file trong `results/cum5/` bằng SSMS, database CompanyX_DW, Execute (F5), **đúng thứ tự**:

| Bước | File | Kết quả mong đợi (phải thấy đúng dòng PRINT cuối) |
|---|---|---|
| 1.1 | `CUM5_01_ModelRegistry.sql` | 3 dòng: NB_T20140301_v1 (SCORING), TREE_T20140301_v1 (TREE), MLP_T20140301_v1 (COMPARISON). Cột ROCAUC là **trung bình bốn fold** (Naive Bayes 0,7199, Brier 0,1252), khác số 0,721 của riêng fold cuối dùng ở 4.3.3. Cột DecisionThreshold = 0,9754 chỉ là RiskScore tại phân vị 75 của toàn bộ khách, để tham khảo, **không phải ngưỡng Cao** (ngưỡng Cao tính trong từng hạng ABC). `CUM5_01_OK` |
| 1.2 | `CUM5_02_ModelTreeLeaf.sql` | 11 lá, LeafCount từ 420 đến 6.054. `CUM5_02_OK: 11 lá` |
| 1.3 | `CUM5_03_CustomerRiskScore.sql` (4,7 MB, khoảng 10 giây) | Thấp 13.768, Cao 4.592 (25,0%). `CUM5_03_OK: 18360 khách` |
| 1.4 | `CUM5_04_Verify_READ_ONLY.sql` | 5 bảng: 18.360 / 4.592 / 25,0 / 2.560 — 18.360 / 18.360 — 3 mô hình — 3 khách minh hoạ (12201, 26339, 26774) — 11 lá |

Nếu file 01 hoặc 03 báo lỗi 55001 hoặc 55002 là do đã ghi rồi: chạy `RESET_SCORES.sql` rồi làm lại từ 1.1.

## 2. Hình cần chụp trong SSMS (chỉ khung kết quả, không chụp cả màn hình)
| Hình | Chụp gì | Đặt ở mục |
|---|---|---|
| Hình 4.17 | Bước 1.4, bảng thứ tư: ba khách 12201, 26339, 26774 | 4.3.4 |
| Hình 4.18 | Bước 1.1: 3 dòng ModelRegistry và dòng PRINT | 4.3.5 |
| Hình 4.19 | Bước 1.3: bảng RiskLevel 2 dòng và dòng PRINT | 4.3.5 |
| Hình 4.20 | Bước 1.4, hai bảng đầu (18.360 / 4.592 / 2.560 và 18.360 / 18.360) | 4.3.5 |

Số hình đánh theo thứ tự xuất hiện trên Doc: hình ở 4.3.4 đứng trước ba hình ở 4.3.5. Ảnh chèn rồi thu về bề rộng trang, chú thích nghiêng canh giữa như Chương 3.

## 3. Bảng cần dán (CSV đã sinh sẵn)
| Bảng | Tên | File | Mục |
|---|---|---|---|
| Bảng 4.15 | Lớp 1: chỉ số phân lớp của Naive Bayes ở ba ngưỡng và cách luôn dự đoán lớp đa số | `results/cum5/bang_4_3_3a_lop1_ba_nguong.csv` → gói bàn giao `Bang_4_15_Lop_1_ba_nguong.csv` | 4.3.3 |
| Bảng 4.16 | Lớp 2 và Lớp 3: chất lượng điểm và giá trị quyết định của Naive Bayes | `results/cum5/bang_4_3_3b_lop2_lop3.csv` → gói bàn giao `Bang_4_16_Lop_2_va_3.csv` | 4.3.3 |
| Bảng 4.17 | Xác suất có điều kiện P(x | y) của Naive Bayes | `results/cum5/bang_4_3_4_xac_suat_co_dieu_kien_NB.csv` → gói bàn giao `Bang_4_17_Xac_suat_co_dieu_kien_NB.csv` | 4.3.4 |
| Bảng 4.18 | Ba khách minh hoạ | `results/cum5/bang_4_3_4_khach_minh_hoa.csv` → gói bàn giao `Bang_4_18_Ba_khach_minh_hoa.csv` | 4.3.4 |

Số kiểu Việt: 0,837 và 18.360. Cột TopFactors của bảng ba khách dài, có thể bỏ khỏi bảng và nói trong chữ. Không dùng dấu chấm phẩy trong thân bài, không viết "bài giảng".

## 4. Dàn ý và số liệu cho phần chữ
### 4.3.3. Đánh giá và lựa chọn mô hình
- **Mở đầu.** Đánh giá theo ba lớp của Bảng 3.16 trên fold cuối E = 01/03/2014 (mô hình học ở 15/11/2013). Trung bình bốn fold đã trình bày ở 4.3.2.
- **Lớp 1, chỉ số phân lớp (Bảng 4.15).** Đây là các chỉ số có trong nội dung môn học (ma trận nhầm lẫn, accuracy, tỷ lệ lỗi, precision, sensitivity, specificity, F1). Mục 3.4.6 hẹn báo cáo ở cả ngưỡng Youden và ngưỡng phân vị 75, và đối chiếu ngưỡng chọn trên mốc huấn luyện với ngưỡng chọn ngoài mẫu. Bảng có bốn cột:
  - Youden chọn trên mốc huấn luyện (RiskScore ≥ 0,729): cảnh báo 82,2% số khách. Accuracy 0,837, tỷ lệ lỗi 0,163, sensitivity 0,902, specificity 0,541, precision 0,899, F1 0,901.
  - Youden chọn ngoài mẫu (Naive Bayes học ở 01/08/2013, dự đoán mốc 15/11/2013 mà nhãn đã đủ trước 01/03/2014, ngưỡng 0,878): cảnh báo 64,4%, accuracy 0,690, sensitivity 0,704, specificity 0,627. Cân bằng hơn hẳn, xác nhận nhận định của 3.4.6 rằng ngưỡng chọn trên chính mốc huấn luyện là lạc quan và gắn cảnh báo cho phần lớn khách.
  - Phân vị 75 trong từng hạng ABC, tức RiskLevel Cao mà DSS dùng: cảnh báo 25,0%, precision 0,898, specificity 0,858, sensitivity 0,274, accuracy 0,379. Giải thích: DSS chỉ đưa 1/4 khách vào nhóm ưu tiên nên sensitivity và accuracy thấp là chủ ý. Điều quan trọng là precision 0,898 cao hơn tỷ lệ nền 0,820 (lift 1,10): trong 10 khách bị gắn Cao có khoảng 9 khách thật sự không mua lại, và specificity 0,858 cho thấy rất ít khách sẽ mua lại bị làm phiền.
  - Luôn dự đoán y = 1: accuracy 0,820 và F1 0,901, ngang Naive Bayes ở ngưỡng Youden, nhưng specificity bằng 0. Đây là minh hoạ vì sao 3.4.6 không dùng accuracy hay F1 một mình khi lớp y = 1 chiếm đa số.
- **Lớp 2 (Bảng 4.16).** ROC-AUC 0,721 so với Recency đảo chiều 0,719 (điều kiện 1 đạt). Brier 0,118 so với dự đoán hằng số 0,148 (điều kiện 2 đạt). AP lớp không mua lại 0,893, AP lớp mua lại 0,476 (mức nền của lớp này khoảng 0,18), Precision@4000 = 0,893.
- **Lớp 3.** Z theo p·v 289.246 USD so với chỉ theo v 254.293 USD (điều kiện 3 đạt), mức trần biết trước nhãn 339.886 USD. Mô hình thu được khoảng 41% khoảng cách từ "chỉ theo v" lên mức trần.
- **Kết luận chọn.** Nhắc lại 4.3.2: Naive Bayes đạt ba điều kiện ở 4/4 fold và Z cao hơn MLP ở 4/4 mốc. MLP có ROC-AUC trung bình 0,751, cao hơn Naive Bayes 0,720, nhưng Z thấp hơn và thay đổi theo hạt giống khởi tạo, nên chỉ giữ làm mô hình so sánh. Nói rõ điểm này vì người đọc thấy AUC của MLP cao hơn sẽ hỏi.
- **Ngưỡng cảnh báo.** RiskLevel Cao khi RiskPercentile ≥ 75 tính TRONG TỪNG HẠNG ABC (mục 3.4.6, 3.5.3): A 1.285, B 646, C 2.661 khách, tổng 4.592 (25,0%). Vì vậy **không có một ngưỡng RiskScore chung**. RiskScore thấp nhất của khách Cao là 0,935 ở hạng A, 0,886 ở hạng B và 0,986 ở hạng C, đều trên tỷ lệ nền 0,82. Nghĩa là khách Cao ở hạng nào cũng có xác suất không mua lại rất cao, RiskLevel là thứ tự ưu tiên trong hạng còn RiskScore mới là xác suất. Viết câu này để chặn trước câu hỏi "khách hạng A bị gắn Cao với xác suất thấp".
- **Giới hạn.** Ba lớp tính trên fold phát triển nên có thiên lệch lựa chọn (mục 3.4.4).

### 4.3.4. Giải thích dự đoán
- **Tầng 1: bảng xác suất có điều kiện của Naive Bayes (Bảng 4.17).** Tỷ số P(x | y = 1) / P(x | y = 0) lớn hơn 1 làm tăng rủi ro. Recency 180–269 ngày có tỷ số 2,50 (tăng mạnh). Recency 270–539 ngày có tỷ số 0,09 đến 0,10 (giảm mạnh, đây là nhóm mua theo năm sắp đến kỳ). NSub = 1 có tỷ số 0,43 (giảm), NSub = 2 có tỷ số 2,75 (tăng). Tiên nghiệm P(y = 1) = 0,820.
- **Lưu ý khi đọc bảng.** Monetary và BikeBuyer phụ thuộc mạnh (Cramér V 0,92, xem Bảng 4.11 ở 4.3.2), nên Naive Bayes đếm hai lần cùng một thông tin "đã mua xe đắt". Đọc hai dòng này cùng nhau, không cộng dồn.
- **Tầng 2: luật lá của cây đối chứng (TopFactors) và TreeScore.** Đây là mô tả nhóm khách giống nhau, không phải lý do của RiskScore. Giao diện hiển thị luật này thành câu tiếng Việt, ví dụ "lần mua gần nhất cách đây trên 275 ngày, đã là khách được trên 744 ngày".
- **Ba khách minh hoạ (Bảng 4.18, Hình 4.17).**
  - 12201 (Recency 180, 2 đơn, 64 USD, hạng C): RiskScore 0,993, phân vị 100,0, Cao. Cùng lá 1 (89,9% không mua lại), hai mô hình thống nhất.
  - 26339 (Recency 186, 2 đơn, 4.923 USD, hạng A): RiskScore 0,963, Cao, nhưng TreeScore 0,586 nên có cờ lệch và DSS yêu cầu xem xét.
  - 26774 (Recency 508, 1 đơn, 865 USD, hạng C): RiskScore 0,049, phân vị 0,009, Thấp. Lá 8 (420 khách, 18,1% không mua lại, TreeScore 0,249), hai mô hình thống nhất. Đây là khách mua theo năm sắp đến kỳ.
- **Cờ lệch.** 2.560 khách (13,9%) có |TreeScore − RiskScore| > 0,3, tập trung ở lá 8 (1.376 trên 2.727 khách, RiskScore trung bình 0,55 trong khi TreeScore 0,25).
- **Từ giải thích đến hành động.** Mỗi yếu tố dẫn tới một quyết định trong DSS: khách N1 ở mức Cao được liên hệ cá nhân (R3), khách N3 được mời quay lại (R4), còn lại nhận email (R5), và khách có giá trị kỳ vọng không dương bị loại (R2). Khách có cờ lệch hiện ô đỏ "Cần xem xét thêm" ở màn hình 2. Người quản lý hỏi đội bán hàng rồi giữ, thêm hoặc bớt khách ở màn hình 4 kèm lý do, lý do được ghi vào file xuất. Cờ không làm đổi điểm.
- Không dùng feature importance của MLP vì MLP không phải mô hình chấm điểm. Bảng xác suất có điều kiện chính là phần "mức ảnh hưởng" đọc được của Naive Bayes.

### 4.3.5. Tích hợp kết quả ML vào kho
- **Luồng theo Hình 3.7.** Học ở 01/03/2014 → đăng ký ModelRegistry (Hình 4.18, 3 phiên bản, chỉ một mô hình SCORING đang active nhờ chỉ mục UX_ModelRegistry_ActiveRole) → lưu 11 lá vào ModelTreeLeaf → ghi 18.360 dòng CustomerRiskScore (Hình 4.19) → kiểm tra nối Snapshot (Hình 4.20).
- **Cột ghi.** RiskScore, RiskPercentile (phân vị trong hạng ABC, đồng điểm xếp theo Recency giảm dần), RiskLevel (ràng buộc CHECK đúng ngưỡng 75), TreeScore, TreeModelVersion, TopFactors, ScoredAt. Khoá (CustomerID, ScoreDate, ModelVersion) cho phép giữ điểm cũ khi có phiên bản mới.
- **Cách thực hiện.** Python chấm điểm và sinh file SQL (`python/cum5_cham_diem_sinh_sql.py`), chạy trong SSMS. Mọi file có giao dịch và tự dừng khi số dòng lệch. Script Python cũng tự kiểm trước khi sinh file: mỗi khách một dòng, RiskLevel khớp phân vị, mỗi hạng đúng 25% Cao. DSS (mục 4.4) chỉ đọc phiên bản SCORING đang active.
- Sau khi ghi điểm, Snapshot bị khoá để điểm và đặc trưng luôn đi cùng nhau. Muốn tính lại phải xoá điểm trước (`RESET_SCORES.sql`).

## 5. Việc trên Doc
- Các comment [bu]–[cd] gắn ở **dòng tiêu đề** 4.3.3, 4.3.4, 4.3.5, không gắn ở các gạch đầu dòng nháp. Xoá gạch đầu dòng nháp và viết đoạn mới thoải mái, **không sửa chữ của dòng tiêu đề** (sửa sẽ mất comment).
- Comment cũ có thể còn số cũ (mã khách 27068, Hình 4.16–4.19, câu ngưỡng 0,9754). Theo file này, không theo comment cũ.
- Xong thì nhắn Bảo chạy kiểm tra toàn Phần 3 (comment, dấu chấm phẩy, số thứ tự, bố cục trang).

## 6. Kiểm tra bạn đã làm đúng
- Bước 1.4 bảng 1: 18360 / 4592 / 25,0 / 2560. Bảng 2: 18360 / 18360. Khác số là dữ liệu hai máy khác nhau, dừng lại và nhắn Bảo.
- Trên Doc: 4.3.3 có Bảng 4.15 và Bảng 4.16, 4.3.4 có Bảng 4.17, Bảng 4.18 và Hình 4.17, 4.3.5 có Hình 4.18 đến Hình 4.20.
