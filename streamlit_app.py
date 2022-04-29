import streamlit as st
import pandas as pd
import zipfile36 as zipfile

path = zipfile.ZipFile("coord_events.csv.zip", "r")
df = pd.read_csv(path.open("coord_events.csv"))

print(df.head())