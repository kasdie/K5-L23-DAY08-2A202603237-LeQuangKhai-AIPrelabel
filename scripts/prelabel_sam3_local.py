"""Use the existing local SAM3 interactor for the lab's box-to-mask pipeline.

Example:
  python scripts/prelabel_sam3_local.py --model yolo26 --size m \
    --images img_004.jpg img_013.jpg --classes person,motorbike,car \
    --conf 0.3 --segmenter sam --sam sam3.pt --out work/prelabel/t_sam3

Keeps the original prelabel.py unchanged. Uses its detection, taxonomy mapping,
COCO export, visualization and run logging, with SAM3 masks from localhost:8071.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

import numpy as np
from PIL import Image
import requests

from common import mask_to_polys
import prelabel

SERVICE = "http://127.0.0.1:8071"
FUNCTION = "local-sam3-apple-mps"


class LocalSam3Segmenter:
    def __init__(self, name: str, device: str):
        if Path(name).stem != "sam3":
            raise ValueError("This wrapper requires --sam sam3.pt")
        self.session = requests.Session()
        self.session.trust_env = False
        response = self.session.get(SERVICE + "/health", timeout=5)
        response.raise_for_status()
        health = response.json()
        if not health.get("ready") or health.get("model") != "SAM 3" or health.get("device") != device:
            raise RuntimeError(f"SAM3 local is not ready on requested device {device}: {health}")
        self.calls = []

    def masks_for(self, path: Path, boxes):
        if not boxes:
            return []
        with Image.open(path) as im:
            width, height = im.size
        encoded = base64.b64encode(path.read_bytes()).decode()
        polygons = []
        for index, box in enumerate(boxes, 1):
            x1, y1, x2, y2 = map(float, box)
            started = time.perf_counter()
            response = self.session.post(
                SERVICE + "/api/function_invocations",
                headers={"x-nuclio-function-name": FUNCTION},
                json={"image": encoded, "obj_bbox": [[x1, y1], [x2, y2]]},
                timeout=180,
            )
            response.raise_for_status()
            mask = np.asarray(response.json()["mask"], dtype=np.uint8)
            if mask.shape != (height, width):
                raise RuntimeError(f"Wrong mask shape for {path.name}: {mask.shape}")
            polygons.append(mask_to_polys(mask) or None)
            self.calls.append({
                "at_utc": datetime.now(timezone.utc).isoformat(),
                "model": "SAM 3", "backend": "existing local Ultralytics bridge",
                "device": "mps", "image": path.name, "box_xyxy": [x1, y1, x2, y2],
                "seconds": round(time.perf_counter() - started, 3), "mask_pixels": int(mask.sum()),
            })
            print(f"  SAM3 {path.name}: mask {index}/{len(boxes)}", flush=True)
        return polygons


def main() -> None:
    # Reuse the original CLI, but replace only its geometric segmenter.
    if "--segmenter" not in sys.argv or sys.argv[sys.argv.index("--segmenter") + 1] not in ("sam", "sam2"):
        raise SystemExit("Use --segmenter sam --sam sam3.pt with this wrapper")
    if "--sam" not in sys.argv:
        sys.argv.extend(["--sam", "sam3.pt"])
    instances = []

    def create_segmenter(name, device):
        result = LocalSam3Segmenter(name, device)
        instances.append(result)
        return result

    original = prelabel.Sam2Segmenter
    prelabel.Sam2Segmenter = create_segmenter
    try:
        prelabel.main()
    finally:
        prelabel.Sam2Segmenter = original
        if "--out" in sys.argv and instances:
            out = Path(sys.argv[sys.argv.index("--out") + 1])
            out.mkdir(parents=True, exist_ok=True)
            (out / "sam3-service-calls.json").write_text(json.dumps({
                "service": SERVICE, "function": FUNCTION,
                "calls": [call for instance in instances for call in instance.calls],
            }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
