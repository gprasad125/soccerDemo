import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import altair as alt


def page():
    st.markdown("# Team Event By Coordinates")


    st.markdown("## The Dataset")
    st.markdown("This pared-down dataset contains only four features – team name, event name, and (x, y) coordinates along the following coordinate system, where the leftmost corner represents (0, 0) and the top right represents (120, 80).")

    @st.cache(suppress_st_warning=True)
    def load_and_clean():
        coord_df = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/coord_events.csv")
        def to_int(coord):

            if not pd.isnull(coord):

                coord = int(coord)

            return coord

        coord_df['location_x'] = coord_df['location_x'].apply(to_int)
        coord_df['location_y'] = coord_df['location_y'].apply(to_int)

        clean = coord_df.dropna().reset_index(drop = True)
        clean = clean.rename(columns = {"possession_team_name": "team",
                                        "type_name": "event",
                                       "location_x": "x",
                                       "location_y": "y"})

        clean = clean.sample(frac=1).reset_index(drop = True)
        st.write("Running for 1st time only!")
        return clean

    data = load_and_clean()
    st.write(data.head())

    @st.cache(suppress_st_warning=True)
    def make_color_dict():

        def make_color():
            color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            return color


        event_colors = dict.fromkeys(data['event'].unique())
        for ev in event_colors:

            number_of_colors = 8
            color = make_color()
            if color not in event_colors.values():
                event_colors[ev] = color

        return event_colors

    event_colors = make_color_dict()

    st.image('Assets/coordinates.png')

    example_teams = ["Barcelona", "Real Madrid", "Liverpool", "Manchester United", "Manchester City"]
    option = st.selectbox("Select a team", example_teams)
    st.write("You have chosen: " + option)
    #
    option_df = data[data["team"] == option]
    st.write(option_df.head())

    fig, ax = plt.subplots()

    x = option_df["x"].to_numpy()
    y = option_df["y"].to_numpy()
    labels = option_df["event"].to_numpy()

    for l in np.unique(labels):
        i = np.where(labels == l)
        color = event_colors[l]
        ax.scatter(x[i], y[i], c = color, label = l)
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.title(option + " Events By (x, y) Coordinates")
    st.pyplot(fig)


    #
    # chart = alt.Chart(option_df).mark_point().encode(
    #     x = "x", y = "y", color = "event").interactive().properties(
    #         width = 650, height = 500, title = option + " Event by Coord.")
    # st.altair_chart(chart)
