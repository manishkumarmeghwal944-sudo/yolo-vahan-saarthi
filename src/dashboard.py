"""Streamlit dashboard for YOLO Vahan Saarthi traffic results."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

DEFAULT_SUMMARY = Path("runs/track/traffic_summary.json")
DEFAULT_EVENTS = Path("runs/track/crossing_events.csv")
DEMO_SUMMARY = Path("demo/traffic_summary.json")
DEMO_EVENTS = Path("demo/crossing_events.csv")
UPLOAD_ROOT = Path("runs/uploads")

st.set_page_config(page_title="YOLO Vahan Saarthi", page_icon="🚗", layout="wide")

st.title("🚗 YOLO Vahan Saarthi")
st.caption("Traffic intelligence dashboard — detection, tracking, IN/OUT counting and analytics")

# -----------------------------------------------------------------------------
# Video upload and analysis
# -----------------------------------------------------------------------------
st.sidebar.header("🎥 Analyze a video")
uploaded_video = st.sidebar.file_uploader(
    "Upload a traffic video",
    type=["mp4", "avi", "mov", "mkv", "webm"],
    help="Upload a road-traffic video. YOLO + ByteTrack will analyze it on the server.",
)
conf = st.sidebar.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
line_ratio = st.sidebar.slider("Counting line position", 0.10, 0.90, 0.60, 0.05)

if uploaded_video is not None:
    st.subheader("🎥 Uploaded Traffic Video")
    st.video(uploaded_video)

    if st.button("🚀 Analyze uploaded video", type="primary", use_container_width=True):
        UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
        input_path = UPLOAD_ROOT / uploaded_video.name
        output_dir = UPLOAD_ROOT / "latest"
        output_dir.mkdir(parents=True, exist_ok=True)
        input_path.write_bytes(uploaded_video.getbuffer())

        command = [
            sys.executable,
            "src/tracking_counting.py",
            "--source", str(input_path),
            "--output", str(output_dir),
            "--conf", str(conf),
            "--line", str(line_ratio),
            "--no-display",
        ]

        with st.spinner("YOLO is detecting and tracking vehicles. This can take a while for longer videos..."):
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=600,
            )

        if completed.returncode != 0:
            st.error("Video analysis failed.")
            if completed.stderr:
                st.code(completed.stderr[-6000:])
        else:
            st.session_state["uploaded_summary"] = str(output_dir / "traffic_summary.json")
            st.session_state["uploaded_events"] = str(output_dir / "crossing_events.csv")
            st.session_state["uploaded_video_output"] = str(output_dir / "vehicle_tracking.mp4")
            st.success("✅ Analysis complete! The dashboard below now shows your uploaded video's results.")
            st.rerun()

# Prefer freshly analyzed upload results; otherwise use local tracker output.
if "uploaded_summary" in st.session_state and Path(st.session_state["uploaded_summary"]).exists():
    summary_path = Path(st.session_state["uploaded_summary"])
    events_path = Path(st.session_state["uploaded_events"])
    using_demo = False
    data_source = "Uploaded video analysis"
else:
    summary_file = st.sidebar.text_input("Summary JSON", str(DEFAULT_SUMMARY))
    events_file = st.sidebar.text_input("Events CSV", str(DEFAULT_EVENTS))
    summary_path = Path(summary_file)
    events_path = Path(events_file)
    using_demo = False
    data_source = "Local tracker results"

    # Streamlit Community Cloud does not have files generated on a user's PC.
    # Fall back to a bundled demo dataset so the deployed app is immediately useful.
    if not summary_path.exists():
        if DEMO_SUMMARY.exists():
            summary_path = DEMO_SUMMARY
            events_path = DEMO_EVENTS
            using_demo = True
            data_source = "Bundled demo dataset"
        else:
            st.warning("No traffic summary found yet. Upload a video above or run the tracker locally.")
            st.code("python src/tracking_counting.py --source traffic_sample.webm")
            st.stop()

with summary_path.open("r", encoding="utf-8") as file:
    summary = json.load(file)

counts_in = summary.get("counts_in", {})
counts_out = summary.get("counts_out", {})
total_in = summary.get("total_in", 0)
total_out = summary.get("total_out", 0)
total_crossed = summary.get("total_crossed", total_in + total_out)
peak_visible = summary.get("peak_visible", 0)
avg_rate = summary.get("average_vehicles_per_minute", 0.0)
duration_minutes = summary.get("duration_minutes", 0.0)
density = summary.get("peak_density", "UNKNOWN")

st.info(f"📌 Data source: **{data_source}**")
if using_demo:
    st.caption("Upload your own traffic video from the sidebar to replace the demo results.")

# -----------------------------------------------------------------------------
# KPIs
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vehicles IN", total_in)
col2.metric("Vehicles OUT", total_out)
col3.metric("Total Crossed", total_crossed)
col4.metric("Peak Visible", peak_visible)

left, middle, right = st.columns(3)
with left:
    st.metric("Average vehicles/min", f"{avg_rate:.1f}")
with middle:
    st.metric("Peak traffic density", density)
with right:
    st.metric("Analysis duration", f"{duration_minutes:.2f} min")

# -----------------------------------------------------------------------------
# Charts
# -----------------------------------------------------------------------------
st.subheader("📊 Vehicle Flow")
classes = sorted(set(counts_in) | set(counts_out))
chart_data = pd.DataFrame(
    {
        "IN": [counts_in.get(name, 0) for name in classes],
        "OUT": [counts_out.get(name, 0) for name in classes],
    },
    index=[name.capitalize() for name in classes],
)
st.bar_chart(chart_data)

if events_path.exists():
    st.subheader("📈 Crossing Events")
    events = pd.read_csv(events_path)
    if not events.empty and "time_seconds" in events.columns:
        events["minute"] = (events["time_seconds"] // 60).astype(int)
        per_minute = events.groupby("minute").size().rename("vehicles").to_frame()
        st.line_chart(per_minute)
        with st.expander("View detailed crossing events"):
            st.dataframe(events, use_container_width=True)
    elif events.empty:
        st.caption("No crossing events recorded.")
else:
    events = pd.DataFrame()
    st.caption("Crossing event data is not available for this dataset.")

# -----------------------------------------------------------------------------
# Processed video and exports
# -----------------------------------------------------------------------------
output_video = None
if "uploaded_video_output" in st.session_state:
    candidate = Path(st.session_state["uploaded_video_output"])
    if candidate.exists():
        output_video = candidate

if output_video is not None:
    st.subheader("🎬 Processed Video")
    st.caption("YOLO detections, tracking IDs, counting line, and traffic metrics are overlaid on the processed video.")
    st.video(str(output_video))
    st.download_button(
        "⬇️ Download processed video",
        data=output_video.read_bytes(),
        file_name="vehicle_tracking.mp4",
        mime="video/mp4",
    )

st.subheader("⬇️ Export Results")
col_a, col_b = st.columns(2)
with col_a:
    st.download_button(
        "Download summary JSON",
        data=json.dumps(summary, indent=2),
        file_name="traffic_summary.json",
        mime="application/json",
    )
with col_b:
    csv_data = events_path.read_text(encoding="utf-8") if events_path.exists() else ""
    st.download_button(
        "Download events CSV",
        data=csv_data,
        file_name="crossing_events.csv",
        mime="text/csv",
    )

st.caption("YOLO Vahan Saarthi • YOLO + ByteTrack + Streamlit")
