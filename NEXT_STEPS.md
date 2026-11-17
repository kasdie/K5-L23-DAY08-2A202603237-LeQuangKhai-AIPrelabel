# Trạng thái Day 08 — Lê Quang Khải, 2A202603237, L2

Học viên đã chọn **Release** ngày **18/11/2026** cho lô bài lab hiện tại, với các kết quả và giới hạn đã nêu trong [REPORT.md](submission/REPORT.md).

## Nội dung đã hoàn thành

- Gold tự gán: 4 ảnh, 45 đối tượng; học viên xác nhận chưa xem nhãn AI trước khi gán tay. Bản gold giữ nguyên qua các vòng xử lý.
- Tour YOLO26, YOLOE và SAM3 chạy thực trên máy. Log có nguồn từ các lượt chạy thật, không dùng cache thay cho chạy model. Các quyết định r05–r08 và nhận xét r06 đã được học viên đọc, đồng ý và điền đủ; kế hoạch kiểm hai lượt được ghi là cải tiến cho lần sau.
- Chọn ngưỡng bằng script trên gold; bảng ngưỡng ghi rõ lớp thiếu mẫu hoặc chưa đạt recall mục tiêu. Phép đo dùng cùng gold để chọn và chấm ngưỡng, không phải kiểm tra độc lập.
- Phân tích bẫy lọt đã bổ sung tự đánh giá của học viên: chưa đọc kỹ tên lớp, chưa kiểm đủ bốn cạnh và khó quan sát khi box chồng nhau; phân biệt rõ bẫy do script tạo với lỗi dự đoán tự nhiên của model.
- Batch review: 24 ảnh, 539 đối tượng. Giữ riêng các vòng bắt bẫy 5/12 → 8/12 → 11/12. Hai vòng sau đã có gợi ý; không thay kết quả mù đầu bằng kết quả sau sửa.
- 3 mask SAM3 ở ảnh 004, 013, 017 đã được học viên xem và nhận xét. Tọa độ prompt do script chuẩn bị; không ghi là học viên tự click trong CVAT. Mỗi phép thử chọn một xe.
- 3 quyết định calibration do học viên chốt đã vào guideline v1.1; mục `rules` trong taxonomy giữ nguyên.
- Lỗi box three_wheeler ở ảnh 003 đã được học viên sửa, Save và tái kiểm xác nhận ôm sát. CVAT ServerID 3694 giữ nguyên, COCO ID đổi từ #13 sang #1 sau xuất. `qc_fixed.json` chứa ảnh 003 / 22 đối tượng để thay đúng ảnh này trong release; 23 ảnh khác giữ nguyên.
- QC trước sửa: 1/5 ảnh lỗi, 1/101 đối tượng lỗi. Sau sửa: 0/5 ảnh lỗi, 0/101 đối tượng lỗi. Mẫu được dùng lại, không phải kiểm độc lập mới; cận trên Wilson 95% của script khoảng 43% chưa chứng minh toàn lô đạt lỗi ≤ 2%.
- Báo cáo ghi đúng thời gian học viên đã báo: 15 phút gold, 20 phút review đầu. Chưa có số đo cho các vòng sửa tiếp theo, QC và calibration; không tự ước lượng.

## File để xem lại

- [Thông tin học viên](STUDENT.md), [báo cáo](submission/REPORT.md).
- [Nhãn cuối](submission/release/final_det.coco.json), [manifest](submission/release/release_manifest.json), [báo cáo QC](submission/qc/qc_report_auto.md), [lịch sử sửa QC](submission/qc/qc_fix_log.md).
- [Guideline v1.1](submission/guidelines/guideline_v1.1_calibrated.md), [model log](submission/model_log.csv), [time log](submission/time_log.csv).
- Khi server local còn chạy: [trang mask và QC](http://127.0.0.1:8768/work/part6/review.html), [ảnh 003 trước/sau sửa](http://127.0.0.1:8768/work/part6/qc_fix_review.html).
- CVAT: [gold](http://localhost:8080/tasks/37/jobs/36), [batch](http://localhost:8080/tasks/38/jobs/37). Không cần nạp lại pre-label vì sẽ ảnh hưởng phần đã sửa.

## Kiểm tra và nộp

Trong thư mục repo, chạy:

```bash
source ./activate_lab.sh
python scripts/validate_labels.py --all
python scripts/validate_labels.py submission/labels/qc_fixed.json
python scripts/validate_labels.py submission/release/final_det.coco.json --expect batch
python scripts/check_submission.py
```

Bộ test workflow đã qua 12/12; kiểm cấu trúc và kiểm đủ file không xác nhận thay chất lượng nội dung nhãn.

Các Part đã được lưu bằng commit local với tên/tài khoản GitHub của học viên. Repo đích: [kasdie/K5-L23-DAY08-2A202603237-LeQuangKhai-AIPrelabel](https://github.com/kasdie/K5-L23-DAY08-2A202603237-LeQuangKhai-AIPrelabel). Nhánh main là bản bài nộp; trước khi nộp, đối chiếu commit trên GitHub với bản cuối. Học viên tự nộp link trên LMS theo yêu cầu, thao tác LMS không thuộc phần Codex thực hiện. Không commit `work/`, trọng số hoặc token.
