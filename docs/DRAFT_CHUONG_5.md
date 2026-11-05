# BẢN NHÁP CHƯƠNG 5 (chưa dán lên Doc)

Quy ước: phần A là nội dung để dán. Phần B là bảng đối chiếu, không dán. Mọi số lấy từ Chương 4 trên Doc (kiểm bằng xuất HTML ngày 04/11/2026). Lý thuyết lấy từ slide môn học, trong thân bài chỉ ghi "theo tài liệu môn học" hoặc số tài liệu [n] đã có trong danh mục.

---

## PHẦN A. NỘI DUNG

CHƯƠNG 5. ĐÁNH GIÁ VÀ PHÂN TÍCH KẾT QUẢ (EVALUATION AND DISCUSSION)

Chương này đánh giá ba thành phần đã triển khai ở Chương 4 là kho dữ liệu cùng quy trình ETL, mô hình Machine Learning và hệ thống hỗ trợ ra quyết định. Mỗi thành phần được đối chiếu với tiêu chí đã đặt ra ở Chương 3 và với khung lý thuyết theo tài liệu môn học. Mọi số liệu trong chương lấy từ kết quả ở Chương 4, nhóm không chạy thêm thí nghiệm mới.

### 5.1. Đánh giá Data Warehouse và ETL

Theo tài liệu môn học, chất lượng dữ liệu được đánh giá theo sáu chiều chính. Tính đầy đủ (Completeness) là tỷ lệ dữ liệu đã lưu so với mức đầy đủ 100%. Tính duy nhất (Uniqueness) là mỗi đối tượng chỉ được ghi một lần theo cách đối tượng đó được định danh. Tính kịp thời (Timeliness) là mức dữ liệu phản ánh đúng thực tế tại thời điểm cần dùng. Tính hợp lệ (Validity) là dữ liệu tuân theo cú pháp đã định nghĩa, gồm định dạng, kiểu và miền giá trị. Tính chính xác (Accuracy) là mức dữ liệu mô tả đúng đối tượng hoặc sự kiện trong thực tế. Tính nhất quán (Consistency) là không có khác biệt khi so sánh hai hay nhiều cách biểu diễn của cùng một đối tượng. Bảng 5.1 đối chiếu các nhóm kiểm tra đã thiết kế ở Bảng 3.7 và kết quả ở Chương 4 với sáu chiều này.

Năm trong sáu chiều có phép kiểm tra trực tiếp và đều đạt, với 44/44 phép kiểm tra sau ETL và 21/21 phép kiểm tra Customer Snapshot không có FAIL. Kết quả nạp cũng khớp với phạm vi đã xác định. Trong 19.820 bản ghi khách hàng được trích xuất, 18.484 khách cá nhân hợp lệ được nạp vào DimCustomer và 1.336 bản ghi ngoài phạm vi được loại. Từ 31.465 đơn hàng và 121.317 dòng chi tiết ở staging, kho giữ 27.382 đơn và 59.795 dòng chi tiết (Bảng 4.1). Lần chạy ETL cuối hoàn tất 11 bước với trạng thái SUCCESS (Hình 4.7).

Có hai điểm cần nói rõ. Thứ nhất, tính chính xác mới được kiểm ở mức kho khớp với nguồn. Theo định nghĩa, dữ liệu chính xác phải mô tả đúng thực tế, nhưng nhóm không có nguồn độc lập để đối chiếu, nên nếu dữ liệu nguồn sai thì kho cũng sai theo. Thứ hai, tính kịp thời chưa có phép kiểm tra tự động. Nhóm xử lý gián tiếp bằng cách chỉ dùng dữ liệu trước mốc phân tích khi tạo Customer Snapshot và dừng cửa sổ nhãn trước 01/06/2014. Hướng cải tiến được nêu ở mục 5.4.

Bảng 5.1. Đánh giá kho dữ liệu CompanyX_DW theo sáu chiều chất lượng dữ liệu

| Chiều chất lượng | Phép kiểm tra tương ứng | Kết quả ở Chương 4 | Mức đáp ứng |
|---|---|---|---|
| Completeness | Số lượng bản ghi, mã định danh nguồn, giá trị thiếu trong Customer Snapshot | 8/8 và 8/8 PASS (Bảng 4.3), 21/21 PASS (Hình 4.9) | Đạt |
| Uniqueness | Khóa trùng trong kho, bản ghi trùng theo cặp khách và mốc trong Customer Snapshot | Nhóm khóa và quan hệ 6/6 PASS (Bảng 4.3), 21/21 PASS (Hình 4.9) | Đạt |
| Timeliness | Customer Snapshot chỉ dùng dữ liệu phát sinh trước mốc phân tích, cửa sổ nhãn kết thúc trước 01/06/2014 | Chưa có phép kiểm tra tự động riêng. Tháng 6/2014 có 930 đơn nhưng không có đơn xe đạp nào, được nhận ra khi khảo sát dữ liệu và khi so với dự báo (Bảng 4.32) | Một phần |
| Validity | Loại khách, trạng thái đơn, ngày giao dịch, giá, số lượng, chiết khấu, mã ánh xạ và bản ghi bất thường | 8/8 và 6/6 PASS (Bảng 4.3). 6 đơn và 75 dòng chi tiết ngoài phạm vi được ghi vào etl.RejectedRow | Đạt |
| Accuracy | Đối chiếu SubTotal, TotalDue và LineTotal giữa CompanyX và CompanyX_DW | 4/4 PASS. SubTotal 29.052.549,9450 và TotalDue 32.103.068,4755 khớp ở hai cơ sở dữ liệu | Đạt khi so với nguồn |
| Consistency | Liên kết giữa Fact và Dimension, quan hệ giữa các thành phần giá trị đơn hàng | Nhóm khóa và quan hệ 6/6 PASS, không có sai lệch vượt dung sai 0,01 | Đạt |

### 5.2. Đánh giá Machine Learning

Theo tài liệu môn học, phân lớp gồm hai bước. Bước học xây dựng mô hình phân lớp, bước phân lớp dùng mô hình đó để dự đoán nhãn lớp cho dữ liệu mới. Kết quả phân lớp được tóm tắt bằng ma trận nhầm lẫn gồm bốn ô TP, TN, FP và FN [3]. Nhóm đánh giá theo ba lớp tiêu chí ở Bảng 3.16, gồm khả năng phân lớp, chất lượng xác suất và giá trị quyết định, trên bốn fold Rolling-Origin (Bảng 4.5).

#### 5.2.1. So sánh với các mốc so sánh

Bảng 4.7 cho thấy chỉ Naive Bayes và mạng nơ-ron đạt cả ba điều kiện chọn mô hình ở 4/4 fold. Quy tắc Recency đảo chiều xếp hạng gần bằng Naive Bayes (ROC-AUC 0,717 so với 0,720) nhưng xác suất kém xa (Brier 0,269 so với 0,125), nên không đạt điều kiện về Brier ở fold nào. Logistic Regression đạt ROC-AUC 0,659, thấp hơn cả quy tắc Recency. Cây Gini đạt 0,680 vì chỉ có từ 9 đến 11 lá nên xác suất thô. Mạng nơ-ron có ROC-AUC cao nhất (0,751) nhưng Z thấp hơn Naive Bayes ở cả bốn mốc, chênh trung bình 3.504 USD (Bảng 4.8), và kết quả còn thay đổi theo hạt giống khởi tạo.

Điểm yếu cần thừa nhận là khả năng xếp hạng của Naive Bayes gần như không hơn quy tắc đơn giản. Tại mốc 01/03/2014, ROC-AUC của Naive Bayes là 0,7207, so với 0,7191 của Recency đảo chiều (Bảng 4.16). Giá trị của mô hình nằm ở chất lượng xác suất và giá trị quyết định. Brier Score đạt 0,1176, thấp hơn mức 0,1480 của cách dự đoán một xác suất hằng cho mọi khách. Khi chọn khách theo p·v, Z đạt 289.245,54 USD, cao hơn 13,7% so với 254.292,63 USD khi chỉ chọn theo giá trị v, và thu hẹp khoảng 41% khoảng cách đến mức trần 339.886,26 USD khi biết trước nhãn. Nói cách khác, Recency đủ để biết ai có nguy cơ, nhưng cần xác suất được hiệu chỉnh tốt để quyết định chi ngân sách cho ai.

#### 5.2.2. Phân tích chỉ số và ma trận nhầm lẫn

Bảng 4.15 cho thấy cần chọn chỉ số theo cách DSS dùng mô hình. Với ngưỡng Youden chọn trên mốc huấn luyện, mô hình cảnh báo 82,2% số khách, đạt accuracy 0,837 và F1 0,901. Tuy nhiên cách luôn dự đoán y = 1 cũng đạt accuracy 0,820 và F1 0,901 với specificity bằng 0, vì lớp y = 1 chiếm khoảng 82% số khách. Accuracy và F1 vì vậy không đủ để đánh giá khi lớp mục tiêu chiếm đa số. DSS chỉ gắn mức Cao cho khách từ phân vị 75 trong từng hạng ABC, tức 25,0% số khách. Ở mức này sensitivity chỉ 0,274 nhưng precision đạt 0,898, cao hơn tỷ lệ nền 0,820, và Precision@4.000 đạt 89,33%. Với ngân sách có hạn, người quản lý cần một danh sách ưu tiên ít nhầm, không cần bắt hết mọi khách có nguy cơ.

#### 5.2.3. Những đặc trưng quan trọng

Recency là đặc trưng chi phối. Trong cây đối chứng, độ quan trọng Gini của Recency là 0,83 và của Monetary là 0,12, nút gốc luôn tách theo Recency ở cả bốn mốc. Trong Naive Bayes, khách có Recency từ 180 đến 269 ngày có tỷ số xác suất có điều kiện giữa hai lớp là 2,495, còn khách có Recency từ 365 đến 539 ngày có tỷ số 0,088 (Bảng 4.17). Nhóm sau phù hợp với nhóm khách mua theo chu kỳ năm đã nêu ở mục 4.3.1 và 4.3.2. Monetary thấp (Q1) có tỷ số 1,907, Monetary cao (Q3) có tỷ số 0,478. NSub không xuất hiện trong cây nhưng có ích cho Naive Bayes. Bỏ NSub làm ROC-AUC giảm từ 0,720 xuống 0,701, Brier tăng từ 0,125 lên 0,133 và Z giảm 2.577 USD (Bảng 4.12).

#### 5.2.4. Đánh giá theo thời gian

Mỗi fold học trên một mốc và đánh giá trên mốc sau đó, Customer Snapshot không dùng thông tin phát sinh sau mốc phân tích (Bảng 4.5, Hình 4.12). Kết quả theo thời gian cho thấy hai điều.

Thứ nhất, cơ cấu khách thay đổi nhanh. Tại mốc 01/06/2013, mọi khách chỉ có một đơn và đều từng mua xe đạp. Đến 01/03/2014 hai tỷ lệ này còn 69,3% và 54,1%, đến 08/07/2014 còn 63,1% và 49,5% (Bảng 4.4). Vì vậy huấn luyện lại ở mốc gần nhất cho Z 291.883 USD, cao hơn học một lần ở mốc đầu (283.465 USD) và gộp mọi mốc (281.033 USD). DSS cần học lại mô hình mỗi lần chấm điểm.

Thứ hai, nhãn 90 ngày có nhiễu. 26,2% số khách bị gắn y = 1 theo nhãn 90 ngày có mua lại trong khoảng ngày thứ 90 đến 180 (Bảng 4.13), tức là khách chưa đến kỳ chứ chưa bỏ đi. Khi đối chiếu với nhãn 180 ngày, ROC-AUC của Naive Bayes tăng ở cả ba mốc của Bảng 4.14, chẳng hạn từ 0,707 lên 0,773 tại mốc 01/12/2013. Như vậy một phần dự đoán bị tính là sai theo nhãn 90 ngày thực ra là khách chưa đến kỳ. Ảnh hưởng của điểm này lên giá trị quyết định được xét ở mục 5.3.2.

### 5.3. Đánh giá khả năng hỗ trợ quyết định của DSS

Theo tài liệu môn học, DSS nhận đầu vào về một quy trình ra quyết định đã biết hoặc mới biết một phần, rồi cung cấp thông tin cần để ra quyết định. Quá trình ra quyết định gồm bốn giai đoạn tìm hiểu, thiết kế, lựa chọn và thực hiện, sau đó theo dõi để biết quyết định thành công hay thất bại [1]. DSS cần hỗ trợ nhiều phong cách, kỹ năng và hiểu biết khác nhau của người ra quyết định, không ép một quy trình cố định. Các kỹ thuật phân tích thường dùng là what-if, phân tích độ nhạy, tìm mục tiêu, tối ưu hóa và mô phỏng [1]. Nhóm đánh giá DSS theo ba câu hỏi: hệ thống trả lời được câu hỏi kinh doanh nào, có giúp chọn khách tốt hơn cách đơn giản không, và đáp ứng các đặc điểm của DSS đến đâu.

#### 5.3.1. Các câu hỏi kinh doanh hệ thống trả lời được

Bảng 5.2. Câu hỏi kinh doanh và mức trả lời của DSS

| Câu hỏi (mục 2.2) | Chức năng và màn hình | Bằng chứng ở Chương 4 | Mức trả lời |
|---|---|---|---|
| Q1. Khách nào có nguy cơ không mua lại | RiskScore của Naive Bayes, RiskLevel theo từng hạng ABC, màn hình 1 và 2 | 4.592 khách Cao trong 18.360 khách được chấm điểm ngày 08/07/2014 (A 1.285, B 646, C 2.661). Tại mốc 01/03/2014, precision ở mức Cao là 0,898 (Bảng 4.15, Bảng 4.23) | Trả lời được, theo nhãn thay thế 90 ngày |
| Q2. Hành vi mua thay đổi thế nào | Customer Snapshot 20 mốc, năm nhóm khách K-means, luật kết hợp Apriori, dự báo theo tháng ở màn hình 5 | Cơ cấu khách theo mốc (Bảng 4.4), hồ sơ năm nhóm (Bảng 4.22), 26 luật dùng được làm gợi ý trong 164 luật (Bảng 4.25), MAPE 8,2% với số đơn và 15,4% với doanh thu (Bảng 4.32) | Trả lời được |
| Q3. Nên ưu tiên giữ chân khách nào | Giá trị kỳ vọng, ma trận Rủi ro × Giá trị, chọn khách theo ngân sách, màn hình 3 | Kịch bản cơ sở chọn 4.000 khách với Z 292.595 USD (Bảng 4.28). Bài toán theo kênh chọn 6.124 khách với Z 256.502 USD (Bảng 4.31) | Trả lời được, phụ thuộc giả định về r và c |
| Q4. Nên dùng hành động giữ chân nào | Quy tắc R1 đến R9, kênh R3 đến R5, gợi ý sản phẩm, màn hình 4 | R3 có 983 khách, R5 có 5.141 khách, R4 chỉ có khách khi ngân sách từ khoảng 61.213 USD (Bảng 4.31). R1, R9 và nhóm đối chứng cần dữ liệu CRM | Một phần |

#### 5.3.2. DSS so với cách chọn khách đơn giản

Có ba bằng chứng cho thấy DSS giúp chọn khách tốt hơn. Thứ nhất, tại mốc đánh giá 01/03/2014, chọn khách theo p·v cho Z cao hơn 13,7% so với chọn chỉ theo giá trị (Bảng 4.16). Thứ hai, trong bài toán theo kênh, xếp khách theo lợi trên mỗi USD chi phí cho Z cao hơn 6,9% so với xếp theo p·v mà bỏ qua chi phí kênh, và ngân sách được dồn vào hai nhóm có giá trị là N1 (3.964 khách) và N2 (2.160 khách). Thứ ba, kết quả vẫn dương khi giả định bất lợi hơn. Nếu trừ khách chưa đến kỳ khỏi lợi ích, Z của kịch bản cơ sở còn 205.555 USD với tỷ lệ thành công hoà vốn 1,63% (Bảng 4.27). Mô phỏng 10.000 lần với r theo phân phối Beta cho Z trung bình 290.490 USD và xác suất lỗ 1,7% (Hình 4.24).

Các kết quả này phù hợp với lý do cần DSS theo tài liệu môn học, gồm nâng chất lượng quyết định và vượt qua giới hạn của con người khi lưu trữ và xử lý thông tin. Người quản lý khó tự xếp hạng 18.360 khách theo xác suất, giá trị và chi phí kênh trong một ngân sách cố định.

#### 5.3.3. Hỗ trợ các giai đoạn ra quyết định

Ở giai đoạn tìm hiểu, màn hình 1 cho biết tỷ lệ khách rủi ro theo hạng và nhóm, màn hình 5 cho biết mô hình còn tốt hơn quy tắc đơn giản hay không. Ở giai đoạn thiết kế, mô hình giá trị kỳ vọng có đủ ba loại biến theo tài liệu môn học: biến quyết định là danh sách khách và ngân sách B, tham số không kiểm soát được là tỷ lệ chăm sóc thành công r, biến kết quả là giá trị ròng Z. Ở giai đoạn lựa chọn, màn hình 3 cung cấp what-if, độ nhạy, tìm mục tiêu, bảng payoff, mô phỏng và bài toán chọn khách theo kênh giải bằng quy hoạch nguyên. Ở giai đoạn thực hiện, màn hình 4 cho phép bớt khách có ghi lý do và xuất danh sách CSV, còn chiến dịch do CRM thực hiện. Việc theo dõi quyết định thành công hay thất bại chưa làm được vì chưa có dữ liệu chiến dịch. Màn hình 5 mới theo dõi mô hình và dữ liệu nguồn, chẳng hạn dự báo đã phát hiện tháng 6/2014 lệch mạnh. Giai đoạn thực hiện vì vậy mới đạt mức một phần (Bảng 4.34).

Ba tình huống sau minh họa cách người quản lý dùng DSS.

Tình huống 1, hai mô hình không thống nhất. Khách 26339 có RiskScore 0,963 (mức Cao) nhưng TreeScore chỉ 0,586. Khách thuộc lá 5 của cây, nhóm gồm 440 khách với tỷ lệ không mua lại 55,9%. Chênh lệch 0,377 vượt ngưỡng 0,3 nên khách được gắn cờ để xem xét thêm (Bảng 4.18). DSS không tự sửa điểm mà để người quản lý quyết định. Toàn bộ có 2.560 khách (13,9%) được gắn cờ như vậy.

Tình huống 2, tỷ lệ thành công chưa biết. Vì r chưa đo được, người quản lý cần biết quyết định chịu được sai lệch đến đâu. Chức năng tìm mục tiêu cho r hoà vốn 1,20% và r cần có để Z đạt 100.000 USD là 4,21%. Khi r thay đổi 20% thì Z thay đổi 22,7% (Bảng 4.29). Với bảng payoff, người lạc quan và tiêu chí giá trị kỳ vọng chọn ngân sách 100.000 USD, còn người bi quan chọn 40.000 USD (Bảng 4.30). DSS không chọn thay mà đưa ra phương án cho từng phong cách ra quyết định.

Tình huống 3, cái giá của việc chăm sóc nhóm N3. Ở ngân sách 40.000 USD, kênh R4 dành cho nhóm N3 không được chọn khách nào. Kênh này chỉ bắt đầu có khách khi ngân sách từ khoảng 61.213 USD (Bảng 4.27). Người quản lý thấy rõ muốn chăm sóc N3 thì cần tăng ngân sách bao nhiêu.

#### 5.3.4. Đối chiếu với đặc điểm DSS và tính khả dụng

Bảng 4.34 đối chiếu bản triển khai với 14 đặc điểm DSS. Có 4 đặc điểm đạt đầy đủ, 9 đặc điểm đạt một phần và 1 đặc điểm hạn chế. Bốn đặc điểm đầy đủ là giải quyết bài toán bán cấu trúc và phi cấu trúc, hỗ trợ nhiều quy trình và phong cách ra quyết định, con người kiểm soát máy, mô hình hóa và phân tích. Đặc điểm hạn chế là người dùng cuối dễ tự phát triển, vì muốn sửa mô hình vẫn cần SQL và Python.

Khả dụng gồm ba mặt là hiệu quả, hiệu suất và mức hài lòng của người dùng [21]. Rà soát nội bộ theo 10 nguyên tắc Nielsen tìm ra 16 vấn đề, nhóm đã sửa 13 vấn đề, gồm cả ba vấn đề nặng nhất (Bảng 4.33). Nhóm không thử nghiệm với người dùng thật, nên chương này chưa kết luận về mức hài lòng.

### 5.4. Hạn chế và hướng cải tiến

Bảng 5.3 tóm tắt các hạn chế rút ra từ ba mục trên và từ cột giới hạn ở Bảng 3.0, cùng hướng cải tiến tương ứng.

Bảng 5.3. Hạn chế và hướng cải tiến

| STT | Hạn chế | Ảnh hưởng | Hướng cải tiến |
|---|---|---|---|
| 1 | Kho chỉ có một nguồn OLTP và dùng SCD Type 1 | Không giữ lịch sử thay đổi thông tin khách, thiếu dữ liệu ngoài giao dịch | Dùng SCD Type 2, tích hợp thêm nguồn CRM |
| 2 | Kho nạp một lần từ bản sao lưu tĩnh, chưa kiểm tra độ mới và chưa ghi nhật ký sử dụng | Dữ liệu thiếu như tháng 6/2014 chỉ lộ ra khi khảo sát. Kho mới được đối chiếu với nguồn, chưa với thực tế | Kiểm tra ngày dữ liệu mới nhất trước mỗi lần nạp, ghi nhật ký truy cập và thời gian phản hồi |
| 3 | Chưa có nhãn churn thực tế, chỉ dùng nhãn 90 ngày | 26,2% khách y = 1 là khách chưa đến kỳ. Trừ nhóm này, Z cơ sở còn 205.555 USD | Dùng thêm nhãn 180 ngày, xác nhận khách rời bỏ bằng dữ liệu CRM |
| 4 | Lịch sử dữ liệu ngắn | Chỉ 19 mốc có nhãn đầy đủ, từ 01/06/2013 đến 01/03/2014 | Bổ sung dữ liệu mới, học lại mô hình mỗi lần chấm điểm |
| 5 | Bốn mốc đánh giá cũng là tập dùng để chọn mô hình | Kết quả có thể lạc quan. Ngưỡng Youden trên mốc huấn luyện cảnh báo 82,2% khách, ngoài mẫu chỉ 64,4% (Bảng 4.15) | Đối chiếu với nhãn thật khi có dữ liệu sau 08/07/2014, giữ một giai đoạn kiểm thử riêng |
| 6 | Khả năng xếp hạng chỉ ngang quy tắc Recency | ROC-AUC 0,7207 so với 0,7191, mô hình mạnh về xác suất hơn thứ hạng | Thêm dữ liệu ngoài giao dịch nếu có, như phản hồi chiến dịch |
| 7 | Chưa có dữ liệu chiến dịch | r và c là giả định, R1, R9 và nhóm đối chứng chưa chạy được | Chạy chiến dịch có nhóm đối chứng để đo r thay cho giả định |
| 8 | Giai đoạn thực hiện dừng ở xuất CSV, quy tắc mới chưa lưu vào kho | Kết quả chiến dịch chưa quay lại DSS | Kết nối CRM, lưu quy tắc mới vào kho |
| 9 | Chưa thử nghiệm khả dụng với người dùng thật | Kết luận về khả dụng mới dựa trên rà soát nội bộ | Thử với người dùng thật, chấm phiếu SUS |

Tóm lại, kho dữ liệu đạt năm trong sáu chiều chất lượng, mô hình Naive Bayes không xếp hạng tốt hơn nhiều so với quy tắc đơn giản nhưng cho xác suất đủ tốt để chọn khách có giá trị hơn, và DSS hỗ trợ đủ bốn giai đoạn ra quyết định, trong đó giai đoạn thực hiện còn phụ thuộc hệ thống CRM. Chương 6 tổng kết các kết quả này.

---

## PHẦN B. ĐỐI CHIẾU (không dán)

### B1. Lý thuyết lấy từ slide

| Câu trong bản nháp | Slide | Nguyên văn slide (rút gọn) |
|---|---|---|
| Sáu chiều chất lượng và định nghĩa | Lecture 4, slide 46 (DAMA UK 2013) | Completeness "proportion of stored data against the potential of 100% complete", Uniqueness "no thing recorded more than once", Timeliness "represent reality from the required point in time", Validity "conforms to the syntax (format, type, range)", Accuracy "correctly describes the real world object or event", Consistency "absence of difference when comparing two or more representations" |
| Phân lớp hai bước | Lecture 5, slide 60 | "learning step where a classification model is constructed", "classification step where the model is used to predict class labels for given data" |
| TP, TN, FP, FN và ma trận nhầm lẫn | Lecture 5, slide 69–70 (nguồn [2] của slide là Han, Kamber, Pei, trùng [3] của Doc) | định nghĩa bốn ô, "Confusion matrix" |
| DSS nhận đầu vào về quy trình đã biết hoặc biết một phần | Lecture 1, slide 48 | "takes inputs regarding a known (or partially-known) decision making process and provide the information necessary to make a decision" |
| Bốn giai đoạn và theo dõi | Lecture 6, slide 7 | Intelligence, Design, Choice, Implementation, "Success vs. Failure? Monitoring & Feedback" |
| Hỗ trợ nhiều phong cách, không ép quy trình | Lecture 6, slide 27 | "support varying styles, skills, and knowledge", "should not attempt to enforce a specific process" |
| What-if, độ nhạy, tìm mục tiêu, tối ưu | Lecture 1, slide 49 và Lecture 7, slide 16 | What if, Sensitivity, Goal Seek, Optimization |
| Mô phỏng | Lecture 7, slide 17 | "experiments with a computer on a model to test specific values of the decision or uncontrollable variables" |
| Quy hoạch nguyên | Lecture 7, slide 15 | "Linear and integer programming" |
| Ba loại biến của mô hình | Lecture 7, slide 13 | Decision variables, Uncontrollable variables (parameters), Result (outcome) variables |
| Lý do cần DSS | Lecture 1, slide 47 | "Boosting the quality of decision making", "Overcoming human limitation in information storage and processing" |
| Khả dụng gồm hiệu quả, hiệu suất, hài lòng | Lecture 4, slide 47 (Batini, áp cho dữ liệu) và [21] ISO 9241-11 | "effectiveness, efficiency, satisfaction with which specified users perceive and make use of data" |
| 14 đặc điểm DSS | Lecture 6, slide 29–30 (slide 30 là ảnh, đã đọc qua Notebook), dùng lại Bảng 3.33 và Bảng 4.34 (trước 04/11 đánh số 4.35) | |
| Giám sát kho dữ liệu (Bảng 5.3 dòng 2) | Lecture 4, slide 37–38 | "what data is being used", "who is actually using", "how frequently", "what response time the end user is getting" |

Kết quả Notebook ngày 04/11/2026: cả 9 câu lý thuyết được đánh giá Đúng. Câu về quy hoạch nguyên và ba loại biến đúng về phân loại, phần gán vào bài toán là diễn giải của nhóm (bản nháp đã viết theo hướng áp dụng). Notebook gợi ý thêm giám sát kho dữ liệu, đã đưa vào Bảng 5.3 (nay gộp ở dòng 2) vì hệ thống chưa ghi nhật ký sử dụng (chỉ có nhật ký ETL và nhật ký điều chỉnh ở màn hình 4).

Ghi chú: slide không có tiêu chí nghiệm thu ETL hay phương pháp đánh giá DSS riêng, nên bản nháp dùng sáu chiều chất lượng dữ liệu cho 5.1 và bốn giai đoạn cùng 14 đặc điểm cho 5.3.

### B2. Số liệu lấy từ Doc

| Số trong bản nháp | Vị trí trên Doc |
|---|---|
| 8, 8, 6, 8, 4, 6, 4 phép kiểm tra, 44/44 PASS | Bảng 4.3 |
| 21/21 PASS Customer Snapshot | đoạn trước Hình 4.9 |
| 6 đơn và 75 dòng chi tiết ngoài phạm vi trong etl.RejectedRow | đoạn trước Hình 4.10 |
| SubTotal 29.052.549,9450, TotalDue 32.103.068,4755, dung sai 0,01 | mục 4.2, đoạn đối chiếu tài chính |
| 19.820, 18.484, 1.336 | mục 4.2.2.1 |
| 31.465 đơn, 121.317 dòng ở staging | mục 4.2.2.2 |
| 27.382 đơn, 59.795 dòng | Bảng 4.1 |
| 11 bước, SUCCESS | Hình 4.7 |
| 930 đơn tháng 6/2014, không có đơn xe đạp | mục 4.3 đoạn định nghĩa nhãn, Bảng 4.32 |
| ROC-AUC 0,720/0,717/0,659/0,680/0,751, Brier 0,125/0,269, 4/4 fold | Bảng 4.7 |
| 9 đến 11 lá | đoạn sau Bảng 4.8 |
| chênh 3.504 USD, hạt giống | đoạn trước Bảng 4.7, Bảng 4.8 |
| 0,7207, 0,7191, 0,1176, 0,1480, 89,33%, 289.245,54, 254.292,63, 339.886,26 | Bảng 4.16 |
| 13,7% | tính từ Bảng 4.16: (289.245,54 − 254.292,63) / 254.292,63 = 13,7% |
| khoảng 41% | tính từ Bảng 4.16: 34.952,91 / 85.593,63 = 40,8%. Số này chưa có trên Doc, có thể bỏ nếu nhóm muốn chỉ dùng số đã in |
| 82,2%, 0,837, 0,901, 0,820, specificity 0, 25,0%, 0,274, 0,898 | Bảng 4.15 và đoạn sau |
| Gini Recency 0,83, Monetary 0,12, nút gốc luôn là Recency | đoạn sau Bảng 4.12, đoạn trước Bảng 4.9 |
| 2,495, 0,088, 1,907, 0,478 | Bảng 4.17 |
| bỏ NSub: 0,720 → 0,701, 0,125 → 0,133, −2.577 USD | đoạn sau Bảng 4.12 |
| 100%, 69,3%, 54,1%, 63,1%, 49,5% | Bảng 4.4 |
| 291.883, 283.465, 281.033 | đoạn trước Bảng 4.9 |
| 26,2%, nhãn 90 và 180 ngày | đoạn trước Bảng 4.13 |
| 0,707 → 0,773 tại 01/12/2013, ba mốc | Bảng 4.14 |
| 4.592, A 1.285, B 646, C 2.661, 18.360 | Bảng 4.23 |
| 164 luật, 26 luật | đoạn trước Bảng 4.25 |
| MAPE 8,2%, 15,4% | đoạn trước Bảng 4.32 |
| 4.000 khách, Z 292.595 | đoạn trước Bảng 4.28 |
| 6.124 khách, Z 256.502, 6,9%, R3 983, R5 5.141, R4 0 | đoạn trước Bảng 4.31 và Bảng 4.31 (tổng trong bảng ghi 256.501 do làm tròn từng dòng) |
| 61.213 USD | Bảng 4.27 và đoạn trước Bảng 4.31 |
| N1 3.964, N2 2.160 | Bảng 4.22 và đoạn trước |
| 205.555 USD, 1,63% | Bảng 4.27 |
| mô phỏng 10.000 lần, Z trung bình 290.490, xác suất lỗ 1,7% | đoạn trước Bảng 4.30 |
| r hoà vốn 1,20%, 4,21%, ±22,7% | đoạn trước Bảng 4.29, Bảng 4.29 |
| payoff 100.000 và 40.000 USD | đoạn trước Bảng 4.30 |
| khách 26339: 0,963, 0,586, lá 5, 440 khách, 55,9%, chênh 0,377, ngưỡng 0,3 | Bảng 4.18 và đoạn sau |
| 2.560 khách (13,9%) | đoạn sau Hình 4.17 |
| 4 đầy đủ, 9 một phần, 1 hạn chế, tên các đặc điểm | Bảng 4.34 (trước 04/11 đánh số 4.35) |
| 16 vấn đề, sửa 13, ba vấn đề nặng nhất | đoạn trước Bảng 4.33 |
| Không thử nghiệm với người dùng | quyết định của nhóm ngày 04/11/2026, câu ở 4.4.4 sau Bảng 4.33 |
| Bảng 5.3 dòng 1 và 5 (một nguồn OLTP, SCD Type 1, bốn mốc là tập phát triển, ngưỡng Youden lạc quan) | Bảng 3.0 cột Giới hạn |
| Quy tắc chọn đã chốt trước | mục 3.4.6, đoạn sau Bảng 4.12 |
| Nguồn là bản sao lưu tĩnh | mục 3.4.3 |
| 82,2% và 64,4% | Bảng 4.15 |
| Q1 đến Q4 | mục 2.2 trên thẻ Phần 345 |

### B3. Không dùng

- Thông tin của khách 26339 trong file kết quả (nhóm N1, kênh R3, EV 107,41 USD, gợi ý Helmets và Fenders) chưa có trong lời văn Chương 4 nên chưa đưa vào.
- Tên thủ tục ETL và dấu vân tay dữ liệu không có trong Chương 4 nên không nhắc.
