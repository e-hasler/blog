import streamlit as st
import json
import datetime
from pathlib import Path
import streamlit.components.v1 as components


# ------------- CV content
st.title("My interactive CV")

#load data.json file
with open("data.json", "r") as f:
    entries = json.load(f)

#parse available dates
all_dates = []
for k in entries:
    try:
        all_dates.append(datetime.datetime.strptime(k, "%d-%m-%Y").date())
    except ValueError:
        try:
            all_dates.append(datetime.datetime.strptime(k, "%m-%Y").date())
        except ValueError:
            try:
                all_dates.append(datetime.datetime.strptime(k, "%Y").date())
            except ValueError:
                pass

all_dates = sorted(all_dates)
if not all_dates:
    st.warning("No valid entries found in data.json.")
    st.stop()

#slider
date = st.select_slider(
    "📅 Pick a date",
    options=all_dates,
    value=all_dates[-1],
    format_func=lambda d: d.strftime("%B %Y"),
)

formats_to_try = ["%d-%m-%Y", "%m-%Y", "%Y"]
date_str = None
for fmt in formats_to_try:
    ds = date.strftime(fmt)
    if ds in entries:
        date_str = ds
        break

#display corresponding content
if date_str and date_str in entries:
    file_path = Path(entries[date_str])
    if file_path.exists():
        st.markdown(file_path.read_text(), unsafe_allow_html=True)
    else:
        st.subheader(f"📅 {date.strftime('%d %B %Y')}")
        st.write(entries[date_str])
else:
    st.info("Nothing recorded for this date.")