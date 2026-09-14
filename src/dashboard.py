"""Professional Streamlit dashboard for YOLO Vahan Saarthi traffic results."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DEFAULT_SUMMARY = Path("runs/track/traffic_summary.json")
DEFAULT_EVENTS = Path("runs/track/crossing_events.csv")
DEFAULT_VIDEO = Path("runs/track/vehicle_tracking.mp4")

st.set_page_config(
    page_title="YOLO Vahan Saarthi",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .hero { padding: 1.2rem 1.4rem; border: 1px solid rgba(128,128,128,.25);
            border-radius: 14px; margin-bottom: 1.2rem; }
    .hero h1 { margin: 0; }
    .hero p { margin: .35rem 0 0; opacity: .75; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🚗 YOLO Vahan Saarthi</h1>
        <p>Traffic intelligence dashboard — detection, tracking, IN/OUT counting and analytics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    summary_file = st.text_input("Summary JSON", str(DEFAULT_SUMMARY))
    events_file = st.text_input("Events CSV", str(DEFAULT_EVENTS))
    video_file = st.text_input("Processed video", str(DEFAULT_VIDEO))
    st.divider()
    st.caption("Run the tracker first, then refresh this dashboard to load the latest results.")

summary_path = Path(summary_file)
events_path = Path(events_file)
video_path = Path(video_file)

if not summary_path.exists():
    st.warning("No traffic summary found yet.")
    st.code("python src/tracking_counting.py --source traffic_sample.webm", language="bat")
    st.stop()

try:
    with summary_path.open("r", encoding="utf-8") as file:
        summary = json.load(file)
except (OSError, json.JSONDecodeError) as exc:
    st.error(f"Could not read the summary file: {exc}")
    st.stop()

counts_in = summary.get("counts_in", {})
counts_out = summary.get("counts_out", {})
total_in = int(summary.get("total_in", 0))
total_out = int(summary.get("total_out", 0))
total_crossed = int(summary.get("total_crossed", total_in + total_out))
peak_visible = int(summary.get("peak_visible", 0))
avg_rate = float(summary.get("average_vehicles_per_minute", 0.0))
duration = float(summary.get("duration_minutes", 0.0))

thresholds = summary.get("density_thresholds", {})
low_threshold = int(thresholds.get("low", 10))
medium_threshold = int(thresholds.get("medium", 25))
if peak_visible < low_threshold:
    density = "LOW"
elif peak_visible < medium_threshold:
    density = "MEDIUM"
else:
    density = "HIGH"

st.caption(f"Analysis duration: {duration:.1f} min  •  Current dataset: {summary_path}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Vehicles IN", f"{total_in:,}")
m2.metric("Vehicles OUT", f"{total_out:,}")
m3.metric("Total Crossed", f"{total_crossed:,}")
m4.metric("Peak Visible", f"{peak_visible:,}")

st.divider()

left, right = st.columns([1.35, 1])
with left:
    st.subheader("🚦 Traffic Overview")
    classes = sorted(set(counts_in) | set(counts_out))
    if classes:
        chart_data = pd.DataFrame(
            {
                "IN": [int(counts_in.get(name, 0)) for name in classes],
                "OUT": [int(counts_out.get(name, 0)) for name in classes],
            },
            index=[name.capitalize() for name in classes],
        )
        st.bar_chart(chart_data, height=330)
    else:
        st.info("No vehicle classes were recorded.")

with right:
    st.subheader("🚥 Traffic Status")
    st.metric("Density", density)
    st.metric("Average flow", f"{avg_rate:.1f} vehicles/min")
    st.caption(
        f"Relative thresholds: LOW < {low_threshold}, "
        f"MEDIUM < {medium_threshold}, HIGH ≥ {medium_threshold}."
    )

st.divider()

if events_path.exists():
    try:
        events = pd.read_csv(events_path)
    except (OSError, pd.errors.ParserError) as exc:
        st.error(f"Could not read crossing events: {exc}")
        events = pd.DataFrame()

    st.subheader("📈 Traffic Flow Over Time")
    if not events.empty and "time_seconds" in events.columns:
        events["minute"] = (events["time_seconds"] // 60).astype(int)
        per_minute = events.groupby("minute").size().rename("Vehicles").to_frame()
        st.line_chart(per_minute, height=280)
    else:
        st.info("No crossing events are available for the timeline.")
else:
    events = pd.DataFrame()
    st.info("Crossing event CSV was not found.")

with st.expander("📋 Detailed Crossing Events", expanded=False):
    if not events.empty:
        st.dataframe(events, use_container_width=True, hide_index=True)
    else:
        st.write("No event records available.")

st.divider()

video_col, download_col = st.columns([2, 1])
with video_col:
    st.subheader("🎥 Processed Video")
    if video_path.exists():
        st.video(str(video_path))
    else:
        st.info("Processed video not found. Run the tracker to generate it.")

with download_col:
    st.subheader("⬇️ Export Results")
    if summary_path.exists():
        st.download_button(
            "Download summary JSON",
            data=summary_path.read_bytes(),
            file_name="traffic_summary.json",
            mime="application/json",
            use_container_width=True,
        )
    if events_path.exists():
        st.download_button(
            "Download events CSV",
            data=events_path.read_bytes(),
            file_name="crossing_events.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.caption("YOLO Vahan Saarthi • Vehicle detection • ByteTrack • Traffic analytics")
