# Thiết lập Day 08 trên máy Lê Quang Khải

> Tài liệu này ghi trạng thái tại thời điểm chuẩn bị môi trường ban đầu. Tiến độ và kết quả cuối bài xem [NEXT_STEPS.md](NEXT_STEPS.md) và [REPORT.md](submission/REPORT.md).

Ngày kiểm tra: 17/11/2026 (giờ Việt Nam). MSHV: `2A202603237`, lớp L2.

## Môi trường

- MacBook Air, Apple M5 (CPU 10 lõi, GPU 8 lõi), RAM 16 GB; GPU MPS hoạt động.
- Cài thư viện từ `requirements.txt` vào `.venv` riêng; không thay đổi môi trường các bài trước.
- Python 3.14.10, PyTorch 2.15.0, Ultralytics 8.4.215, Transformers 5.23.0.
- Python mới hơn dải 3.10–3.13 mà đề khuyến nghị. Máy có wheel tương thích và đã chạy inference thực tế; `check_env.py` vẫn giữ cảnh báo, không sửa bộ kiểm tra để bỏ cảnh báo.
- CVAT Docker **2.74.1**, đang chạy ở <http://localhost:8080>. Tài liệu lab minh họa phiên bản 2.81; tên nút giao diện có thể khác. Kiểm tra backend/API; chưa xác minh giao diện bằng trình duyệt tự động vì công cụ trình duyệt thiếu thành phần.

Kích hoạt từ thư mục repository:

```bash
source ./activate_lab.sh
python scripts/check_env.py --cvat http://localhost:8080
```

File kích hoạt đặt cache trong `work/runtime/`, Hugging Face trong `models/huggingface/`, bật fallback MPS khi cần và tắt tự cài thư viện ngầm. CLIP đã được cài riêng để YOLOE chạy được.

## Model

| Model | Nguồn | Trạng thái kiểm tra |
|---|---|---|
| YOLO26n | Tái dùng `../linh tinh/K5-L2-Day02-ObjectDetection/outputs/yolo26n.pt` bằng symlink trong `models/` | MPS: 15 box trên `img_011.jpg` |
| SAM3 | Tái dùng `../day03/sam3.pt` (~3.2 GiB), có bản thứ hai trong `~/Downloads/` | Dịch vụ local MPS ở cổng 8071 trả mask 682 × 1024, 4.951 pixel trên ảnh pilot |
| YOLO26m | Tải vào `models/yolo26m.pt` (~42 MB) | MPS: 30 box trên `img_011.jpg` |
| YOLOE-26s-seg | Tải vào `models/yoloe-26s-seg.pt` (~30 MB) | MPS: 1 box trên `img_011.jpg`; đã tải bộ mã hóa `mobileclip2_b.ts` (~242 MB) |
| SAM 2.1 base | Tải vào `models/sam2.1_b.pt` (~154 MB) | MPS: pipeline YOLO26 → SAM trả 2 box và 2 mask trên `img_011.jpg` |

Các lần chạy này là **smoke test kỹ thuật Part 0 trên ảnh pilot**, chưa thay cho Part 2, nhận xét bằng mắt, hay mask Part 5 của học viên. Kết quả nằm trong `work/smoke/`; không chép tự động vào `submission/model_log.csv` hoặc `submission/masks/`.

`pip check` báo `No broken requirements found`. YOLOE còn có `FutureWarning` từ `torch.jit.load` trên Python 3.14; lần chạy thực tế đã thành công. Phần thời gian nạp YOLOE lần đầu gồm khoảng 7,5 phút tải encoder, không dùng nó để so sánh tốc độ model.

SAM3 sẵn có là checkpoint dùng với **Ultralytics**. `prelabel.py --model sam3` của đề dùng **Transformers/Hugging Face**, cần cấu trúc model/config riêng và quyền Hugging Face; không truyền thẳng `sam3.pt` vào lệnh đó. Dịch vụ SAM3 đang chạy phục vụ click/box và tránh nạp thêm một model lớn vào RAM. SAM 2.1 dùng được trực tiếp với các lệnh chuẩn `--sam sam2.1_b.pt` của lab.

Symlink phụ thuộc file gốc ở bài trước: giữ file gốc nếu muốn tiếp tục dùng lại. Model và cache đã được `.gitignore` loại trừ.

## CVAT đã chuẩn bị

- [Project day08-2A202603237](http://localhost:8080/projects/3): đủ 8 lớp, kiểu `Any`; 7 lớp đối tượng có `conf` và `can_review`.
- [Task gold-manual, job 36](http://localhost:8080/tasks/37/jobs/36): 4 ảnh `001`, `012`, `020`, `036`.
- [Task batch-review, job 37](http://localhost:8080/tasks/38/jobs/37): 24 ảnh batch, chưa nạp pre-label.
- API xác nhận đúng số ảnh, đúng danh sách gold và cả hai task chưa có annotation tại thời điểm chuẩn bị.
- Dùng tài khoản local `hocvien` đang có để tạo project/task; không đọc mật khẩu, không tạo hoặc lưu token. Các project/task cũ được giữ nguyên.

## Việc làm tiếp theo

Hướng dẫn thao tác sẵn có trong [NEXT_STEPS.md](NEXT_STEPS.md). `Bat-dau-Gold.command` mở job gold và đồng hồ đo thời gian thực, loại trừ thời gian tạm dừng. `Nhap-Gold.command` nhận ZIP/JSON COCO, kiểm đúng 4 ảnh và cấu trúc bằng script của đề trước khi ghi nhãn. Guideline v1.0 đã được gắn vào Annotation Guide của project CVAT (guide 3) để đọc trong công cụ gán nhãn.

1. Đọc [guideline v1.0](guideline/guideline_v1.0_label_contract.md), mở task **gold-manual**, bấm giờ và tự gán rectangle cho 4 ảnh. Nhãn tay để trống `conf`; ca chưa chắc quy tắc tick `can_review`.
2. Export **COCO 1.0**, tắt **Save images**, lấy `annotations/instances_default.json` trong ZIP, đặt thành `submission/labels/gold_manual.json`. Ghi thời gian thật vào `submission/time_log.csv`, bước `gold_manual`, số ảnh `4`.
3. Kiểm tra gold bằng `python scripts/validate_labels.py --all`. Trước khi có nhãn batch, thông báo thiếu batch là công việc chưa làm, không phải lỗi môi trường.
4. Tiếp tục [GUIDE.md](GUIDE.md) Part 2: chạy tour YOLO26, YOLOE, SAM; xem `viz/` và tự ghi nhận xét. Sau đó mới chạy `--split all`, chọn ngưỡng, trộn bẫy và review batch.

Theo [RULES.md](RULES.md), gold phải được tự gán **trước AI**; không chạy model, xem pre-label hoặc hỏi AI nội dung 4 ảnh gold trước khi export. Không mở `traps_key.json` trước khi export nhãn batch đã review. Kết luận, calibration và quyết định Release/Hold/Rework do học viên viết từ số liệu thật.

Repo bài nộp được học viên xác nhận: <https://github.com/kasdie/K5-L23-DAY08-2A202603237-LeQuangKhai-AIPrelabel>. Repo public, tên đã đúng mẫu trong `SUBMISSION.md`; tài khoản trong `STUDENT.md` là `kasdie`. Remote `origin` trỏ tới repo bài nộp; nguồn đã clone trước đó được giữ ở remote `lab-source`. Trước khi nộp vẫn cần ít nhất 4 commit theo Part và hoàn tất các đầu ra bắt buộc. Chưa thực hiện push hoặc nộp bài.

## Bằng chứng kỹ thuật

- `work/setup/check_env.txt`: kết quả cuối **SẴN SÀNG**, import thư viện, GPU, 36 ảnh và kết nối CVAT.
- `work/setup/environment.json`, `work/setup/requirements-installed.txt`: phiên bản và nguồn model tái dùng.
- `work/setup/cvat-verified.json`: cấu hình project, danh sách ảnh và job.
- `work/setup/smoke-*.log`, `work/smoke/*/run.json`: tham số và đầu ra kiểm tra model.
- `work/` không commit theo quy định của đề. Thư mục `data/images/`, `data/split.csv`, mục `rules` của taxonomy và nội dung đáp án bẫy được giữ nguyên.
