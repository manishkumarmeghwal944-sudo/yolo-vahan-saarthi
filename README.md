# 🚗 YOLO Vahan Saarthi

> YOLO-based vehicle detection for images, videos, and webcams.

## 📌 Overview

**YOLO Vahan Saarthi** is a computer vision project that uses the **Ultralytics YOLO** framework to detect common vehicle classes such as cars, motorcycles, buses, and trucks.

The current implementation provides a simple command-line detection pipeline that can work with a webcam, image, or video source and save annotated detection results.

## ✨ Current Features

- 🚘 Detects **cars, motorcycles, buses, and trucks**
- 📷 Supports image input
- 🎥 Supports video input
- 📹 Supports webcam input
- 🎯 Configurable confidence threshold
- 🤖 Uses an Ultralytics YOLO model
- 💾 Saves annotated detection results
- 📊 Prints a vehicle-detection summary

## 🛠️ Tech Stack

- **Python**
- **Ultralytics YOLO**
- **PyTorch** (through Ultralytics)

## 📁 Project Structure

```text
yolo-vahan-saarthi/
├── README.md
├── requirements.txt
├── .gitignore
└── src/
    └── detection.py
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

The YOLO model weights are downloaded automatically by Ultralytics when the selected model is used for the first time.

## ▶️ Usage

### Webcam

```bash
python src/detection.py --source 0
```

### Image

```bash
python src/detection.py --source path/to/image.jpg
```

### Video

```bash
python src/detection.py --source path/to/video.mp4
```

### Use a different YOLO model

```bash
python src/detection.py --source path/to/video.mp4 --model yolo11s.pt
```

### Change confidence threshold

```bash
python src/detection.py --source 0 --conf 0.50
```

Detection results are saved under:

```text
runs/detect/vehicle_detection/
```

## 🚘 Detected Vehicle Classes

The current pipeline filters the standard COCO classes to:

| Class | YOLO Class ID |
|---|---:|
| Car | 2 |
| Motorcycle | 3 |
| Bus | 5 |
| Truck | 7 |

## 📊 Detection Summary

After processing, the program prints a summary similar to:

```text
Vehicle Detection Summary
-------------------------
Car         : 12
Motorcycle  : 4
Bus         : 2
Truck       : 3
Total       : 21
```

## 🗺️ Roadmap

- [x] Create project structure
- [x] Add YOLO vehicle detection
- [x] Support webcam, image, and video sources
- [x] Add confidence threshold configuration
- [x] Save detection results
- [ ] Add vehicle tracking
- [ ] Add reliable per-frame vehicle counting
- [ ] Add traffic-density analysis
- [ ] Add automated tests
- [ ] Add evaluation metrics and benchmark results
- [ ] Add sample detection outputs

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
