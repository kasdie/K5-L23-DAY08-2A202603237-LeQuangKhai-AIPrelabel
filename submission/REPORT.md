# Báo cáo Day 08 — 2A202603237 - Lê Quang Khải

> Báo cáo được hoàn thiện từ các quan sát, lựa chọn và nội dung gợi ý học viên đã đọc và đồng ý. Số liệu lấy từ các file đầu ra được dẫn dưới đây; các giới hạn được giữ cùng kết quả.

## 1. Model và recipe (Part 2–3)

| Lớp | Model + cỡ | Ngưỡng | Vì sao (dẫn `run_id` trong `model_log.csv`) |
|---|---|---|---|
| person / bicycle / motorbike / car / bus / truck | YOLO26m | 0,3 mặc định theo script | Tour r05–r06; nguồn toàn bộ ảnh r09. Theo `qc/threshold_sweep.md`, person/motorbike/car không đạt recall mục tiêu 90% ở các ngưỡng thử; bicycle/bus/truck không có vật trong gold. Script giữ mặc định, không có bằng chứng đây là ngưỡng tối ưu. |
| three_wheeler | YOLOE-26s; tuk-tuk / cyclo / cargo tricycle | 0,15 theo script | Tour r07; nguồn toàn bộ ảnh r10. Script ghi recall 100%, precision khoảng 67% trên 6 vật gold ở ngưỡng 0,15; đây là căn cứ kỹ thuật của cấu hình đã chạy, cần kiểm tay vì học viên quan sát sai lớp. |

**Quyết định sau tour model** (đã ghi trong `model_log.csv`):

| Run | Kết quả đã quan sát | Quyết định của tôi |
|---|---|---|
| r05 — YOLO26m, conf 0,25 | Ảnh 011 có người/xe ở xa được khoanh, nhưng các box nhỏ chưa nhìn rõ để xác nhận. | Dùng làm cấu hình thử tạo nhãn gợi ý; kiểm lại các vật nhỏ trước khi giữ nhãn. |
| r06 — YOLO26m, conf 0,5 | So với 0,25, có cả người/xe thật bị loại. Chưa xác nhận được ưu điểm rõ ràng; ít box hơn không tự chứng minh chính xác hơn. | Không chọn 0,5 làm ngưỡng mặc định cho lượt gán gợi ý này. |
| r07 — YOLOE | Ảnh 011 box khá sát nhưng three_wheeler có vẻ nhầm loại xe. | Dùng để gợi ý xe ba bánh, con người kiểm lại loại xe trước khi giữ. |
| r08 — YOLO26 + SAM3 | Ảnh 013 mask nhìn chung bám sát, nhưng có lỗi vùng xe, box person trùng và sai phạm vi người ngồi trong xe. | Dùng SAM3 hỗ trợ tạo mask; kiểm vật đầu vào, tên lớp và box trùng, sửa box/prompt khi cần. |

Ngưỡng 0,25 và 0,5 là hai cấu hình tour; recipe gộp thực tế vẫn dùng YOLO26 mặc định 0,3 và three_wheeler 0,15 theo script. Không coi việc chọn ngưỡng là cách tự sửa nhãn sai lớp, hoặc coi mask đẹp là bằng chứng tên lớp đúng.

- Lệnh `merge_prelabels.py` đã dùng: `python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json --thr "three_wheeler=0.15" --conf 0.3 --iou 0.6 --split "batch,gold" --out work/prelabel/merged_review/pre.coco.json`
- **Phiên bản SAM đã chạy:** SAM3 qua Ultralytics local trên MPS, tái dùng checkpoint học viên đã có trên máy. Học viên muốn dùng SAM3 sẵn có; sau khi xem 3 kết quả Part 5, học viên xác nhận mask ôm sát vật được chọn, không lấy thêm người hoặc bỏ mất phần xe. Đây là quan sát trên 3 vật, không phải phép so sánh chất lượng với các phiên bản SAM khác.
- Quan sát sai lớp từ học viên: img_011, YOLOE gán three_wheeler cho vật học viên thấy có vẻ là xe khác. img_009, học viên xác nhận xe hai bánh và giữ motorbike dù tham chiếu bẫy kỳ vọng three_wheeler (CAL-01). Cách dùng AI do học viên chốt: cho máy gán trước rồi con người kiểm lại; không tin nhãn máy 100%, ưu tiên kiểm lớp dễ nhầm và cụm motorbike dày đặc.
- Quan sát học viên về điểm tin cậy: img_011, khi tăng từ 0,25 lên 0,5 có người/xe thật bị loại; các box nhỏ ở xa tại 0,25 chưa nhìn rõ để xác nhận. Ở img_013, học viên chỉ ra box person trùng người áo hồng và box sai phạm vi người ngồi trong xe; ảnh chụp học viên gửi có box person 0,91 ở khu vực này.
- Giới hạn phép đo: cùng 4 ảnh gold được dùng để quét ngưỡng và đo lại precision/recall, không có tập kiểm tra độc lập cho lựa chọn ngưỡng này. Các số đo trong bảng là in-sample và chỉ dựa trên 45 vật gold.

## 2. AI error profile (vòng 1, từ `qc/review_stats_round1.md`)

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | 422 | 80,8% | 522 box máy, vòng 1 |
| edited | 41 | 7,9% | 522 box máy, vòng 1 |
| deleted | 59 | 11,3% | 522 box máy, vòng 1 |
| added | 74 | 13,8% | 537 đối tượng sau duyệt, vòng 1 |

Theo script, 23 đối tượng nằm quanh vùng bẫy đã được loại khỏi profile trên để lỗi nhân tạo không bị tính thành chất lượng của model. Chỉ số bẫy được tính riêng. Trong deleted + added có 6 trường hợp đổi lớp theo phép ghép của script; vì vậy không coi toàn bộ 74 added là vật máy bỏ sót. Các con số phản ánh khác biệt nhãn theo quy ước ghép, vẫn phụ thuộc chất lượng nhãn sau duyệt.

- Ưu tiên kiểm theo nhận xét của học viên: three_wheeler vì dễ nhầm lớp (img_011; CAL-01 ở img_009), và motorbike khi xe xuất hiện dày đặc, box dễ chồng nhau (cụm xe ở img_018/img_024). Trong thống kê vòng 1, three_wheeler có 8 accepted, 8 edited và 25 deleted trên 41 box máy, tức 33/41 ≈ 80,5% không thuộc accepted — tỷ lệ cao nhất trong các lớp theo chỉ số này. Đây là trạng thái so với nhãn sau duyệt, không phải tỷ lệ lỗi đã được kiểm chứng độc lập; người duyệt vẫn có thể giữ hoặc tạo lỗi.
- So với gold: precision của **máy** = 35/74 = 47,3%; recall = 35/45 = 77,8% (45 đối tượng trong 4 ảnh gold). Số lấy từ `qc/review_stats_round1.json`.

## 3. Thiên kiến tự động hóa và ảnh bẫy

- Vòng 3: 11/12 = 91,7% (số từ `qc/review_stats_round3.json`), sau khi xem gợi ý; nhãn ở `labels/batch_reviewed_round3.json`. Các kiểm tra hình học không còn box dưới 20 px/vượt biên/gần trùng. Điểm còn khác tham chiếu là img_009: nhãn hiện motorbike, script kỳ vọng three_wheeler; học viên đã xác nhận vật thực tế là xe hai bánh và giữ motorbike (CAL-01).

- Số đo vòng 2 từ script: 8/12 = 66,7% sau khi đã xem gợi ý các ảnh/loại bẫy lọt. Nhãn giữ ở `labels/batch_reviewed_round2.json`; số đo ở `qc/review_stats_round2.*`. Chưa coi số này là kết quả review mù ban đầu. Hai khác biệt cần tự kiểm trên ảnh: img_008 đã đổi đúng person nhưng box khác kích thước tham chiếu (IoU 0,47); img_009 đang là motorbike trong khi bẫy kỳ vọng three_wheeler.

- Cách review vòng 1 do học viên mô tả: "Làm cả hai tùy ảnh" — sử dụng cả cách ẩn nhãn/quét ảnh gốc trước và cách xem/sửa các box đang hiện, tùy ảnh. Chưa kết luận riêng mô tả này là nguyên nhân khiến bẫy lọt.

- Bắt bẫy vòng 1: 5/12 = 41,7%; còn lọt 1 missing, 2 wrong_class, 2 loose, 2 extra (từ `qc/review_stats_round1.md`). Học viên chưa xác định được nguyên nhân cụ thể hoặc bước checklist đã bỏ qua. Không suy từ thống kê này rằng học viên chắc chắn tin máy quá mức; mô tả “làm cả hai tùy ảnh” cũng không cho biết từng ảnh đã được kiểm đủ các lượt hay chưa.
- Accepted 422/522 = 80,8% phản ánh độ giống giữa box máy và box sau duyệt theo phép ghép của script, không phải tỷ lệ nhãn đúng được kiểm chứng độc lập. Tôi chỉ bắt được 5/12 bẫy nên lần duyệt đầu vẫn còn lọt lỗi ở cả bốn nhóm. Một box sai mà tôi giữ gần nguyên vẫn có thể thuộc accepted. Tôi chưa xác định được nguyên nhân cụ thể; không tự nhận đã bỏ một bước kiểm nào khi chưa nhớ rõ. Tôi sẽ dùng quy trình hai lượt và checklist cụ thể ở mục 4 cho lần review sau, thay vì coi accepted cao là đủ để chốt chất lượng.

## 4. Máy có đáng dùng không?

- Thời gian (từ `time_log.csv`, học viên báo trong hội thoại): gold 15/4 = 3,75 phút/ảnh; review vòng 1 20/24 ≈ 0,83 phút/ảnh. Chưa có thời gian đo cho các vòng sửa tiếp theo, QC và calibration. Hai tập ảnh khác nhau và gold được làm trước; chưa đo riêng ảnh hưởng của độ quen cảnh, nên không dùng hai mức trung bình này để khẳng định mức tiết kiệm thời gian cho toàn quy trình.
- Kết luận học viên đã nêu: **AI đáng dùng** để gán trước, sau đó con người kiểm lại. Học viên yêu cầu kiểm kỹ three_wheeler và motorbike dày đặc vì dễ nhầm hoặc chồng box; không coi nhãn máy đúng 100%. Các số thực tế đi kèm: review đầu giữ 422/522 box theo phép ghép của script, nhưng chỉ bắt 5/12 bẫy; kết quả giữ nguyên box không thay thế kiểm chất lượng.
- **Ba quy tắc tôi chọn cho lần review sau:**
  1. Mỗi ảnh kiểm hai lượt: ẩn nhãn để tìm vật trước, sau đó hiện nhãn để đối chiếu các box đang có.
  2. Trước khi chuyển ảnh, kiểm đủ bốn nhóm: thiếu box, box thừa/trùng, sai tên lớp và sai phạm vi box. Chỉ gán các vật thỏa guideline; không thêm box cho mọi vật quá nhỏ ở xa.
  3. Kiểm riêng three_wheeler và cụm motorbike dày đặc; xác nhận loại xe bằng cấu tạo nhìn thấy. Nếu chưa rõ lớp hoặc quy tắc, đánh dấu can_review và ghi ca cần giải quyết, thay vì chọn nhãn để khớp máy.

Đây là kế hoạch tôi đã chọn sau khi xem kết quả và đọc phần giải thích; chưa có phép đo kiểm chứng hiệu quả của quy trình này, và không ghi là đã thực hiện đầy đủ trong lần review đầu.

## 5. Mask SAM cho 3 vật (Part 5)

| Ảnh | SAM (phiên bản) | Số click | Mask gồm người lái / hàng hoá? | Lỗi quan sát | File trong `masks/` |
|---|---|---|---|---|---|
| img_013.jpg | SAM3, Ultralytics local | 3 điểm prompt (2+/ 1−), chuẩn bị bằng script | Theo học viên: không gồm thêm người/nền ở vật được chọn | Không báo lỗi biên ở vật được chọn | `sam3_img013_tuktuk.jpg` |
| img_004.jpg | SAM3, Ultralytics local | 3 điểm prompt (2+/ 1−), chuẩn bị bằng script | Theo học viên: không gồm thêm người/nền ở vật được chọn | Không báo lỗi biên ở vật được chọn | `sam3_img_004_tuktuk.jpg` |
| img_017.jpg | SAM3, Ultralytics local | 2 điểm prompt (2+/ 0−), chuẩn bị bằng script | Theo học viên: không gồm thêm người/nền ở vật được chọn | Không báo lỗi biên ở vật được chọn (img_017 chỉ prompt 1 xe trong 3 xe)| `sam3_img_017_tuktuk.jpg` |

- Đối chiếu guideline mục 4.2: sau khi được giải thích về bám biên phần nhìn thấy và tách từng vật, học viên trả lời các quy tắc này “có giúp” và “model gán tốt, giúp nhìn vật thể dễ hơn”. Học viên vẫn ưu tiên kiểm lại lớp phân loại và lưu ý box không ôm sát tuy ít gặp vẫn có thể xảy ra. Kiểm biên mask và kiểm lớp là hai việc khác nhau; nhận xét trên không đồng nghĩa các box hoặc mask khác đều đúng. Học viên chưa nêu ca cụ thể còn vướng về người lái, kính hoặc hàng hóa; chưa bổ sung quy tắc cho những tình huống chưa được đánh giá.
- Các mask Part 5 được tạo bằng script gọi interactor SAM3 local; không có bằng chứng thao tác click của học viên trực tiếp trong giao diện CVAT cho ba ảnh này. Tọa độ prompt và số điểm thật được lưu ở JSON cùng tên ảnh. Mỗi kết quả chọn một vật, không yêu cầu tô mọi vật trong ảnh.

## 6. Calibration (Part 6)

- Số quyết định đã ghi: 3 (`calibration_decisions.csv`, CAL-01–CAL-03), chép từ phản hồi của học viên. Học viên ưu tiên CAL-01 (xe hai bánh ở img_009) và CAL-03 (xóa box trùng người áo hồng), vì quan tâm đến ảnh hưởng của lỗi nhận diện sai lớp và box trùng đối với ứng dụng xe tự lái. Lab này chưa đo tác động đến vận hành xe; đây là lý do ưu tiên của học viên.
- Bổ sung v1.1: CAL-02 làm rõ cụm xe gần camera vẫn tách từng xe khi còn phân biệt được; CAL-01 và CAL-03 ghi cách áp dụng quy tắc cũ cho xe hai bánh và box trùng, theo quyết định học viên.
- Nguồn ca trong bảng calibration: CAL-01 và CAL-03 từ lỗi máy/tham chiếu máy được học viên kiểm lại; CAL-02 từ câu hỏi mở của guideline về cụm xe đỗ gần camera. Chưa có bằng chứng để quy toàn bộ bẫy lọt cho việc chưa nắm guideline.

## 7. QC và quyết định (Part 6)

- Mẫu QC: 5 ảnh, 101 đối tượng (0 ảnh `can_review` + 5 ảnh ngẫu nhiên, seed 42); học viên kiểm. Hạn chế thiết kế: cùng người đã review lô trước đó, không phải đánh giá độc lập.
- QC trước sửa: 1/101 ≈ 0,99% đối tượng lỗi; 1/5 = 20% ảnh lỗi. Sau khi học viên sửa box ảnh 003 và tái kiểm xác nhận ôm sát: **0/101 = 0% đối tượng lỗi; 0/5 = 0% ảnh lỗi** (ngưỡng Release ≤ 2% theo ảnh). Kết quả trước sửa giữ ở `qc/qc_review_before_fix.csv` và `qc/qc_report_auto_before_fix.md`; kết quả hiện tại ở `qc/qc_review.csv`, script tính trong `qc/qc_report_auto.md`.
- Lỗi trước sửa: sai vị trí/kích thước, 1 trường hợp ở img_003.jpg, three_wheeler #13 trên ảnh QC cũ (CVAT ServerID 3694), box chưa ôm sát vật theo học viên. Học viên đã Save bản sửa và xác nhận qua ảnh so sánh: “Đã ôm sát, không thấy lỗi còn lại ở ảnh 003”. Box hiện là #1 trong COCO mới. Bốn ảnh 006, 014, 031, 035 không thay đổi nhãn và giữ kết quả học viên đã kiểm không thấy lỗi. `labels/qc_fixed.json` chứa 1 ảnh / 22 đối tượng, được `build_release.py` dùng thay img_003; release vẫn 24 ảnh / 539 đối tượng. Chi tiết ở `qc/qc_fix_log.md`.
- **Giới hạn mẫu nhỏ**: cận trên 95% Wilson do script tính khoảng 62% trước sửa (1/5) và 43% sau sửa (0/5). Mẫu 5 ảnh không chứng minh được tỉ lệ lỗi thật của cả lô ≤ 2%. Lần sau sửa là tái kiểm cùng mẫu có biết lỗi, không phải kiểm mù hoặc mẫu độc lập mới; con số Wilson không khắc phục được thiên lệch này.
- Script kiểm được cấu trúc COCO, lớp thuộc taxonomy, box vượt biên, vật nhỏ và các phép ghép hình học với tham chiếu. Script QC đếm kết quả học viên nhập; không tự xác nhận box ôm sát hay phát hiện vật mà cả máy và người cùng bỏ sót. Việc kiểm bằng mắt vẫn cần thiết.

- Gợi ý tự động: trước sửa **REWORK** vì 20% ảnh mẫu có lỗi > 2%; sau sửa và học viên tái kiểm, **RELEASE** vì phiếu hiện ghi 0/5 ảnh lỗi và thống kê bẫy vòng 3 là 11/12. Gợi ý của script được đọc cùng quyết định cá nhân dưới đây; kết quả này không chứng minh chất lượng toàn lô hoặc thay kết quả bắt bẫy mù lần đầu 5/12. Chưa thực hiện gán lại mù để đo độ nhất quán.

**Quyết định của học viên: Release**, ngày **2026-11-18**. Học viên chọn: “Release — chốt lô hiện tại với các kết quả và giới hạn đã nêu”, sau khi được giải thích cây quyết định QC và nhận khuyến nghị của Codex.

Căn cứ của lựa chọn đã được học viên chấp nhận: lỗi QC đã sửa và tái kiểm; phiếu hiện ghi 0/5 ảnh lỗi, 0/101 đối tượng lỗi; thống kê bẫy sau gợi ý là 11/12, vượt mức 10/12 của lab. Không có ảnh hỏng hoặc ca đang giữ lại vì chưa rõ quy tắc được ghi trong phiếu QC. Quyết định áp dụng cho lô bài lab hiện tại và giữ nguyên các giới hạn: lần mù đầu chỉ đạt 5/12, tái kiểm cùng mẫu đã biết lỗi, mẫu nhỏ chưa chứng minh tỷ lệ lỗi toàn lô ≤ 2%, và các câu hỏi mở chưa được đánh giá không tự coi là đã giải quyết.

Nếu kiểm bổ sung phát hiện ca chưa rõ quy tắc hoặc lỗi mới, cần ghi lại, xử lý ca đó và chạy lại QC trước khi thay quyết định. Chưa thực hiện thêm vòng kiểm độc lập hoặc gán lại mù.

## 8. Ghi chú cá nhân

- **Dùng AI để làm bài:** Codex hỗ trợ đọc yêu cầu, tìm model sẵn có, cài môi trường, chạy script, kiểm tra kỹ thuật, chuẩn bị tiện ích đo giờ/nhập COCO và trình bày báo cáo từ phản hồi học viên. Codex giải thích ý nghĩa accepted, tỷ lệ bắt bẫy, quy tắc mask và cây quyết định QC khi học viên yêu cầu gợi ý; không coi giả thuyết do AI giải thích là nguyên nhân học viên đã xác nhận. Bằng chứng kỹ thuật: `LOCAL_SETUP.md`, `work/setup/` và `work/smoke/`. Học viên thực hiện gán gold, review, kiểm bằng mắt và nêu các quyết định calibration; kết luận cuối được ghi theo lựa chọn của học viên. Sau khi đọc bản giải thích và gợi ý bổ sung, học viên xác nhận “ý tôi cũng giống như bạn, hãy hoàn thiện báo cáo giúp tôi”; các quyết định r05–r08 và kế hoạch review hai lượt được đưa vào theo sự đồng ý đó. Không tạo thêm số đo hoặc tự xác định nguyên nhân bẫy lọt.
- Gold: học viên xác nhận “tôi không xem nhãn AI của 4 ảnh gold trước khi gán tay”. Bản gold được export trước khi chạy model trên toàn bộ dữ liệu; đã giữ nguyên SHA256 qua các vòng review và QC. Phần chọn ngưỡng vẫn dùng chính gold nên có giới hạn in-sample như mục 1.
- Lưu lịch sử review: `labels/batch_reviewed_round1.json` và `qc/review_stats_round1.*` giữ nguyên lần đầu, export trước khi xem thống kê bẫy; vòng sửa tiếp theo được ghi riêng vì đã biết ảnh/loại bẫy lọt.
- Tiện ích kỹ thuật bổ sung: `scripts/prelabel_sam3_local.py` dùng SAM3 Ultralytics qua dịch vụ local cho box → mask; giữ nguyên `prelabel.py`. Gold đã export trước khi chạy model trên toàn bộ dữ liệu. `time_log.csv` ghi 15 phút gold do học viên báo, không phải đo bằng tiện ích Terminal.
- Máy / GPU / CVAT dùng: macOS, Apple M5, RAM 16 GB, GPU MPS; CVAT Docker v2.74.1 (tài liệu lab minh họa v2.81). Python 3.14.10 mới hơn dải 3.10–3.13 khuyến nghị; kiểm tra bằng chạy model thực tế. Chi tiết kỹ thuật ở `LOCAL_SETUP.md`.
- Dùng cache `data/cache/` thay vì tự chạy: không; các lượt pre-label và SAM3 đã chạy thật, có run.json/log và tọa độ prompt. Các lượt chạy được Codex thực hiện theo yêu cầu, nhận xét do học viên xem và cung cấp.
- Khác biệt kỹ thuật với script gốc: dùng wrapper SAM3 local để tái dùng checkpoint Ultralytics; không đổi script chấm. Bẫy ở img_009 dùng lớp tham chiếu three_wheeler, trong khi học viên xác nhận xe hai bánh nên giữ motorbike; số đo vẫn giữ đúng đầu ra gốc 11/12.
- Điều tôi làm khác ở lần sau: dùng quy trình hai lượt cho từng ảnh và checklist bốn nhóm lỗi trước khi chuyển ảnh; kiểm kỹ lớp dễ nhầm, đặc biệt three_wheeler và cụm motorbike dày đặc. Tôi chọn các bước này sau khi đọc phần gợi ý; hiệu quả cần được đo ở lần review tiếp theo.
