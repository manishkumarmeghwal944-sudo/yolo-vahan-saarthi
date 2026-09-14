"""Streamlit dashboard for YOLO Vahan Saarthi traffic results."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DEFAULT_SUMMARY = Path("runs/track/traffic_summary.json")
DEFAULT_EVENTS = Path("runs/track/crossing_events.csv")

st.set_page_config(page_title="YOLO Vahan Saarthi", page_icon="🚗", layout="wide")
st.title("🚗 YOLO Vahan Saarthi")
st.caption("Vehicle tracking, IN/OUT counting, traffic density, and rate analysis")

summary_file = st.sidebar.text_input("Summary JSON", str(DEFAULT_SUMMARY))
events_file = st.sidebar.text_input("Events CSV", str(DEFAULT_EVENTS))

summary_path = Path(summary_file)
events_path = Path(events_file)

if not summary_path.exists():
    st.info(
        "No traffic summary found yet. Run the tracker first: "
        "python src/tracking_counting.py --source path/to/video.mp4"
    )
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

col1, col2, col3, col4 = st.columns(4)
col1.metric("Vehicles IN", total_in)
col2.metric("Vehicles OUT", total_out)
col3.metric("Total Crossed", total_crossed)
col4.metric("Peak Visible", peak_visible)

st.subheader("📊 Vehicle Counts")
classes = sorted(set(counts_in) | set(counts_out))
chart_data = pd.DataFrame(
    {
        "IN": [counts_in.get(name, 0) for name in classes],
        "OUT": [counts_out.get(name, 0) for name in classes],
    },
    index=[name.capitalize() for name in classes],
)
st.bar_chart(chart_data)

left, right = st.columns(2)
with left:
    st.subheader("⏱️ Traffic Rate")
    st.metric("Average vehicles/min", f"{avg_rate:.1f}")
with right:
    st.subheader("🚥 Traffic Density")
    st.metric("Peak visible vehicles", peak_visible)
    st.caption("Density thresholds are configurable relative indicators, not engineering standards.")

if events_path.exists():
    st.subheader("📈 Crossing Events")
    events = pd.read_csv(events_path)
    if not events.empty:
        events["minute"] = (events["time_seconds"] // 60).astype(int)
        per_minute = events.groupby("minute").size().rename("vehicles").to_frame()
        st.line_chart(per_minute)
        st.dataframe(events, use_container_width=True)
else:
    st.info("Crossing event data is not available. Re-run the tracker after the dashboard update.")

st.caption("YOLO Vahan Saarthi • Streamlit dashboard")
