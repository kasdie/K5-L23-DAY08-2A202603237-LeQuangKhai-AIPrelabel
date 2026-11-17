# Số đo review (det)

- Ảnh tính: 24 (batch,gold); box máy: 522; đối tượng sau duyệt: 543; ngưỡng accepted: IoU >= 0.9
- Đã **loại 24 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 409 | 409/522 = 78.4% | 522 box máy |
| edited (sửa) | 51 | 51/522 = 9.8% | 522 box máy |
| deleted (xoá) | 62 | 62/522 = 11.9% | 522 box máy |
| added (vẽ thêm) | 83 | 83/543 = 15.3% | 543 đối tượng sau duyệt |

Trong số deleted + added, **7 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 76.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 240 | 18 | 14 | 49 |
| bicycle | 5 | 1 | 2 | 1 |
| motorbike | 103 | 23 | 12 | 12 |
| car | 48 | 1 | 6 | 11 |
| bus | 2 | 0 | 0 | 2 |
| truck | 3 | 0 | 3 | 3 |
| three_wheeler | 8 | 8 | 25 | 5 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 45 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 35 | 39 | 10 | 47.3% (KTC 95%: 36–59%) | 77.8% (KTC 95%: 64–87%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*


(Ảnh gold không nằm trong nhãn sau duyệt: không tính residual / new error. Đó là chủ ý: duyệt lại ảnh bạn vừa tự gán tay sẽ đo trí nhớ, không đo thiên kiến.)

## 3. Ảnh bẫy
- Bắt được 8/12 = 66.7% (KTC 95%: 39–86%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - missing: 3/3
  - wrong_class: 1/3
  - loose: 2/3
  - extra: 2/3
  - lọt: img_024.jpg (wrong_class), img_008.jpg (wrong_class), img_018.jpg (extra), img_009.jpg (loose)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).
