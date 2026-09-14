"""Vehicle tracking with direction-aware IN/OUT counting.

Examples:
    python src/tracking_counting.py --source 0
    python src/tracking_counting.py --source path/to/video.mp4

Vehicles are tracked with ByteTrack. A vehicle is counted once when its
center crosses the configured horizontal line. Crossing from above to below
is classified as IN; crossing from below to above is classified as OUT.
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
        str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    previous_y: dict[int, float] = {}
    counted_ids: set[int] = set()
    counts_in = defaultdict(int)
    counts_out = defaultdict(int)

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
                annotated, "COUNTING LINE", (20, max(30, line_y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
            )

            if result.boxes is not None and result.boxes.id is not None:
                ids = result.boxes.id.int().cpu().tolist()
                classes = result.boxes.cls.int().cpu().tolist()
                boxes = result.boxes.xyxy.cpu().tolist()

                for track_id, class_id, box in zip(ids, classes, boxes):
                    _, y1, _, y2 = box
                    center_y = (y1 + y2) / 2
                    name = VEHICLE_CLASSES.get(class_id)
                    if name is None:
                        continue

                    old_y = previous_y.get(track_id)
                    if old_y is not None and track_id not in counted_ids:
                        crossed_down = old_y < line_y <= center_y
                        crossed_up = old_y > line_y >= center_y

                        if crossed_down:
                            counts_in[name] += 1
                            counted_ids.add(track_id)
                        elif crossed_up:
                            counts_out[name] += 1
                            counted_ids.add(track_id)

                    previous_y[track_id] = center_y

            total_in = sum(counts_in.values())
            total_out = sum(counts_out.values())
            total = total_in + total_out

            # Dashboard overlay.
            cv2.rectangle(annotated, (10, 10), (340, 205), (0, 0, 0), -1)
            lines = [
                f"IN: {total_in}",
                f"OUT: {total_out}",
                f"TOTAL: {total}",
                f"Cars {counts_in['car']}/{counts_out['car']}  "
                f"Motorcycles {counts_in['motorcycle']}/{counts_out['motorcycle']}",
                f"Buses {counts_in['bus']}/{counts_out['bus']}  "
                f"Trucks {counts_in['truck']}/{counts_out['truck']}",
            ]
            for index, text in enumerate(lines):
                scale = 0.65 if index < 3 else 0.48
                cv2.putText(
                    annotated, text, (20, 40 + index * 32),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 2,
                )

            writer.write(annotated)
            cv2.imshow("YOLO Vahan Saarthi - IN/OUT Tracking", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

    total_in = sum(counts_in.values())
    total_out = sum(counts_out.values())
    print("\nVehicle Tracking & Counting Summary")
    print("-----------------------------------")
    print(f"IN           : {total_in}")
    print(f"OUT          : {total_out}")
    print(f"Total        : {total_in + total_out}")
    print("\nBy vehicle class (IN / OUT):")
    for name in VEHICLE_CLASSES.values():
        print(f"{name.capitalize():12}: {counts_in[name]} / {counts_out[name]}")
    print(f"Result saved : {output_path}")


if __name__ == "__main__":
    main()
