"""Vehicle tracking and line-crossing counting with Ultralytics YOLO.

Examples:
    python src/tracking_counting.py --source 0
    python src/tracking_counting.py --source path/to/video.mp4

The script tracks cars, motorcycles, buses, and trucks and counts each
vehicle once when its tracked center crosses a configurable horizontal line.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import cv2
from ultralytics import YOLO

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track and count vehicles with YOLO.")
    parser.add_argument("--source", default="0", help="Video path or webcam index (default: 0).")
    parser.add_argument("--model", default="yolo11n.pt", help="Ultralytics YOLO model.")
    parser.add_argument("--conf", type=float, default=0.35, help="Confidence threshold.")
    parser.add_argument("--line", type=float, default=0.60, help="Counting line position as frame-height ratio.")
    parser.add_argument("--output", default="runs/track", help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source
    Path(args.output).mkdir(parents=True, exist_ok=True)

    model = YOLO(args.model)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open source: {args.source}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1280
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25.0

    line_y = int(height * max(0.1, min(args.line, 0.9)))
    output_path = Path(args.output) / "vehicle_tracking.mp4"
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    previous_y: dict[int, float] = {}
    counted_ids: set[int] = set()
    counts = defaultdict(int)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            result = model.track(
                frame,
                persist=True,
                conf=args.conf,
                classes=list(VEHICLE_CLASSES),
                tracker="bytetrack.yaml",
                verbose=False,
            )[0]

            annotated = result.plot()
            cv2.line(annotated, (0, line_y), (width, line_y), (255, 255, 255), 2)
            cv2.putText(
                annotated,
                "COUNTING LINE",
                (20, max(30, line_y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            if result.boxes is not None and result.boxes.id is not None:
                ids = result.boxes.id.int().cpu().tolist()
                classes = result.boxes.cls.int().cpu().tolist()
                boxes = result.boxes.xyxy.cpu().tolist()

                for track_id, class_id, box in zip(ids, classes, boxes):
                    x1, y1, x2, y2 = box
                    center_y = (y1 + y2) / 2
                    name = VEHICLE_CLASSES.get(class_id)
                    if name is None:
                        continue

                    old_y = previous_y.get(track_id)
                    if (
                        old_y is not None
                        and track_id not in counted_ids
                        and ((old_y < line_y <= center_y) or (old_y > line_y >= center_y))
                    ):
                        counts[name] += 1
                        counted_ids.add(track_id)

                    previous_y[track_id] = center_y

            total = sum(counts.values())
            cv2.rectangle(annotated, (10, 10), (270, 145), (0, 0, 0), -1)
            cv2.putText(annotated, f"Cars: {counts['car']}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
            cv2.putText(annotated, f"Motorcycles: {counts['motorcycle']}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
            cv2.putText(annotated, f"Buses: {counts['bus']}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
            cv2.putText(annotated, f"Trucks: {counts['truck']}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

            writer.write(annotated)
            cv2.imshow("YOLO Vahan Saarthi - Tracking & Counting", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

    print("\nVehicle Tracking & Counting Summary")
    print("-----------------------------------")
    for name in VEHICLE_CLASSES.values():
        print(f"{name.capitalize():12}: {counts[name]}")
    print(f"Total crossed: {sum(counts.values())}")
    print(f"Result saved : {output_path}")


if __name__ == "__main__":
    main()
