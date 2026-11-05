# Bản nháp 4.3.2. Huấn luyện và so sánh mô hình (thay toàn bộ 4.3.2 cũ)
Quy ước: không dùng dấu chấm phẩy, không ghi "bài giảng". Nguồn số: `results/cum4/`. Số bảng/hình tạm 4.3.2a…, đánh lại khi dán.

---

### 4.3.2. Huấn luyện và so sánh mô hình

Các mô hình ở Bảng 3.14 được huấn luyện bằng Python và scikit-learn trên bốn fold của Bảng 3.12 theo đúng giao thức mục 3.4.4: học trên mốc T, chấm điểm toàn bộ khách tại mốc E, không gộp mốc, mọi tham số chuẩn hóa và rời rạc hóa tính trên mốc T. Cấu hình cố định trước gồm: Naive Bayes trên năm thuộc tính rời rạc của Bảng 3.10 với hiệu chỉnh Laplace (alpha = 1), cây Gini sâu tối đa 4, tối thiểu 400 khách mỗi lá, m = 50, mạng nơ-ron hai lớp ẩn (32, 16), ReLU, dừng sớm, hạt giống 0, Logistic Regression one-hot với chính quy hóa L2, cùng hai mốc so sánh là dự đoán lớp đa số và quy tắc Recency đảo chiều. Ba mô hình bổ sung ngoài nội dung môn học (Random Forest 300 cây, gradient boosting, kNN với k = 200) chạy cùng giao thức để biết giới hạn của dữ liệu. Giá trị ròng Z tính theo chính sách chọn khách ở mục 3.5.4 với kịch bản cơ sở r = 10%, c = 10 USD, B = 40.000 USD và tỷ lệ lợi nhuận gộp g = 41,15% tính từ giá vốn tại ngày đặt của 59.795 dòng đơn trong phạm vi (mục 4.3.3 trình bày cách tính). Toàn bộ chạy trong 46 giây trên máy cá nhân, mã nguồn và nhật ký chạy kèm báo cáo.

**Hình 4.3.2a.** Cấu hình huấn luyện và nhật ký chạy → chụp phần đầu `results/cum4/cum4_ket_qua.md` hoặc đoạn mã cấu hình trong `python/cum4_huan_luyen.py`.

Bảng 4.3.2a tổng hợp kết quả trung bình trên bốn fold và số fold đạt từng điều kiện của mục 3.4.6. Hai mô hình đạt cả ba điều kiện ở 4/4 fold là Naive Bayes và mạng nơ-ron. Mạng nơ-ron có ROC-AUC cao nhất (0,751 so với 0,720), nhưng Naive Bayes có Brier thấp nhất (0,125) và giá trị ròng Z cao nhất (291.883 USD so với 288.379 USD). Theo luật ở mục 3.4.6, khi nhiều mô hình cùng đạt thì chọn mô hình có Z cao hơn ở nhiều mốc hơn: Naive Bayes cao hơn mạng nơ-ron ở 4/4 mốc (Bảng 4.3.2b), chênh trung bình 3.504 USD, tương đương 1,2%. Vì vậy Naive Bayes là mô hình chấm điểm, đúng như đã chốt ở mục 3.4.5. Hai lý do bổ sung: mạng nơ-ron thay đổi kết quả theo hạt giống khởi tạo (độ lệch chuẩn ROC-AUC giữa ba hạt giống là 0,019, có hạt giống cho ROC-AUC 0,710 tại mốc 15/01/2014), còn Naive Bayes là mô hình xác định và tái lập được trên mọi máy. Ba mô hình bổ sung có ROC-AUC từ 0,724 đến 0,741 nhưng Z không cao hơn Naive Bayes, cho thấy với bài toán này xác suất hiệu chỉnh tốt quan trọng hơn khả năng xếp hạng.

**Bảng 4.3.2a.** Kết quả trung bình bốn fold và số fold đạt ba điều kiện chọn mô hình → dán từ `bang_4_3_2b_trung_binh.csv` (cột: Vai trò, Mô hình, ROC-AUC, Brier, Z theo p·v, ĐK1, ĐK2, ĐK3).

**Bảng 4.3.2b.** Giá trị ròng Z của Naive Bayes và mạng nơ-ron theo từng mốc → dán từ `bang_4_3_2c_nb_vs_mlp.csv`.

Cây đối chứng đạt điều kiện Z ở 4/4 fold nhưng ROC-AUC chỉ 0,680, thấp hơn quy tắc Recency đảo chiều ở 3/4 fold với khoảng tin cậy 95% nằm dưới 0. Nguyên nhân là cây có từ 9 đến 11 lá nên xác suất thô, và nhóm khách mua theo chu kỳ năm (Recency 270 đến 539 ngày) quá nhỏ để tách thành lá riêng. Điều này đúng với dự đoán ở mục 3.4.5: cây không được dùng để chấm điểm, chỉ dùng để sinh luật IF-THEN mô tả nhóm khách và TopFactors. Thuộc tính ở nút gốc ổn định qua bốn mốc (luôn là Recency, ngưỡng từ 131,5 đến 170,5 ngày), nên cấu trúc luật đọc được và nhất quán giữa các kỳ.

Bảng 4.3.2c so sánh các cấu hình của Bảng 3.15. Huấn luyện lại ở mốc gần nhất cho Naive Bayes Z = 291.883 USD, cao hơn học một lần ở mốc đầu (283.465 USD) và gộp mọi mốc (281.033 USD), xác nhận giả thuyết ở mục 3.4.4 về cơ cấu khách thay đổi. Với cây, độ sâu 3 đến 6 và số khách tối thiểu mỗi lá 200 đến 800 chỉ làm ROC-AUC dao động trong 0,671 đến 0,687 và m từ 0 đến 200 gần như không đổi kết quả, nên giữ cấu hình xuất phát (sâu 4, 400 khách mỗi lá, m = 50) vì luật ngắn nhất. Với mạng nơ-ron, kiến trúc (32, 16) tốt hơn (16,) và (64, 32).

**Bảng 4.3.2c.** So sánh cấu hình theo Bảng 3.15 (trung bình bốn fold) → dán từ `bang_4_3_2d_cau_hinh.csv`.

Hình 4.3.2b vẽ đường ROC và Precision–Recall của các mô hình tại fold cuối (E = 01/03/2014). Đường ROC của Naive Bayes và Recency đảo chiều gần trùng nhau, đường của mạng nơ-ron cao hơn ở vùng tỷ lệ dương tính giả 0,2 đến 0,4, còn cây có dạng bậc thang vì chỉ có 11 mức xác suất. Ma trận nhầm lẫn của Naive Bayes tại fold này với ngưỡng Youden chọn trên mốc huấn luyện (0,729) cho accuracy 0,837, sensitivity 0,902, specificity 0,541 và precision 0,899 (Hình 4.3.2c). Các chỉ số lớp 1 này chỉ để tham khảo vì DSS không phân lớp theo ngưỡng mà chọn khách theo giá trị kỳ vọng trong ngân sách (mục 3.4.6).

**Hình 4.3.2b.** Đường ROC và Precision–Recall tại mốc 01/03/2014 → `hinh_4_3_2_roc_pr.png`.
**Hình 4.3.2c.** Ma trận nhầm lẫn của Naive Bayes tại mốc 01/03/2014 → `hinh_4_3_2_ma_tran_nham_lan.png`.

Mô hình cuối được học lại trên mốc 01/03/2014 (14.167 khách, tỷ lệ y = 1 là 81,97%) rồi chấm điểm 18.360 khách tại mốc 08/07/2014. RiskScore của Naive Bayes có trung vị 0,922, tứ phân vị 0,803 và 0,975, (Hình 4.3.2d). RiskLevel Cao = 25% khách có RiskPercentile cao nhất trong từng hạng ABC: A 1.285, B 646, C 2.661, tổng 4.592. Cây đối chứng học cùng mốc có 11 lá, luật ở Bảng 4.3.2d, trong đó nhánh Recency trên 275 ngày và Tenure trên 744 ngày là nhóm có tỷ lệ không mua lại thấp nhất (18,1%), tức nhóm khách mua đều theo năm. Số khách có TreeScore lệch RiskScore quá 0,3 là 2.560 (13,9%), DSS cắm cờ xem xét cho các khách này theo Bảng 3.19. Mô hình chấm điểm, cây, tham số rời rạc hóa và bảng xác suất có điều kiện được lưu thành tệp và đăng ký vào analytics.ModelRegistry ở mục 4.3.4.

**Bảng 4.3.2d.** Các lá của cây đối chứng học ở mốc 01/03/2014 (luật, số khách, tỷ lệ y = 1, TreeScore) → ghép từ phần "Cây đối chứng" và `bang_4_3_2f_la_cay.csv`.
**Hình 4.3.2d.** Phân bố RiskScore tại mốc 08/07/2014 của Naive Bayes và mạng nơ-ron → `hinh_4_3_2_phan_bo_diem.png`.

Giới hạn: bốn fold có cửa sổ nhãn chồng nhau và các cấu hình được chọn trên chính bốn fold này, nên kết quả có thiên lệch lựa chọn (mục 3.4.4). Chênh lệch Z giữa Naive Bayes và mạng nơ-ron (1,2%) nhỏ hơn biến động Z của mạng nơ-ron giữa các hạt giống (khoảng 2.900 USD), vì vậy lựa chọn Naive Bayes dựa trên việc thắng nhất quán ở mọi mốc và mọi hạt giống, không dựa trên độ lớn của chênh lệch.

---
Ghi chú cho người dán: thay thế các bảng cũ ở 4.3.2 (đã bị xoá, chỉ còn con trỏ tới Bảng 3.14, 3.15). Mọi số trong đoạn văn lấy từ `cum4_ket_qua.md`, nếu chạy lại trên máy khác thì chỉ dòng MLP có thể lệch ở chữ số thứ 3, các dòng khác phải giống hệt.
