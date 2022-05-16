import os
import streamlit as st
import numpy as np

# Custom imports
from Pages import multiPage, EDA, EDA2

# Create an instance of the app
app = multiPage.MultiPage()

# Title of the main page
st.markdown("# Passing and Team Success in Soccer")

# Add all your application here
app.add_page("Exploratory Data Analysis", EDA.page)
app.add_page("Build Your Own Team", EDA2.page)


# The main app
app.run()
