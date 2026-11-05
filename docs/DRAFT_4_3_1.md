# Bản nháp 4.3.1. Chuẩn bị dữ liệu huấn luyện (thay toàn bộ 4.3.1 cũ)
Quy ước: không dùng dấu chấm phẩy, không ghi "bài giảng", bảng và hình đánh số tiếp theo của Chương 4 khi dán (số tạm 4.3.1a…). Nguồn số: `results/cum3b/`.

---

### 4.3.1. Chuẩn bị dữ liệu huấn luyện

Bước này hiện thực quy trình ở mục 3.4.3 trên kho CompanyX_DW sau cụm ETL và Snapshot (mục 4.2). Bộ dữ liệu gồm một dòng cho mỗi cặp (khách, mốc T) với 11 thuộc tính ở Bảng 3.9 và Bảng 3.10, đọc từ bảng analytics.CustomerSnapshot, và nhãn y tính theo công thức (3.1) từ FactSalesOrder: y = 1 nếu khách không có đơn nào đặt trong 90 ngày kể từ T, tính cả ngày T và không tính ngày T + 90. Nhãn chỉ được dùng khi T + 97 ngày không vượt quá mốc đánh giá E (cửa sổ 90 ngày cộng 7 ngày gửi đơn) và cửa sổ nhãn kết thúc trước 01/06/2014, vì tháng 6/2014 có 930 đơn nhưng không có đơn xe đạp nào (mục 3.4.3). Với điều kiện này, 19 mốc từ 01/06/2013 đến 01/03/2014 có nhãn đầy đủ, còn mốc chấm điểm 08/07/2014 chỉ có thuộc tính.

Bảng 4.3.1a trình bày số khách và tỷ lệ y = 1 tại từng mốc cùng ba đại lượng theo dõi của Bảng 3.13. Số khách tăng từ 5.324 lên 14.167 vì kho tích lũy thêm khách mới, tỷ lệ y = 1 dao động trong khoảng 79,3% đến 82,8%. Tỷ lệ khách chỉ có một đơn giảm dần từ 100% xuống 69,3% và tỷ lệ khách đã mua từ hai danh mục con trở lên tăng từ 0% lên 64,9%, cho thấy cơ cấu khách thay đổi rõ giữa các mốc, đúng với lý do huấn luyện lại ở mỗi kỳ (mục 3.4.4).

**Bảng 4.3.1a.** Số khách, tỷ lệ y = 1 và các đại lượng theo dõi tại 20 mốc phân tích → dán từ `bang_4_3_1a_moc.csv` (cột: Mốc T, Số khách, Số khách y = 1, Tỷ lệ y = 1, Tỷ lệ 1 đơn, Tỷ lệ BikeBuyer, Tỷ lệ NSub ≥ 2).

Bảng 4.3.1b ghép bốn mốc đánh giá với mốc huấn luyện theo Bảng 3.12 kèm số khách thật. Mỗi mốc huấn luyện có từ 7.705 đến 10.447 khách, mốc đánh giá có từ 11.564 đến 14.167 khách, và trong mọi cặp, nhãn của mốc huấn luyện đã đủ ngày trước mốc đánh giá. Hình 4.3.1 minh họa lịch này trên trục thời gian.

**Bảng 4.3.1b.** Bốn fold phát triển và mốc chấm điểm với số khách thật → dán từ `bang_4_3_1b_fold.csv`.

**Hình 4.3.1.** Lịch ghép mốc huấn luyện, cửa sổ nhãn và mốc đánh giá trên dữ liệu thật → `hinh_4_3_1_moc_thoi_gian.png`.

Để hỗ trợ diễn giải, Bảng 4.3.1c cho tỷ lệ y = 1 theo các khoảng rời rạc hóa của Bảng 3.10 tại mốc huấn luyện cuối 01/03/2014. Quan hệ giữa Recency và nhãn không đơn điệu: khách mua trong 270 ngày gần nhất có tỷ lệ không mua lại từ 88,9% đến 91,9%, nhưng khách có Recency từ 270 đến 539 ngày chỉ 28,5% đến 32,2%, tức nhóm mua theo chu kỳ năm đang đến kỳ mua lại. Monetary cũng không đơn điệu (Q3 thấp nhất, 68,5%). Đây là lý do Chương 3 rời rạc hóa thuộc tính cho Naive Bayes thay vì giả định quan hệ tuyến tính. Các khoảng này chỉ để mô tả, mô hình học ngưỡng và xác suất từ dữ liệu.

**Bảng 4.3.1c.** Tỷ lệ y = 1 theo khoảng rời rạc hóa tại mốc huấn luyện 01/03/2014 → dán từ `bang_4_3_1c_khoang.csv`.

Chuẩn hóa và rời rạc hóa được thực hiện đúng Bảng 3.11: ranh giới tứ phân vị của Monetary (60,75 USD, 666,86 USD và 3.023,74 USD tại mốc 01/03/2014), trung bình và độ lệch chuẩn cho z-score của mô hình so sánh đều tính trên mốc huấn luyện rồi giữ nguyên khi áp dụng cho mốc đánh giá và mốc chấm điểm. Các tham số này được lưu cùng mô hình (tệp `models/chuan_hoa_T20140301.json`) và ghi vào analytics.ModelRegistry ở mục 4.3.4. Không lấy log Monetary, đúng kết luận ở mục 3.4.2.

Kiểm tra trước khi huấn luyện: tính lại độc lập toàn bộ 10 thuộc tính của 196.985 dòng Snapshot từ hai bảng fact bằng Python cho kết quả khớp hoàn toàn với bảng trong kho, 10 kiểm tra miền giá trị (Tenure không nhỏ hơn Recency, Orders90 không lớn hơn Orders180 không lớn hơn Frequency, tổng tỷ trọng bằng 1, không có giá trị thiếu) đều đạt, và tập khách của mỗi mốc đúng bằng tập khách có đơn đặt và gửi trước T. Chi tiết trong biên bản chuẩn hoá kèm mã nguồn.

---
Ghi chú cho người dán: đoạn "Bảng 4.3.1a" có 20 dòng, nên đặt page-break-before và keep-with-next cho chú thích. Số liệu 4.2.2 (Bảng 4.2) trùng cột "Số khách" của Bảng 4.3.1a, có thể dẫn chéo thay vì lặp.
