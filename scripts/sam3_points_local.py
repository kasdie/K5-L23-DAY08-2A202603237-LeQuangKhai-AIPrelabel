"""SAM3 click/box prompts through the existing local interactor; no model download.

Uses the same coordinate convention as sam2_points.py. Saves an overlay and a
sidecar with actual prompts/timing. Visual observations are left to the student.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageDraw
import requests

from common import IMAGES_DIR, mask_to_polys
from sam2_points import pt, parse_box


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--pos", action="append", default=[])
    parser.add_argument("--neg", action="append", default=[])
    parser.add_argument("--box")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--note", default="")
    args = parser.parse_args()
    if Path(args.image).name != args.image or not (IMAGES_DIR / args.image).is_file():
        parser.error("--image must be a filename in data/images")
    if Path(args.name).name != args.name or args.name in (".", ".."):
        parser.error("--name must be a filename stem")
    source = IMAGES_DIR / args.image
    original = Image.open(source).convert("RGB")
    width, height = original.size
    positive, negative = [pt(s) for s in args.pos], [pt(s) for s in args.neg]
    if not positive:
        parser.error("Use at least one positive click for Part 5")
    for x, y in positive + negative:
        if not 0 <= x < width or not 0 <= y < height:
            parser.error("Click outside image")
    box = parse_box(args.box) if args.box else None
    if box and not (0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height):
        parser.error("Box outside image")
    session = requests.Session()
    session.trust_env = False
    response = session.get("http://127.0.0.1:8071/health", timeout=5)
    response.raise_for_status()
    health = response.json()
    if not health.get("ready") or health.get("model") != "SAM 3":
        raise SystemExit("SAM3 local is not ready")
    body = {"image": base64.b64encode(source.read_bytes()).decode(),
            "pos_points": positive, "neg_points": negative}
    if box:
        body["obj_bbox"] = [box[:2], box[2:]]
    started = time.perf_counter()
    response = session.post("http://127.0.0.1:8071/api/function_invocations", json=body,
                            headers={"x-nuclio-function-name": "local-sam3-apple-mps"}, timeout=180)
    response.raise_for_status()
    elapsed = time.perf_counter() - started
    mask = np.asarray(response.json()["mask"], dtype=np.uint8) > 0
    if mask.shape != (height, width) or not mask.any():
        raise SystemExit("SAM3 returned an empty mask or wrong dimensions")
    overlay = np.array(original).astype(np.float32)
    overlay[mask] = overlay[mask] * .45 + np.array([230, 25, 75]) * .55
    image = Image.fromarray(overlay.astype(np.uint8))
    draw = ImageDraw.Draw(image)
    for points, color in [(positive, "#00d050"), (negative, "#ff3030")]:
        for x, y in points:
            draw.ellipse([x-6, y-6, x+6, y+6], fill=color, outline="white", width=2)
    if box:
        draw.rectangle(box, outline="yellow", width=2)
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{args.name}.jpg"
    if target.exists():
        raise SystemExit(f"Output already exists; use a new --name to preserve prior evidence: {target}")
    image.save(target, quality=93)
    record = {"model": "SAM 3", "backend": "Ultralytics local interactor", "device": health["device"],
              "image": args.image, "image_size": [width, height], "positive_points": positive,
              "negative_points": negative, "box_xyxy": box,
              "click_count": len(positive) + len(negative), "seconds": round(elapsed, 3),
              "mask_pixels": int(mask.sum()), "polygons": mask_to_polys(mask.astype(np.uint8)),
              "positive_clicks_inside": [bool(mask[int(y), int(x)]) for x, y in positive],
              "negative_clicks_outside": [not bool(mask[int(y), int(x)]) for x, y in negative],
              "created_at_utc": datetime.now(timezone.utc).isoformat(), "note": args.note,
              "status": "model proposal; student visual review pending", "overlay": target.name}
    (args.out / f"{args.name}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
    print(json.dumps({k:record[k] for k in ["image", "click_count", "seconds", "mask_pixels", "positive_clicks_inside", "negative_clicks_outside", "status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
