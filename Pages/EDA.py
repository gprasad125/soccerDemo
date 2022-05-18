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
    def make_color_dict(labels):

        palette = sns.color_palette("husl", len(labels))

        def make_color():
            color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            return color


        event_colors = {}

        #dict.fromkeys(labels)
        for ind, ev in enumerate(labels):
            event_colors[ev] = palette[ind]

            #number_of_colors = 8
            #color = make_color()
            #if color not in event_colors.values():
                #event_colors[ev] = color

        return event_colors

    ## INITIAL DATA SET UP AND CHOOSING TEAM #
    teams_leagues = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/teams_leagues.csv")

    st.markdown("### Selecting a Team")
    leagues = teams_leagues.get('competition_names').unique()
    option = st.selectbox("Select a league/category to choose a team from:", leagues, index = 1)

    if (option == "FA Women's Super League"):
        st.info("Our data for **" + option + "** teams includes data from the 2018/19, 2019/20, & 2020/21 seasons.")
    elif (option == "NWSL"):
        st.info("Our data for **" + option + "** teams includes data from the 2018 season.")
    elif (option == "La Liga"):
        st.info("Our data for **" + option + "** teams includes data from the 2004-2018 and 2019-2021 seasons, as well as time(s) a team appeared in the **Champions League** for the 2003-2005, 2006, & 2008-2019 seasons.")
    elif (option == "Champions League"):
        st.info("Our data for **" + option + "** teams includes data from the 2003-2005, 2006, & 2008-2019 seasons.")
    elif (option == "Premier League"):
        st.info("Our data for **" + option + "** teams includes data from the 2003/2004 season, as well as time(s) a team appeared in the **Champions League** for the 2003-2005, 2006, & 2008-2019 seasons.")
    elif (option == "Men's International"):
        st.info("Our data for **" + option + "** competitions includes data from the 2018 World Cup and the 2020 UEFA Euro Cup.")
    elif (option == "Women's International"):
        st.info("Our data for **" + option + "** competitions includes data from the 2019 Women's World Cup.")
    
    num_games_df = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/game_counts.csv").set_index('team')

    teams = teams_leagues[teams_leagues.get('competition_names') == option].get('team').unique()
    team_option = st.selectbox("Select a team:", teams, index = 4)
    option_df = data[data["team"] == team_option]

    num_team_events = option_df.shape[0]
    num_games = num_games_df.loc[team_option]['count']
    if (option == "Men's International" or option == "Women's International"):
        st.info('We have ' + str(num_team_events) + ' events for the **' + team_option + '** international team in ' + str(num_games) + ' games.')
    else:
        st.info('We have ' + str(num_team_events) + ' events for **' + team_option + '** in ' + str(num_games) + ' games.')

    ## EVENTS ##
    st.markdown("### Plotting Team Events By Location")

    st.markdown("This reduced version of our dataset contains only four features – team name, (x, y) coordinates, and the event type.")
    st.markdown("The coordinates follow StatsBomb's coordinate system, where the top-left corner represents (0, 0) and the bottom-right represents (120, 80).")
    #st.write(data.head())

    st.image('Assets/coordinates.png')

    st.write("Here are the first 5 events with location data for **" + team_option + "**.")
    st.write(option_df.head())

    pitch = Pitch(pitch_type = 'statsbomb', positional = True, shade_middle = True)
    # specifying figure size (width, height)
    fig, ax = pitch.draw(figsize=(16, 8))

    x = option_df["x"].to_numpy()
    y = option_df["y"].to_numpy()
    labels = option_df["event"].to_numpy()
    unique_labels = np.unique(labels)
    event_colors = make_color_dict(unique_labels)

    event_form = st.form("events")
    event_options = event_form.multiselect("Please choose which events you would like to see plotted.", unique_labels, default = ['Shot', 'Goal Keeper'])
    event_submitted = event_form.form_submit_button("Once you're done choosing your events, click this button.")

    if event_submitted and len(event_options) != 0:
        for l in event_options:
            i = np.where(labels == l)
            color = event_colors[l]
            ax.scatter(x[i], y[i], c = color, label = l, s = 5)
        ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
        plt.title(team_option + " Events by (x, y) Coordinates")

        st.pyplot(fig, ax)
    elif event_submitted and len(event_options) == 0:
        st.markdown('You have not selected any events - please select again.')

    # RETURN TO TEAM SELECITON
    team_select = 'selecting-a-team'
    st.markdown(f"<a href='#{team_select}'>Try a different team?</a>", unsafe_allow_html=True)

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

    ## SHOT BAR GRAPHS ##
    st.markdown("### Analyzing a Team's Shots")

    # is this allowed like this?
    @st.cache(suppress_st_warning=True)
    def read_shot_data():
        shot_df = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/shots_reduced.csv")
        shot_df = shot_df.rename(columns = {'team_name': 'team', 'play_pattern_name': 'play_pattern'})
        play_patterns_list = shot_df.get('play_pattern').sort_values(ascending = True).unique()
        st.write("Running for 1st time only!")
        return shot_df, play_patterns_list

    shot_data, play_patterns = read_shot_data()

    team_shot_data = shot_data[shot_data["team"] == team_option]

    st.write(team_shot_data.head())

    shotcol1, shotcol2 = st.columns(2)

    fig2 = plt.figure(2)

    minute_vals = list(range(0, 131, 5))
    minute_df = pd.DataFrame({'minute': minute_vals})
    minute_df

    minute_bins = team_shot_data.get('minute').transform(lambda x: x - (x%5))
    vc_df = pd.DataFrame(minute_bins.value_counts().reset_index()).rename(columns = {'minute': 'count', 'index': 'minute'})
    full_minutes = vc_df.merge(minute_df, how = 'outer').fillna(0)

    sns.set(rc = {'figure.figsize':(15,15)})
    axs2 = sns.barplot(x = full_minutes['minute'], y = full_minutes['count']).set_title('Shot Distribution with 5 Minute Bins', fontsize = 20)

    shotcol1.pyplot(fig2, axs2)

    fig3 = plt.figure(3)

    shot_reasons = team_shot_data.get('play_pattern')
    sns.set(rc = {'figure.figsize':(15,15)})
    axs3 = sns.countplot(shot_reasons, order = play_patterns).set_title('Shots by Play Pattern', fontsize = 20)

    shotcol2.pyplot(fig3, axs3)

    # RETURN TO TEAM SELECTION
    st.markdown(f"<a href='#{team_select}'>Try a different team?</a>", unsafe_allow_html=True)

    st.markdown("### Exploring Passing Patterns")

    @st.cache(suppress_st_warning=True)
    def read_clean_pass_data():
        passing_data = pd.read_csv('https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/withLastEvent.csv')

        locs = passing_data.get("match_id") == 3749133
        passing_data.loc[locs, :] = passing_data.loc[locs].replace({'Aston Villa': 'Aston Villa Men'})

        locs = passing_data.get("match_id") == 3749552
        passing_data.loc[locs, :] = passing_data.loc[locs].replace({'Manchester United': 'Manchester United Men'})

        locs = passing_data.get("match_id") == 3749246
        passing_data.loc[locs, :] = passing_data.loc[locs].replace({'Manchester United': 'Manchester United Men'})

        locs = passing_data.get("match_id") == 18236
        passing_data.loc[locs, :] = passing_data.loc[locs].replace({'Manchester United': 'Manchester United Men'})

        locs = passing_data.get("match_id") == 3750201
        passing_data.loc[locs, :] = passing_data.loc[locs].replace({'Manchester United': 'Manchester United Men'})

        passing_data['possession_team_name'] = passing_data['possession_team_name'].replace({'Seattle Reign': 'OL Reign', 'Sky Blue FC':'NJ/NY Gotham FC'})
        passing_data['team_name'] = passing_data['team_name'].replace({'Seattle Reign': 'OL Reign', 'Sky Blue FC':'NJ/NY Gotham FC'})

        def find_field_section(x):
            if x < 40:
                return 'Defending Third'
            elif x > 80:
                return 'Attacking Third'
            else:
                return 'Middle Third'

        passing_data['field_section'] = passing_data['pass_end_location_x'].transform(find_field_section)

        # DROP COLUMNS
        reduced_pass = passing_data.get(['possession_team_name', 'idx', 'level_0', 'pass_recipient_name', 'field_section'])

        st.write("Running for 1st time only!")
        return reduced_pass

    pass_data = read_clean_pass_data()

    team_pass_data = pass_data[pass_data.get('possession_team_name') == team_option].reset_index(drop = True)

    team_name_counts = team_pass_data.groupby('idx')['pass_recipient_name'].nunique()
    #st.table(team_name_counts.head(5))
    team_pass_counts = team_pass_data.groupby('idx')['level_0'].count()
    #st.table(team_pass_counts.head(5))
    last_locs = team_pass_data.drop_duplicates(subset = 'idx', keep = 'last')[['idx', 'field_section']].set_index('idx')['field_section']
    #st.table(last_locs.head(5))

    fig4 = plt.figure(3)

    axs4 = sns.scatterplot(x = team_pass_counts, y = team_name_counts, hue = last_locs, legend = 'brief')
    axs4.set_xlabel("# of Passes in Passing Chain", fontsize = 20)
    axs4.set_ylabel("# of Unique Players Involved in Passing Chain", fontsize = 20)
    axs4.set_title('# of Passes vs Unique Recipients in Passing Chain', fontsize = 30)

    st.pyplot(fig4, axs4)



    




