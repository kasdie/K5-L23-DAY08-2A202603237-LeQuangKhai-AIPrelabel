# Thông tin học viên

- Họ và tên: Lê Quang Khải
- MSHV: 2A202603237
- Lớp (L2 / L3 / khác): L2
- Tài khoản GitHub: kasdie
- Repo bài nộp (URL): https://github.com/kasdie/K5-L23-DAY08-2A202603237-LeQuangKhai-AIPrelabel
- Commit nội dung chốt bài (hash): đang tạo commit; sẽ ghi mã thật trong bước lưu metadata cuối.
- Máy: macOS, Apple M5 (MPS), RAM 16 GB
- CVAT (Docker): v2.74.1, http://localhost:8080

## Kết quả tóm tắt (điền cuối bài; số lấy từ `submission/qc/*`, kèm mẫu số)

- Vòng review 1 — Máy: accepted 422/522 = 80,8%; edited 41/522 = 7,9%; deleted 59/522 = 11,3%; added 74/537 = 13,8% (đã loại vùng bẫy theo script).
- So với gold: precision của **máy** 35/74 = 47,3%; recall 35/45 = 77,8% (4 ảnh gold; số từ script).
- Bắt bẫy vòng 1: 5/12 = 41,7%; bản nhãn và số đo vòng đầu được giữ riêng trước khi sửa theo danh sách bẫy lọt.
- Bắt bẫy vòng 2: 8/12 = 66,7% sau khi xem gợi ý ảnh/loại bẫy còn lọt; chưa đạt 10/12, cần xác minh thêm nhãn thực tế và các khác biệt so với box tham chiếu máy.
- Bắt bẫy vòng 3: 11/12 = 91,7%, đạt ngưỡng ít nhất 10/12; đây là vòng sửa sau gợi ý, không thay kết quả review mù lần đầu. Bản nhãn: 24 ảnh, 539 rectangle; còn khác biệt lớp với tham chiếu máy ở img_009.
- Thời gian do học viên báo: gold 15 phút/4 ảnh = 3,75 phút/ảnh; review vòng 1 20 phút/24 ảnh ≈ 0,83 phút/ảnh. Chưa gồm thời gian các vòng sửa tiếp theo, QC và calibration.
- Lỗi QC trước sửa: 1/5 = 20% theo ảnh; 1/101 ≈ 0,99% theo đối tượng. Sau học viên sửa và tái kiểm ảnh 003: 0/5 ảnh lỗi, 0/101 đối tượng lỗi. Cùng mẫu 5 ảnh, không phải mẫu độc lập mới; script đổi gợi ý từ REWORK sang RELEASE, học viên đã chọn Release với các kết quả và giới hạn đã nêu.
- **Quyết định:** Release, ngày 2026-11-18 — học viên chốt lô sau sửa và tái kiểm, QC hiện 0/5 ảnh lỗi, bắt bẫy sau gợi ý 11/12; giữ kết quả mù đầu 5/12 và giới hạn mẫu nhỏ, không coi là chứng minh toàn lô hết lỗi.
