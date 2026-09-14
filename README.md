# 🚗 YOLO Vahan Saarthi

> YOLO-based vehicle detection, tracking, direction-aware counting, and traffic-density analysis.

## 📌 Overview

**YOLO Vahan Saarthi** is a computer vision project built with **Ultralytics YOLO** to detect and track common road vehicles such as cars, motorcycles, buses, and trucks.

The project includes a tracking and traffic-monitoring pipeline using **ByteTrack**. Each tracked vehicle receives a persistent ID, crossing events are classified as **IN** or **OUT**, and the system reports both a rolling vehicles-per-minute rate and a simple live traffic-density level.

## ✨ Current Features

- 🚘 Detects **cars, motorcycles, buses, and trucks**
- 🎥 Supports video files
- 📹 Supports webcam input
- 🎯 Configurable confidence threshold
- 🆔 Persistent tracking IDs with **ByteTrack**
- 🚦 Configurable counting line
- ↗️ Direction-aware **IN / OUT** counting
- 📊 Live total and per-class counts
- ⏱️ Rolling **vehicles-per-minute** rate
- 🚥 Live **LOW / MEDIUM / HIGH** traffic-density classification
- 📈 Peak visible-vehicle count and average traffic rate
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

### Traffic monitoring

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

### Change density thresholds

The default thresholds are:

- **LOW:** fewer than 5 visible tracked vehicles
- **MEDIUM:** 5–11 visible tracked vehicles
- **HIGH:** 12 or more visible tracked vehicles

You can customize the Medium and High thresholds:

```bash
python src/tracking_counting.py --source path/to/video.mp4 --density-thresholds 8 20
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

## 🚥 Traffic-Density Analysis

The system estimates live traffic density from the number of vehicle tracks visible in the current frame:

| Visible tracked vehicles | Density |
|---:|---|
| 0–4 | LOW |
| 5–11 | MEDIUM |
| 12+ | HIGH |

These are configurable thresholds rather than calibrated traffic-engineering standards. They provide a useful relative indicator for a fixed camera scene.

### Vehicles per minute

A rolling 60-second window tracks recent IN/OUT crossing events and displays:

```text
Vehicles/min: 14
```

At the end of processing, the program also reports the average crossing rate for the complete video.

## 🚘 Detected Vehicle Classes

| Class | YOLO Class ID |
|---|---:|
| Car | 2 |
| Motorcycle | 3 |
| Bus | 5 |
| Truck | 7 |

## 📊 Example Output

```text
Traffic Monitoring Summary
--------------------------
Car         : IN=  25  OUT=  10
Motorcycle  : IN=  12  OUT=   5
Bus         : IN=   2  OUT=   1
Truck       : IN=   3  OUT=   2
Total crossed: 60
Peak visible : 14 vehicles
Average rate : 11.5 vehicles/min
Result saved : runs/track/vehicle_tracking.mp4
```

## 🗺️ Roadmap

- [x] YOLO vehicle detection
- [x] Webcam, image, and video detection
- [x] Confidence threshold configuration
- [x] Vehicle tracking with ByteTrack
- [x] Line-crossing counting
- [x] Direction-aware IN/OUT counting
- [x] Traffic-density analysis
- [x] Vehicle-per-minute statistics
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
