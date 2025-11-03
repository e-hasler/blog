import streamlit as st
import json
import datetime
from pathlib import Path

st.title("My interactive CV")

with open("data.json", "r") as f:
    entries = json.load(f)

date = st.date_input("Pick a date", min_value=datetime.date(2000,1,1), format="DD/MM/YYYY")

date_str = date.strftime("%d-%m-%Y")

#find precise date or periods of time
for i in range(0,7,3):
    if date_str[i:] in entries:
        file_path = Path(entries[date_str[i:]])
        if file_path.exists():
            st.markdown(file_path.read_text(), unsafe_allow_html=True)
        else:
            st.subheader(f"📅 {date.strftime('%d %B %Y')}")
            st.write(entries[date_str[i:]])