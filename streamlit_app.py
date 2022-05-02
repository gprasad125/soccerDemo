import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random2
import altair as alt

st.markdown(
    "# Soccer Events by Latitude, Longitude Coordinates"
)

df = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/coord_events.csv")
def to_int(coord):

    if not pd.isnull(coord):

        coord = int(coord)

    return coord

df['location_x'] = df['location_x'].apply(to_int)
df['location_y'] = df['location_y'].apply(to_int)

clean = df.dropna().reset_index(drop = True)
clean = clean.rename(columns = {"possession_team_name": "team",
                                "type_name": "event",
                               "location_x": "x",
                               "location_y": "y"})

clean = clean.sample(frac=1).reset_index(drop = True)
st.write(clean.head())

def make_color():

    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color

event_colors = dict.fromkeys(clean['event'].unique())
for ev in event_colors:

    number_of_colors = 8
    color = make_color()
    if color not in event_colors.values():
        event_colors[ev] = color

st.image('coordinates.png')

madrid = clean[clean["team"] == "Real Madrid"]

fig_madrid, ax_madrid = plt.subplots()
scatter_x = madrid['x'].to_numpy()
scatter_y = madrid['y'].to_numpy()
labels = madrid['event'].to_numpy()
for l in np.unique(labels):
    i = np.where(labels == l)
    color = event_colors[l]
    ax_madrid.scatter(scatter_x[i], scatter_y[i], c = color, label = l)
ax_madrid.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
st.pyplot(fig_madrid)

man_city = clean[clean["team"] == "Manchester City"]

fig_city, ax_city = plt.subplots()
scatter_x = man_city['x'].to_numpy()
scatter_y = man_city['y'].to_numpy()
labels = man_city['event'].to_numpy()
for l in np.unique(labels):
    i = np.where(labels == l)
    color = event_colors[l]
    ax_city.scatter(scatter_x[i], scatter_y[i], c = color, label = l)
ax_city.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
st.pyplot(fig_city)

chart = alt.Chart(man_city).mark_point().encode(
    x = "x", y = "y", color = "event").interactive().properties(
        width = 650, height = 500, title = "Man City Event by Coord.")
st.altair_chart(chart)
