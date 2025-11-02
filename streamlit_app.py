import streamlit as st
import json
import datetime

st.title("🌍 My Travel Journal")

with open("data.json", "r") as f:
    entries = json.load(f)

date = st.date_input("Pick a date", min_value="01-01-2000",format="DD/MM/YYYY")

date_str = date.strftime("%Y-%m-%d")

if date_str in entries:
    st.subheader(f"📅 {date.strftime('%B %d, %Y')}")
    st.write(entries[date_str])
else:
    st.subheader(f"📅 {date.strftime('%B %d, %Y')}")
    st.info("Nothing")
