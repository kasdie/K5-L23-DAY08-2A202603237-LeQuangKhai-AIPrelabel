# Số đo review (det)

- Ảnh tính: 24 (batch,gold); box máy: 522; đối tượng sau duyệt: 537; ngưỡng accepted: IoU >= 0.9
- Đã **loại 23 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 422 | 422/522 = 80.8% | 522 box máy |
| edited (sửa) | 41 | 41/522 = 7.9% | 522 box máy |
| deleted (xoá) | 59 | 59/522 = 11.3% | 522 box máy |
| added (vẽ thêm) | 74 | 74/537 = 13.8% | 537 đối tượng sau duyệt |

Trong số deleted + added, **6 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 68.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 246 | 13 | 13 | 43 |
| bicycle | 5 | 1 | 2 | 1 |
| motorbike | 109 | 18 | 11 | 10 |
| car | 48 | 1 | 6 | 10 |
| bus | 2 | 0 | 0 | 2 |
| truck | 4 | 0 | 2 | 3 |
| three_wheeler | 8 | 8 | 25 | 5 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 45 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 35 | 39 | 10 | 47.3% (KTC 95%: 36–59%) | 77.8% (KTC 95%: 64–87%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*


(Ảnh gold không nằm trong nhãn sau duyệt: không tính residual / new error. Đó là chủ ý: duyệt lại ảnh bạn vừa tự gán tay sẽ đo trí nhớ, không đo thiên kiến.)

## 3. Ảnh bẫy
- Bắt được 5/12 = 41.7% (KTC 95%: 19–68%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - missing: 2/3
  - wrong_class: 1/3
  - loose: 1/3
  - extra: 1/3
  - lọt: img_034.jpg (missing), img_024.jpg (wrong_class), img_005.jpg (loose), img_008.jpg (wrong_class), img_025.jpg (extra), img_018.jpg (extra), img_009.jpg (loose)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).
