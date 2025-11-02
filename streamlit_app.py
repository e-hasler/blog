import streamlit as st
import json
import datetime

st.title("🌍 My Travel Journal")

# Load entries from JSON
with open("data.json", "r") as f:
    entries = json.load(f)

# Date picker
date = st.date_input("Pick a date", min_value="2000-01-01")

# Convert to string format
date_str = date.strftime("%Y-%m-%d")

# Display
if date_str in entries:
    st.subheader(f"📅 {date.strftime('%B %d, %Y')}")
    st.write(entries[date_str])
else:
    st.subheader(f"📅 {date.strftime('%B %d, %Y')}")
    st.info("Nothing")
