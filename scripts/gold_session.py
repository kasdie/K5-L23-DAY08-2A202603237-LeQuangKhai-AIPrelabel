"""Part 1 helpers: measure manual work and validate/import a CVAT COCO export.

Does not inspect images, call models, or create annotations.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import io
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path(__file__).resolve().with_name("validate_labels.py")
GOLD_URL = "http://localhost:8080/tasks/37/jobs/36"
BATCH_URL = "http://localhost:8080/tasks/38/jobs/37"


def record_minutes(minutes: float, step: str = "gold_manual", images: int = 4) -> None:
    path = ROOT / "submission/time_log.csv"
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    matches = [r for r in rows if r["step"] == step]
    if len(matches) > 1:
        raise ValueError(f"time_log.csv có nhiều dòng {step}; giữ nguyên file để kiểm tra tay.")
    note = "measured timer; pauses excluded; " + datetime.now().astimezone().isoformat(timespec="seconds")
    if matches:
        row = matches[0]
        if row["images"] != str(images):
            raise ValueError(f"Dòng {step} cũ không ghi {images} ảnh; giữ nguyên để kiểm tra tay.")
        total = float(row["minutes"]) + minutes
        row.update(minutes=f"{total:.6f}", note=(row.get("note", "") + "; " + note).strip("; "))
    else:
        rows.append({"step": step, "images": str(images), "minutes": f"{minutes:.6f}", "note": note})
    backup = ROOT / "work/gold-session/time-log-backups"
    backup.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup / f"{time.time_ns()}.csv")
    pending = path.with_suffix(".csv.tmp")
    with pending.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["step", "images", "minutes", "note"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    pending.replace(path)


def timer(step: str = "gold_manual", images: int = 4, url: str = GOLD_URL) -> None:
    gold = step == "gold_manual"
    print("PART 1 — GOLD GÁN TAY: 4 ảnh, không AI" if gold else "PART 4 — REVIEW: 24 ảnh đã có nhãn máy")
    print("Đọc NEXT_STEPS.md và guideline/guideline_v1.0_label_contract.md trước khi bắt đầu." if gold
          else "Mỗi ảnh: ẩn nhãn, quét ảnh trước; hiện nhãn rồi sửa sót / thừa / sai lớp / box lỏng.")
    subprocess.run(["open", url], check=False)
    input("Đăng nhập CVAT, đọc quy tắc. Khi sẵn sàng làm, nhấn Enter để BẮT ĐẦU đo: ")
    elapsed = 0.0
    active_since = time.monotonic()
    events = []
    print("p = tạm dừng; r = tiếp tục; done = lưu thời gian phiên; q = bỏ phiên, không ghi time_log.")
    while True:
        command = input("Đang đo > " if active_since is not None else "Tạm dừng > ").strip().lower()
        now = time.monotonic()
        events.append({"at": datetime.now().astimezone().isoformat(), "command": command})
        if command == "p" and active_since is not None:
            elapsed += now - active_since
            active_since = None
            print(f"Đã đo {elapsed / 60:.2f} phút. Gõ r để tiếp tục.")
        elif command == "r" and active_since is None:
            active_since = now
        elif command in ("done", "q"):
            if active_since is not None:
                elapsed += now - active_since
            evidence = ROOT / "work/gold-session"
            evidence.mkdir(parents=True, exist_ok=True)
            journal = evidence / f"session-{time.time_ns()}.json"
            record = {
                "step": step, "images": images, "elapsed_seconds": elapsed,
                "saved_to_time_log": False, "events": events,
            }
            journal.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            if command == "q":
                print("Đã bỏ phiên; time_log.csv giữ nguyên.")
                return
            record_minutes(elapsed / 60, step, images)
            record["saved_to_time_log"] = True
            journal.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Đã cộng {elapsed / 60:.2f} phút đo thực tế vào submission/time_log.csv.")
            print(f"Nếu chưa xong cả {images} ảnh, mở lại công cụ để đo phiên tiếp theo; thời gian sẽ được cộng.")
            print("Khi hoàn tất: lưu CVAT, export COCO 1.0 (không ảnh), rồi mở Nhap-Gold.command." if gold
                  else "Lưu CVAT và báo đã review xong để xuất batch_reviewed.json trước khi chấm bẫy.")
            return
        else:
            print("Dùng p / r / done / q; các lệnh không tự đánh dấu bài đã hoàn thành.")


def import_gold(source: Path) -> None:
    from common import images_of

    if not source.is_file():
        raise ValueError(f"Không tìm thấy file: {source}")
    raw = source.read_bytes()
    if zipfile.is_zipfile(io.BytesIO(raw)):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            candidates = [n for n in archive.namelist() if Path(n).name == "instances_default.json"]
            if len(candidates) != 1:
                raise ValueError("ZIP phải chứa đúng một annotations/instances_default.json (COCO 1.0).")
            raw = archive.read(candidates[0])
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Nội dung phải là một đối tượng JSON COCO.")
    images = data.get("images", [])
    names = [Path(im["file_name"]).name for im in images]
    if len(names) != 4 or set(names) != set(images_of(["gold"])):
        raise ValueError("File phải chứa đúng 4 ảnh gold 001, 012, 020, 036; chưa ghi gì vào submission.")
    if not data.get("annotations"):
        raise ValueError("File chưa có annotation; hãy kiểm tra đã lưu và export đúng task gold-manual.")
    staging = ROOT / "work/gold-session"
    staging.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="validate-", dir=staging) as temp:
        candidate = Path(temp) / "gold_manual.json"
        candidate.write_bytes(raw)
        subprocess.run([sys.executable, str(VALIDATOR), str(candidate),
                        "--expect", "gold"], cwd=ROOT, check=True)
        target = ROOT / "submission/labels/gold_manual.json"
        if target.exists() and target.read_bytes() != raw:
            backup = staging / f"gold_manual-before-{time.time_ns()}.json"
            shutil.copy2(target, backup)
            print(f"Đã giữ bản cũ ở {backup.relative_to(ROOT)}")
        target.parent.mkdir(parents=True, exist_ok=True)
        pending = target.with_suffix(".json.tmp")
        pending.write_bytes(raw)
        pending.replace(target)
    print("Đã nhập submission/labels/gold_manual.json; kiểm tra cấu trúc COCO thành công.")
    print("Kiểm tra tự động không đánh giá box ôm sát hay lớp có đúng hình ảnh hay không.")
    print("Đã sẵn sàng chuyển sang GUIDE.md Part 2 sau khi bạn tự kiểm đủ 4 ảnh và time_log.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["timer", "review-timer", "import-gold"])
    parser.add_argument("file", nargs="?", type=Path)
    args = parser.parse_args()
    if args.action == "timer":
        timer()
    elif args.action == "review-timer":
        timer("batch_review", 24, BATCH_URL)
    else:
        source = args.file
        if source is None:
            text = input("Kéo file ZIP/JSON COCO vừa tải vào đây rồi Enter: ").strip()
            source = Path(text).expanduser()
            if not source.is_file():
                values = shlex.split(text)
                if len(values) != 1:
                    raise ValueError("Chọn đúng một file ZIP hoặc JSON.")
                source = Path(values[0]).expanduser()
        import_gold(source.resolve())


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nĐã dừng; chỉ phiên kết thúc bằng done mới ghi vào time_log.csv.")
        sys.exit(130)
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print(f"LỖI: {error}", file=sys.stderr)
        sys.exit(1)
