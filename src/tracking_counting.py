"""YOLO vehicle tracking, IN/OUT counting, and traffic analysis.

Examples:
    python src/tracking_counting.py --source 0
    python src/tracking_counting.py --source path/to/video.mp4

Vehicles are tracked with ByteTrack. Crossing a horizontal line creates an
IN or OUT event. Results are exported for the Streamlit dashboard.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, deque
from pathlib import Path

import cv2
from ultralytics import YOLO

VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track, count, and analyze road traffic with YOLO.")
    parser.add_argument("--source", default="0", help="Video path or webcam index (default: 0).")
    parser.add_argument("--model", default="yolo11n.pt", help="Ultralytics YOLO model.")
    parser.add_argument("--conf", type=float, default=0.35, help="Confidence threshold.")
    parser.add_argument("--line", type=float, default=0.60, help="Counting line position as frame-height ratio.")
    parser.add_argument(
        "--density-thresholds", nargs=2, type=int, metavar=("MEDIUM", "HIGH"),
        default=(5, 12), help="Visible-vehicle thresholds for Medium and High density.",
    )
    parser.add_argument("--output", default="runs/track", help="Output directory.")
    return parser.parse_args()


def density_label(visible_count: int, thresholds: tuple[int, int]) -> str:
    medium, high = thresholds
    if visible_count >= high:
        return "HIGH"
    if visible_count >= medium:
        return "MEDIUM"
    return "LOW"


def main() -> None:
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

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
    output_path = output_dir / "vehicle_tracking.mp4"
    events_path = output_dir / "crossing_events.csv"
    summary_path = output_dir / "traffic_summary.json"
    writer = cv2.VideoWriter(
        str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    previous_y: dict[int, float] = {}
    counted_ids: set[int] = set()
    counts_in = defaultdict(int)
    counts_out = defaultdict(int)
    crossing_events: deque[tuple[float, str, str]] = deque()
    all_events: list[dict[str, object]] = []
    frame_index = 0
    max_visible = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            current_time = frame_index / fps
            frame_index += 1
            result = model.track(
                frame, persist=True, conf=args.conf,
                classes=list(VEHICLE_CLASSES), tracker="bytetrack.yaml", verbose=False,
            )[0]

            annotated = result.plot()
            visible_count = 0
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

                    visible_count += 1
                    old_y = previous_y.get(track_id)
                    if old_y is not None and track_id not in counted_ids:
                        crossed_down = old_y < line_y <= center_y
                        crossed_up = old_y > line_y >= center_y
                        if crossed_down or crossed_up:
                            direction = "IN" if crossed_down else "OUT"
                            if direction == "IN":
                                counts_in[name] += 1
                            else:
                                counts_out[name] += 1
                            event = {"time_seconds": round(current_time, 3), "direction": direction, "vehicle": name, "track_id": track_id}
                            crossing_events.append((current_time, direction, name))
                            all_events.append(event)
                            counted_ids.add(track_id)
                    previous_y[track_id] = center_y

            max_visible = max(max_visible, visible_count)
            while crossing_events and current_time - crossing_events[0][0] > 60:
                crossing_events.popleft()

            vehicles_per_minute = len(crossing_events)
            density = density_label(visible_count, tuple(args.density_thresholds))
            total_in = sum(counts_in.values())
            total_out = sum(counts_out.values())
            total = total_in + total_out

            cv2.rectangle(annotated, (10, 10), (400, 245), (0, 0, 0), -1)
            lines = [f"IN: {total_in}", f"OUT: {total_out}", f"TOTAL: {total}", f"Visible: {visible_count}", f"Vehicles/min: {vehicles_per_minute}", f"Traffic: {density}"]
            for index, text in enumerate(lines):
                cv2.putText(annotated, text, (20, 40 + index * 34), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

            writer.write(annotated)
            cv2.imshow("YOLO Vahan Saarthi - Traffic Monitor", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

    total_in = sum(counts_in.values())
    total_out = sum(counts_out.values())
    total_crossed = total_in + total_out
    duration_minutes = (frame_index / fps) / 60 if frame_index else 0
    avg_vpm = total_crossed / duration_minutes if duration_minutes else 0.0

    with events_path.open("w", newline="", encoding="utf-8") as file:
        fieldnames = ["time_seconds", "direction", "vehicle", "track_id"]
        writer_csv = csv.DictWriter(file, fieldnames=fieldnames)
        writer_csv.writeheader()
        writer_csv.writerows(all_events)

    summary = {
        "counts_in": dict(counts_in),
        "counts_out": dict(counts_out),
        "total_in": total_in,
        "total_out": total_out,
        "total_crossed": total_crossed,
        "peak_visible": max_visible,
        "average_vehicles_per_minute": round(avg_vpm, 2),
        "duration_minutes": round(duration_minutes, 2),
        "density_thresholds": list(args.density_thresholds),
        "counting_line_ratio": args.line,
    }
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print("\nTraffic Monitoring Summary")
    print("--------------------------")
    for name in VEHICLE_CLASSES.values():
        print(f"{name.capitalize():12}: IN={counts_in[name]:4}  OUT={counts_out[name]:4}")
    print(f"Total crossed: {total_crossed}")
    print(f"Peak visible : {max_visible} vehicles")
    print(f"Average rate : {avg_vpm:.1f} vehicles/min")
    print(f"Result saved : {output_path}")
    print(f"Dashboard data: {summary_path}")


if __name__ == "__main__":
    main()
