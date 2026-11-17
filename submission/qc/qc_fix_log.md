# Sửa sau QC — ảnh 003

- Học viên báo lỗi: box `three_wheeler` chưa ôm sát vật, ở img_003.jpg; QC release object #13, CVAT ServerID 3694; bản COCO sau sửa đánh ID mới #1.
- Học viên đã sửa trong CVAT và báo “đã save”. Task được lưu lúc 00:39:42 ngày 18/11/2026, giờ Việt Nam.
- Đối chiếu snapshot trước/sau: chỉ shape 3694 thay đổi, thuộc img_003.jpg. Box xyxy trước sửa: (243.30, 324.20)–(773.53, 623.98); sau sửa: (291.10, 324.20)–(737.40, 623.98).
- Xuất COCO bằng exporter gốc của CVAT; `submission/labels/qc_fixed.json` chỉ chứa ảnh 003 với đủ 22 đối tượng. `build_release.py` thay ảnh này trong release; 23 ảnh khác không thay đổi. Bản release vẫn có 24 ảnh, 539 đối tượng.
- `qc_review_before_fix.csv` và `qc_report_auto_before_fix.md` giữ kết quả trước sửa: 1/101 đối tượng lỗi; 1/5 ảnh lỗi (20%); script gợi ý REWORK.
- Tái kiểm: học viên xem ảnh trước/sau và xác nhận “Đã ôm sát, không thấy lỗi còn lại ở ảnh 003”. Phiếu hiện tại ghi 0/5 ảnh lỗi sau sửa; bốn ảnh khác dùng kết quả kiểm trước đó vì ảnh và nhãn giữ nguyên. Đây là tái kiểm có biết lỗi, không phải lấy mẫu độc lập mới. Kết quả lỗi trước sửa vẫn giữ nguyên.
- Bản gán gold, nhãn máy có bẫy và đáp án bẫy giữ nguyên SHA256. `batch_reviewed.json` và các vòng review được giữ riêng, không ghi đè bởi sửa QC.
