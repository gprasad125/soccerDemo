import os
import streamlit as st
import numpy as np

# Custom imports
from Pages import multiPage, EDA

# Create an instance of the app
app = multiPage.MultiPage()

# Title of the main page
st.markdown("# DS3 Soccer Project")

# Add all your application here
app.add_page("Exploratory Data Analysis", EDA.page)

# The main app
app.run()
