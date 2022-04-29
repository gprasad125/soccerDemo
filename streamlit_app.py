import streamlit as st
import pandas as pd

st.markdown(
    "# Soccer Events by Latitude, Longitude Coordinates"
)

df = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/coord_events.csv")
st.write(df.head())

