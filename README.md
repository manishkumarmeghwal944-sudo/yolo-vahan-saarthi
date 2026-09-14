# 🚗 YOLO Vahan Saarthi

> YOLO-based vehicle detection, tracking, and direction-aware traffic counting.

## 📌 Overview

**YOLO Vahan Saarthi** is a computer vision project built with **Ultralytics YOLO** to detect and track common road vehicles such as cars, motorcycles, buses, and trucks.

The project includes a tracking and counting pipeline using **ByteTrack**. Each tracked vehicle receives a persistent ID and is counted once when its center crosses a configurable horizontal line. The crossing direction is reported as **IN** or **OUT**.

## ✨ Current Features

- 🚘 Detects **cars, motorcycles, buses, and trucks**
- 🎥 Supports video files
- 📹 Supports webcam input
- 🎯 Configurable confidence threshold
- 🆔 Persistent tracking IDs with **ByteTrack**
- 🚦 Configurable counting line
- ↗️ Direction-aware **IN / OUT** counting
- 📊 Live total and per-class counts
- 💾 Saves the processed tracking video

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

```bash
git clone https://github.com/manishkumarmeghwal944-sudo/yolo-vahan-saarthi.git
cd yolo-vahan-saarthi
python -m venv venv
```

Activate the environment and install dependencies:

**Windows**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux / macOS**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

YOLO model weights are downloaded automatically by Ultralytics when first used.

## ▶️ Usage

### Basic detection

```bash
python src/detection.py --source path/to/video.mp4
```

### Tracking + IN/OUT counting

```bash
python src/tracking_counting.py --source path/to/video.mp4
```

For a webcam:

```bash
python src/tracking_counting.py --source 0
```

### Change the counting line

The default line is at 60% of the frame height. For a line halfway down the frame:

```bash
python src/tracking_counting.py --source path/to/video.mp4 --line 0.50
```

### Change confidence

```bash
python src/tracking_counting.py --source path/to/video.mp4 --conf 0.50
```

### Change YOLO model

```bash
python src/tracking_counting.py --source path/to/video.mp4 --model yolo11s.pt
```

Press **Q** to stop processing.

Processed video:

```text
runs/track/vehicle_tracking.mp4
```

## 🚦 IN / OUT Counting Logic

The counting line divides the frame into two regions:

- **IN:** vehicle center moves from above the line to below it.
- **OUT:** vehicle center moves from below the line to above it.

Each tracking ID is counted only once per program run, preventing repeated counts while the vehicle remains near the line.

> For reliable results, place the counting line across the road where vehicles clearly pass through it and use a camera with a stable view.

## 🚘 Detected Vehicle Classes

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
IN           : 42
OUT          : 18
Total        : 60

By vehicle class (IN / OUT):
Car         : 25 / 10
Motorcycle  : 12 / 5
Bus         : 2 / 1
Truck       : 3 / 2
```

## 🗺️ Roadmap

- [x] YOLO vehicle detection
- [x] Webcam, image, and video detection
- [x] Confidence threshold configuration
- [x] Vehicle tracking with ByteTrack
- [x] Line-crossing counting
- [x] Direction-aware IN/OUT counting
- [ ] Traffic-density analysis
- [ ] Vehicle-per-minute statistics
- [ ] Web dashboard
- [ ] Automated tests
- [ ] Evaluation metrics and benchmark results
- [ ] Sample detection/tracking outputs

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
