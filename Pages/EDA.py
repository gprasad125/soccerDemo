import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import altair as alt
from mplsoccer import Pitch
import seaborn as sns


def page():
    st.markdown("## Exploratory Data Analysis")

    @st.cache(suppress_st_warning=True)
    def load_and_clean():
        coord_df = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/coord_events_new.csv")
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
    teams_leagues = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/teams_leagues.csv")

    st.markdown("### Selecting a Team")
    leagues = teams_leagues.get('competition_names').unique()
    option = st.selectbox("Select a league/category to choose a team from:", leagues, index = 1)

    if (option == "FA Women's Super League"):
        st.info("Our data for **" + option + "** teams includes data from the 2018/19, 2019/20, & 2020/21 seasons.")
    elif (option == "NWSL"):
        st.info("Our data for **" + option + "** teams includes data from the 2018 season.")
    elif (option == "La Liga"):
        st.info("Our data for **" + option + "** teams includes data from the 2004-2018 and 2019-2021 seasons, as well as any time a team appeared in the **Champions League** for the 2003-2005, 2006, & 2008-2019 seasons.")
    elif (option == "Champions League"):
        st.info("Our data for **" + option + "** teams includes data from the 2003-2005, 2006, & 2008-2019 seasons.")
    elif (option == "Premier League"):
        st.info("Our data for **" + option + "** teams includes data from the 2003/2004 season, as well as any time a team appeared in the **Champions League** for the 2003-2005, 2006, & 2008-2019 seasons.")
    elif (option == "Men's International"):
        st.info("Our data for **" + option + "** competitions includes data from the 2018 World Cup and the 2020 UEFA Euro Cup.")
    elif (option == "Women's International"):
        st.info("Our data for **" + option + "** competitions includes data from the 2019 Women's World Cup.")
    

    teams = teams_leagues[teams_leagues.get('competition_names') == option].get('team').unique()
    team_option = st.selectbox("Select a team:", teams, index = 4)

    st.markdown("### Plotting Team Events By Location")

    #st.markdown("### The Dataset")
    st.markdown("This reduced version of our dataset contains only four features – team name, (x, y) coordinates, and the event type.")
    st.markdown("The coordinates follow StatsBomb's coordinate system, where the top-left corner represents (0, 0) and the bottom-right represents (120, 80).")
    st.write(data.head())

    st.image('Assets/coordinates.png')

    st.write("Here are the first 5 events with location data for **" + team_option + "**.")
    option_df = data[data["team"] == team_option]
    st.write(option_df.head())

    # fig, ax = plt.subplots()

    pitch = Pitch(pitch_type = 'statsbomb', positional = True, shade_middle = True)
    # specifying figure size (width, height)
    fig, ax = pitch.draw(figsize=(16, 8))

    x = option_df["x"].to_numpy()
    y = option_df["y"].to_numpy()
    labels = option_df["event"].to_numpy()
    unique_labels = np.unique(labels)

    event_options = st.multiselect("Please choose which events you would like to see plotted.", unique_labels, default = ['Shot', 'Goal Keeper'])

    for l in event_options:
        i = np.where(labels == l)
        color = event_colors[l]
        ax.scatter(x[i], y[i], c = color, label = l)
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.title(team_option + " Events by (x, y) Coordinates")

    st.pyplot(fig)

    #ax.text('Defending', (5, 5), xycoords = 'figure points')
    #plt.text('Attacking')

    """
    Old Version - haven't deleted yet in case I still need it:

    example_teams = ["-","Barcelona", "Real Madrid", "Liverpool", "Manchester United", "Manchester City"]
    option = st.selectbox("Select a chosen team", example_teams)
    st.write("or")
    text_team = st.text_input("Write in a team", "")

    if option == "-":
        st.write("Go on, choose a team!")
    else:
        if text_team in np.unique(data["team"]):
            option = text_team
            st.write("You have chosen: " + option)
        elif (text_team == ""):
            st.write("You can try either way!")
        else:
            st.write("That team does not exist in our data! Please try again.")

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
    """

    st.markdown("### Analyzing a Team's Shots")
    shot_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/shots_reduced.csv")
    st.write(shot_data.head())




    st.markdown("### Acknowledgments")
    st.info("[StatsBomb Open Data](https://github.com/statsbomb/open-data)\n\n[mplsoccer](https://mplsoccer.readthedocs.io/en/latest/)")


