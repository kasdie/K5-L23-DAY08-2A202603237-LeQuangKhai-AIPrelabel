# Label contract — Phố châu Á — BỔ SUNG v1.1 — 2A202603237 - Lê Quang Khải

> Phần bổ sung dựa trên ba quyết định học viên đã nêu trong hội thoại. Giữ nguyên guideline v1.0 và mục `rules` trong taxonomy. Các ca áp dụng quy tắc cũ được ghi rõ, không coi đó là thay đổi lớp hoặc ngưỡng QC.

## 1. Câu hỏi mở đã chốt

| Câu hỏi từ v1.0 | Quyết định của học viên | Ảnh ví dụ | case_id |
|---|---|---|---|
| Câu 2: cụm xe đỗ dày ở gần camera | Tách từng xe khi còn phân biệt được, để tránh bỏ sót xe. Không dùng ignore_region cho cả cụm chỉ vì đỗ dày hoặc gần camera. Giữ nguyên ngưỡng vật cao dưới 20 px và điều kiện vùng không tách được cá thể ở v1.0. | img_018, img_024 | CAL-02 |

Các câu hỏi mở còn lại của v1.0 chưa có quyết định bổ sung từ học viên; không tự tạo quy tắc cho xe điện, hàng nhô ra, kính xe, độ che khuất hay ngưỡng chấp nhận không sửa. Khi gặp ca chưa rõ, đánh dấu can_review và cần chốt trước quyết định cuối cùng. Sau QC, học viên chưa nêu ca cụ thể đang giữ lại vì chưa rõ quy tắc và đã chọn Release cho lô hiện tại với giới hạn đã nêu trong REPORT.md. Các câu hỏi mở còn lại vẫn chưa được bổ sung quy tắc; khi gặp ca mới thuộc các tình huống đó cần đánh dấu can_review và xử lý trước khi chốt ca.

## 2. Ca khó từ lỗi máy và bẫy

| Ảnh | Tình huống đã được học viên xác nhận | Quyết định | Liên hệ v1.0 | case_id |
|---|---|---|---|---|
| img_009 | Vật thực tế là xe hai bánh; tham chiếu của script kỳ vọng three_wheeler. | Giữ motorbike. Ghi rõ sự khác nhau với tham chiếu máy khi đọc số đo bẫy. | Áp dụng định nghĩa motorbike ở mục 2; không đổi taxonomy hoặc đáp án bẫy. | CAL-01 |
| img_013 | Hai box person trùng trên cùng người áo hồng. | Giữ một box ôm phần nhìn thấy và xóa box trùng. | Áp dụng nguyên tắc mỗi người là một vật riêng; box của hai người khác nhau có thể chồng do che khuất. | CAL-03 |

## 3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do / nguồn |
|---|---|---|
| v1.0 | Giữ nguyên bản giảng viên | guideline_v1.0_label_contract.md |
| v1.1 | Làm rõ cách gán cụm xe gần camera khi còn tách được từng xe; ghi hai ca áp dụng quy tắc cũ | CAL-02 từ câu hỏi mở; CAL-01 và CAL-03 từ quan sát/quyết định học viên |
