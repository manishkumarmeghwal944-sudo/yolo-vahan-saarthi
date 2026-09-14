"""Vehicle detection using Ultralytics YOLO.

Examples:
    python src/detection.py --source 0
    python src/detection.py --source path/to/image.jpg
    python src/detection.py --source path/to/video.mp4
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


# COCO vehicle classes used by the default YOLO model.
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect vehicles with YOLO.")
    parser.add_argument(
        "--source",
        default="0",
        help="Image/video path or webcam index (default: 0).",
    )
    parser.add_argument(
        "--model",
        default="yolo11n.pt",
        help="Ultralytics YOLO model to use (default: yolo11n.pt).",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Minimum confidence threshold (default: 0.35).",
    )
    parser.add_argument(
        "--output",
        default="runs/detect",
        help="Directory for saved detection results.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    source: str | int = int(args.source) if args.source.isdigit() else args.source
    Path(args.output).mkdir(parents=True, exist_ok=True)

    model = YOLO(args.model)

    results = model.predict(
        source=source,
        conf=args.conf,
        classes=list(VEHICLE_CLASSES),
        save=True,
        project=args.output,
        name="vehicle_detection",
        exist_ok=True,
    )

    total = 0
    counts = {name: 0 for name in VEHICLE_CLASSES.values()}

    for result in results:
        if result.boxes is None:
            continue
        for class_id in result.boxes.cls.tolist():
            name = VEHICLE_CLASSES.get(int(class_id))
            if name:
                counts[name] += 1
                total += 1

    print("\nVehicle Detection Summary")
    print("-------------------------")
    for name, count in counts.items():
        print(f"{name.capitalize():12}: {count}")
    print(f"Total        : {total}")
    print(f"Results saved: {args.output}/vehicle_detection")


if __name__ == "__main__":
    main()
