import streamlit as st
import json
import datetime

st.title("🌍 My Travel Journal")

with open("data.json", "r") as f:
    entries = json.load(f)

date = st.date_input("Pick a date", min_value=datetime.date(2000,1,1), format="DD/MM/YYYY")

date_str = date.strftime("%d-%m-%Y")

if date_str in entries:
    st.subheader(f"📅 {date.strftime('%d %B %Y')}")
    st.write(entries[date_str])
elif date_str[3:] in entries:
    st.subheader(f"📅 {date.strftime('%d %B %Y')}")
    st.write(entries[date_str[3:]])
elif date_str[6:] in entries:
    st.subheader(f"📅 {date.strftime('%d %B %Y')}")
    st.write(entries[date_str[6:]])
else:
    st.subheader(f"📅 {date.strftime('%d %B %Y')}")
    st.info("Nothing")



