# 🚗 YOLO Vahan Saarthi

> YOLO-based vehicle detection, tracking, and counting for road-traffic video.

## 📌 Overview

**YOLO Vahan Saarthi** is a computer vision project built with **Ultralytics YOLO** to detect and track common road vehicles such as cars, motorcycles, buses, and trucks.

The project now includes both basic detection and a tracking/counting pipeline. Vehicles receive persistent tracking IDs, and each tracked vehicle is counted once when its center crosses a configurable counting line.

## ✨ Current Features

- 🚘 Detects **cars, motorcycles, buses, and trucks**
- 🎥 Supports video files
- 📹 Supports webcam input
- 🎯 Configurable confidence threshold
- 🆔 Assigns persistent tracking IDs with **ByteTrack**
- 🚦 Counts vehicles crossing a configurable line
- 📊 Displays live per-class counts
- 💾 Saves the processed tracking video
- 🤖 Uses an Ultralytics YOLO model

## 🛠️ Tech Stack

- **Python**
- **Ultralytics YOLO**
- **OpenCV**
- **ByteTrack** (through Ultralytics)
- **PyTorch** (through Ultralytics)

## 📁 Project Structure

```text
yolo-vahan-saarthi/
├── README.md
├── requirements.txt
├── .gitignore
└── src/
    ├── detection.py
    └── tracking_counting.py
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/manishkumarmeghwal944-sudo/yolo-vahan-saarthi.git
cd yolo-vahan-saarthi
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

YOLO model weights are downloaded automatically by Ultralytics when the selected model is used for the first time.

## ▶️ Usage

### Basic vehicle detection

Webcam:

```bash
python src/detection.py --source 0
```

Video:

```bash
python src/detection.py --source path/to/video.mp4
```

Image:

```bash
python src/detection.py --source path/to/image.jpg
```

### Vehicle tracking and counting

Webcam:

```bash
python src/tracking_counting.py --source 0
```

Video:

```bash
python src/tracking_counting.py --source path/to/video.mp4
```

The default counting line is at **60% of the frame height**. You can change it with `--line`:

```bash
python src/tracking_counting.py --source path/to/video.mp4 --line 0.50
```

Change the confidence threshold:

```bash
python src/tracking_counting.py --source path/to/video.mp4 --conf 0.50
```

Use a different YOLO model:

```bash
python src/tracking_counting.py --source path/to/video.mp4 --model yolo11s.pt
```

Press **Q** while the tracking window is active to stop processing early.

Processed tracking videos are saved under:

```text
runs/track/vehicle_tracking.mp4
```

## 🚦 How Counting Works

1. YOLO detects the selected vehicle classes.
2. ByteTrack assigns a persistent ID to each detected vehicle.
3. The center point of each tracked bounding box is monitored across frames.
4. When a vehicle center crosses the counting line, that track ID is counted once.
5. Counts are displayed separately for cars, motorcycles, buses, and trucks.

> **Note:** The current counter counts crossings in either direction. A single track is counted only once during a run.

## 🚘 Detected Vehicle Classes

The pipeline filters the standard COCO classes to:

| Class | YOLO Class ID |
|---|---:|
| Car | 2 |
| Motorcycle | 3 |
| Bus | 5 |
| Truck | 7 |

## 📊 Example Output

```text
Vehicle Tracking & Counting Summary
-----------------------------------
Car         : 42
Motorcycle  : 18
Bus         : 5
Truck       : 11
Total crossed: 76
Result saved : runs/track/vehicle_tracking.mp4
```

## 🗺️ Roadmap

- [x] Create project structure
- [x] Add YOLO vehicle detection
- [x] Support webcam, image, and video detection
- [x] Add confidence threshold configuration
- [x] Save detection results
- [x] Add vehicle tracking
- [x] Add line-crossing vehicle counting
- [ ] Add direction-aware IN/OUT counting
- [ ] Add traffic-density analysis
- [ ] Add automated tests
- [ ] Add evaluation metrics and benchmark results
- [ ] Add sample detection/tracking outputs

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit your changes
5. Open a Pull Request

## 📄 License

A license will be added when the project is prepared for public distribution.

## 👨‍💻 Author

**Manish Kumar Meghwal**

---

⭐ If you find this project useful, consider starring the repository.
