# Bổ sung cuối mục 4.3.2 (dán sau Hình 4.16)
> File này SINH TỰ ĐỘNG bởi `python/tao_huong_dan.py` từ số liệu đã chạy. Không sửa tay, số bảng và số hình lấy từ `python/so_bang_hinh.py`.

Mục 3.4.2 hẹn chọn tập thuộc tính dựa trên kiểm tra tương quan và so sánh mô hình, đồng thời kiểm tra mức hữu ích của NSub. Mục 3.4.1 hẹn phân tích độ nhạy với nhãn 180 ngày. Phần cuối mục này trình bày ba kiểm tra đó.

Bảng 4.11 liệt kê các cặp thuộc tính có hệ số tương quan hạng Spearman trung bình trên năm mốc huấn luyện từ 0,7 trở lên, là cách phát hiện thuộc tính dư thừa trước khi chọn tập con thuộc tính [3]. Có 8 cặp như vậy. Recency gần như nghịch đảo của Orders90 và Orders180 (ρ lần lượt −0,85 và −0,83), Share_Bikes trùng thông tin với BikeBuyer và Share_Accessories, Monetary tương quan với BikeBuyer và Tenure. Vì vậy Naive Bayes chỉ dùng năm thuộc tính Recency, Frequency, Monetary, BikeBuyer và NSub (Bảng 3.10). Trong năm thuộc tính này, cặp Monetary và BikeBuyer vẫn phụ thuộc mạnh sau khi rời rạc hóa (Cramér V = 0,92), tức giả định độc lập có điều kiện của Naive Bayes bị vi phạm ở cặp này, nên khi đọc bảng xác suất có điều kiện ở mục 4.3.4 cần đọc hai thuộc tính này cùng nhau.

*Bảng 4.11. Các cặp thuộc tính có tương quan hạng Spearman mạnh (|ρ| ≥ 0,7), trung bình năm mốc huấn luyện*

| Thuộc tính 1 | Thuộc tính 2 | ρ trung bình | ρ thấp nhất | ρ cao nhất |
|---|---|---|---|---|
| Share_Bikes | BikeBuyer | 0,87 | 0,83 | 0,91 |
| Share_Bikes | Share_Accessories | −0,87 | −0,90 | −0,82 |
| Recency | Orders90 | −0,85 | −0,86 | −0,82 |
| Recency | Orders180 | −0,83 | −0,86 | −0,81 |
| Monetary | BikeBuyer | 0,81 | 0,73 | 0,86 |
| Monetary | Tenure | 0,76 | 0,70 | 0,78 |
| Share_Accessories | BikeBuyer | −0,76 | −0,76 | −0,74 |
| Tenure | Share_Bikes | 0,72 | 0,68 | 0,75 |

Bảng 4.12 so sánh Naive Bayes với các tập thuộc tính khác theo cùng giao thức bốn fold. Bỏ NSub làm ROC-AUC giảm từ 0,720 xuống 0,701, Brier tăng từ 0,125 lên 0,133, Z giảm 2.577 USD và mô hình không còn đạt điều kiện 1 ở fold nào, nên NSub là thuộc tính hữu ích như mục 3.4.2 dự kiến. Trong cây đối chứng NSub có độ quan trọng Gini bằng 0 vì cây sâu 4 dùng hết các phép tách cho Recency (0,83) và Monetary (0,12), nên giá trị của NSub chỉ thể hiện qua Naive Bayes. Bỏ BikeBuyer cho ROC-AUC 0,729 và Brier 0,124, nhỉnh hơn thiết kế, còn Z thấp hơn 830 USD và chỉ cao hơn thiết kế ở 1/4 fold. Chênh lệch này nhỏ hơn mức dao động Z giữa các fold, nên hai tập được xem là tương đương. Thêm Tenure hoặc Orders180 làm ROC-AUC tăng nhưng Brier xấu đi và Z giảm 8.093 và 11.215 USD, phù hợp với tương quan mạnh của hai thuộc tính này với Monetary và Recency ở Bảng 4.11. Nhóm giữ tập thiết kế vì quy tắc chọn đã chốt trước ở mục 3.4.6 (trong các tập đạt ba điều kiện, chọn tập có Z cao nhất) và để tránh chọn lại cấu hình trên chính bốn fold phát triển (mục 3.4.4). Bỏ bớt một trong các thuộc tính BikeBuyer, Frequency, Monetary chỉ làm Z đổi dưới 1%, nên kết luận chọn mô hình không phụ thuộc vào lựa chọn này.

*Bảng 4.12. Naive Bayes theo tập thuộc tính, trung bình bốn fold (ĐK: số fold đạt điều kiện 1, 2, 3 của mục 3.4.6)*

| Tập thuộc tính | ROC-AUC | Brier | Z (USD) | Chênh Z so với thiết kế (USD) | Số fold Z cao hơn thiết kế | ĐK1 | ĐK2 | ĐK3 |
|---|---|---|---|---|---|---|---|---|
| Thiết kế: R, F, M, BikeBuyer, NSub | 0,720 | 0,125 | 291.883 | 0 | – | 4/4 | 4/4 | 4/4 |
| Bỏ NSub | 0,701 | 0,133 | 289.306 | −2.577 | 0/4 | 0/4 | 4/4 | 4/4 |
| Bỏ BikeBuyer | 0,729 | 0,124 | 291.053 | −830 | 1/4 | 4/4 | 4/4 | 4/4 |
| Bỏ Frequency | 0,725 | 0,124 | 291.340 | −543 | 2/4 | 4/4 | 4/4 | 4/4 |
| Bỏ Monetary | 0,722 | 0,123 | 289.869 | −2.014 | 2/4 | 4/4 | 4/4 | 4/4 |
| Chỉ R, F, M | 0,708 | 0,131 | 287.457 | −4.426 | 0/4 | 2/4 | 4/4 | 4/4 |
| Thêm Tenure (tứ phân vị) | 0,732 | 0,131 | 283.791 | −8.093 | 1/4 | 4/4 | 4/4 | 4/4 |
| Thêm Orders180 (0, 1, ≥ 2) | 0,727 | 0,137 | 280.668 | −11.215 | 0/4 | 4/4 | 4/4 | 4/4 |

Mục 3.4.1 lưu ý nhãn y = 1 gồm cả khách đã bỏ đi lẫn khách chưa đến kỳ mua. Bảng 4.13 so sánh nhãn 90 ngày với nhãn 180 ngày tại 13 mốc từ 01/06/2013 đến 01/12/2013, là các mốc có cửa sổ 180 ngày kết thúc trước 01/06/2014. Tỷ lệ y = 1 trung bình giảm từ 80,8% xuống 59,6%, và 26,2% số khách bị gắn y = 1 theo nhãn 90 ngày có mua lại trong khoảng ngày thứ 90 đến 180. Như vậy khoảng một phần tư nhóm "không mua lại trong 90 ngày" thực ra là khách chưa đến kỳ.

*Bảng 4.13. Tỷ lệ y = 1 theo nhãn 90 ngày và 180 ngày tại các mốc có đủ cửa sổ 180 ngày*

| Mốc T | Số khách | Tỷ lệ y = 1 (90 ngày) | Tỷ lệ y = 1 (180 ngày) | Khách y = 1 (90 ngày) mua lại trong ngày 90–180 | Tỷ lệ chưa đến kỳ |
|---|---|---|---|---|---|
| 01/06/2013 | 5.324 | 82,8% | 60,1% | 1.205 | 27,4% |
| 15/06/2013 | 5.423 | 82,6% | 59,1% | 1.271 | 28,4% |
| 01/07/2013 | 5.536 | 82,2% | 57,5% | 1.363 | 30,0% |
| 15/07/2013 | 5.889 | 82,0% | 57,2% | 1.457 | 30,2% |
| 01/08/2013 | 6.529 | 81,5% | 57,6% | 1.563 | 29,4% |
| 15/08/2013 | 7.077 | 80,3% | 58,3% | 1.555 | 27,4% |
| 01/09/2013 | 7.705 | 79,5% | 59,1% | 1.572 | 25,7% |
| 15/09/2013 | 8.249 | 79,6% | 59,7% | 1.640 | 25,0% |
| 01/10/2013 | 8.812 | 79,4% | 59,9% | 1.720 | 24,6% |
| 15/10/2013 | 9.305 | 79,3% | 60,0% | 1.795 | 24,3% |
| 01/11/2013 | 9.898 | 79,3% | 60,8% | 1.835 | 23,4% |
| 15/11/2013 | 10.447 | 80,7% | 62,5% | 1.899 | 22,5% |
| 01/12/2013 | 11.055 | 81,4% | 63,4% | 1.986 | 22,1% |

Bảng 4.14 đối chiếu điểm của ba mô hình học theo nhãn 90 ngày, đúng giao thức T + 97 ≤ E, với cả hai nhãn tại ba mốc đánh giá 01/11/2013, 15/11/2013 và 01/12/2013 (các mốc này sớm hơn bốn fold phát triển vì cửa sổ 180 ngày phải kết thúc trước 01/06/2014). ROC-AUC trung bình của Naive Bayes tăng từ 0,694 lên 0,752 khi đối chiếu với nhãn 180 ngày, tức điểm rủi ro xếp hạng tốt hơn với hành vi không mua lại kéo dài. Quy tắc Recency đảo chiều tăng tương tự (0,693 lên 0,759) và nhỉnh hơn Naive Bayes một chút ở nhãn 180 ngày, còn cây đối chứng tăng ít hơn (0,653 lên 0,678). Không thể huấn luyện và đánh giá thẳng một mô hình với nhãn 180 ngày vì cần đồng thời T + 187 ≤ E và E + 180 ≤ 01/06/2014, tức T phải trước mốc đầu tiên 01/06/2013, và tại mốc 01/06/2013 toàn bộ khách mới có một đơn, đều mua xe đạp và đều có NSub = 1 nên không có gì để học. Vì vậy nhãn 90 ngày được giữ, và DSS coi RiskScore là khả năng không mua lại trong kỳ tới chứ không phải xác suất khách rời bỏ hẳn.

*Bảng 4.14. Khả năng xếp hạng của mô hình học theo nhãn 90 ngày khi đối chiếu với nhãn 180 ngày*

| Mốc E | Mốc T | Mô hình | ROC-AUC (nhãn 90) | ROC-AUC (nhãn 180) | AP (nhãn 90) | AP (nhãn 180) |
|---|---|---|---|---|---|---|
| 01/11/2013 | 15/07/2013 | Naive Bayes (nhãn 90 ngày, thiết kế) | 0,683 | 0,739 | 0,866 | 0,753 |
| 01/11/2013 | 15/07/2013 | Cây Gini (nhãn 90 ngày) | 0,612 | 0,630 | 0,849 | 0,718 |
| 01/11/2013 | 15/07/2013 | Recency đảo chiều | 0,686 | 0,745 | 0,874 | 0,775 |
| 15/11/2013 | 01/08/2013 | Naive Bayes (nhãn 90 ngày, thiết kế) | 0,691 | 0,744 | 0,877 | 0,776 |
| 15/11/2013 | 01/08/2013 | Cây Gini (nhãn 90 ngày) | 0,673 | 0,696 | 0,876 | 0,761 |
| 15/11/2013 | 01/08/2013 | Recency đảo chiều | 0,691 | 0,759 | 0,883 | 0,796 |
| 01/12/2013 | 15/08/2013 | Naive Bayes (nhãn 90 ngày, thiết kế) | 0,707 | 0,773 | 0,890 | 0,807 |
| 01/12/2013 | 15/08/2013 | Cây Gini (nhãn 90 ngày) | 0,673 | 0,709 | 0,882 | 0,783 |
| 01/12/2013 | 15/08/2013 | Recency đảo chiều | 0,701 | 0,773 | 0,890 | 0,804 |
