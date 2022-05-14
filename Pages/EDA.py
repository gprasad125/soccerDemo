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
    event_colors = make_color_dict()

    event_form = st.form("events")
    event_options = event_form.multiselect("Please choose which events you would like to see plotted.", unique_labels, default = ['Shot', 'Goal Keeper'])
    event_submitted = event_form.form_submit_button("Once you're done choosing your events, click this button.")

    if event_submitted and len(event_options) != 0:
        for l in event_options:
            i = np.where(labels == l)
            color = event_colors[l]
            ax.scatter(x[i], y[i], c = color, label = l, s = 1)
        ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
        plt.title(team_option + " Events by (x, y) Coordinates")

        st.pyplot(fig, ax)
    elif len(event_options) == 0:
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
    shot_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/shots_reduced.csv")
    shot_data = shot_data.rename(columns = {'team_name': 'team', 'play_pattern_name': 'play_pattern'})
    
    play_patterns = shot_data.get('play_pattern').sort_values(ascending = True).unique()

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
    axs2 = sns.barplot(x = full_minutes['minute'], y = full_minutes['count']).set(title = 'Shot Distribution with 5 Minute Bins')

    shotcol1.pyplot(fig2, axs2)

    fig3 = plt.figure(3)

    shot_reasons = team_shot_data.get('play_pattern')
    sns.set(rc = {'figure.figsize':(15,15)})
    axs3 = sns.countplot(shot_reasons, order = play_patterns).set(title = 'Shots by Play Pattern')

    shotcol2.pyplot(fig3, axs3)

    # RETURN TO TEAM SELECTION
    st.markdown(f"<a href='#{team_select}'>Try a different team?</a>", unsafe_allow_html=True)

    ## PLAYER ANALYSIS SECTION ##
    def calculate_nearest_point(point, other_points):
        smallest_i = 0
        smallest_dist = np.inf 
        for index, check in enumerate(other_points):
            dist = ((check[0] - point[0])**2 + (check[1] - point[1])**2)**0.5
            if dist < smallest_dist:
                smallest_i = index
                smallest_dist = dist
        return other_points[smallest_i]

    st.markdown("### Design Your Own Team")
    st.markdown("Design your own version of **" + team_option + "**. You must choose exactly 11 positions (1 goalkeeper, and 10 of your choice). This will show how your selected players might distribute the ball across the field (examining all their passes from the position and where their closest teammate might be).")
    
    ppa_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/player_pos_averages.csv").set_index(['team_name','position_name','player_name'])
    team_averages = ppa_data.loc[team_option]

    pploc_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/player_positions_endlocs.csv")

    attack = ['Left Wing', 'Right Center Forward', 'Right Wing', 'Striker', 'Left Center Forward', 'Secondary Striker']
    mid = ['Right Defensive Midfield', 'Center Defensive Midfield', 'Left Defensive Midfield', 'Right Midfield', 'Right Center Midfield', 'Center Midfield', 'Left Center Midfield', 'Left Midfield', 'Right Attacking Midfield', 'Center Attacking Midfield', 'Left Attacking Midfield']
    defense = ['Right Back', 'Right Center Back', 'Center Back', 'Left Center Back', 'Left Back', 'Right Wing Back', 'Left Wing Back']

    pos_options = team_averages.index.get_level_values(0).unique()

    att_reduced = sorted([x for x in attack if x in pos_options])
    mid_reduced = sorted([x for x in mid if x in pos_options])
    def_reduced = sorted([x for x in defense if x in pos_options])

    pos_form = st.form("position_widget")
    passcol1, passcol2, passcol3 = pos_form.columns(3)

    goalie_info = []
    att_info = []
    mid_info = []
    def_info = []

    # GOALKEEPER - goes to bottom
    all_options = list(team_averages.loc["Goalkeeper"].index.unique())
    label = 'Choose a Goalkeeper.'
    goalie_name = pos_form.selectbox(label, all_options)
    goalie_info.append(('Goalkeeper', goalie_name))

    # ATTACK POS
    passcol1.markdown("Please choose which attacking positions you would like to include.")
    for val in att_reduced:
        all_options = list(team_averages.loc[val].index.unique())
        inner_options = ["None"] + all_options
        label = 'Choose a ' + val + '.'
        selected_name = passcol1.selectbox(label, inner_options, index = 0)
        if selected_name != 'None':
            att_info.append((val, selected_name))

    # MID POS
    passcol2.markdown("Please choose which midfield positions you would like to include.")
    for val in mid_reduced:
        all_options = list(team_averages.loc[val].index.unique())
        inner_options = ["None"] + all_options
        label = 'Choose a ' + val + '.'
        selected_name = passcol2.selectbox(label, inner_options, index = 0)
        if selected_name != 'None':
            mid_info.append((val, selected_name))

    # DEFENSE POS
    passcol3.markdown("Please choose which defensive positions you would like to include.")
    for val in def_reduced:
        all_options = list(team_averages.loc[val].index.unique())
        inner_options = ["None"] + all_options
        label = 'Choose a ' + val + '.'
        selected_name = passcol3.selectbox(label, inner_options, index = 0)
        if selected_name != 'None':
            def_info.append((val, selected_name))

    pos_submitted = pos_form.form_submit_button("When you have 11 players (10 non-goalie, 1 goalie) selected, click this button.")

    # ADDS AFTER SUBMIT CHECK    
    player_indexes = goalie_info + att_info + mid_info + def_info
    n_selected_pos = len(player_indexes)

    if pos_submitted and n_selected_pos == 11:
        pitch2 = Pitch(pitch_type = 'statsbomb', pitch_color = 'grass', line_color='white', stripe=True)
        fig4, ax4  = pitch2.draw(figsize=(16, 8))

        dot_locations = []

        for duo in player_indexes:
            info = team_averages.loc[duo]
            dot_locations.append((info['location_x'], info['location_y']))
            ax4.scatter(info['location_x'], info['location_y'], label = duo[0], s = 100)
            ax4.text(info['location_x'] + 1, info['location_y'] + 1, s = np.round(info['simple_pass_accuracy'], 2), color = 'yellow', fontweight = 'bold')

        for i, duo in enumerate(player_indexes):
            locs_removed = dot_locations[0:i] + dot_locations[i+1:]
            # COME BACK TO - HOW DO I CREATE A COLOR DICT FOR THIS AND MATCH COLOR
            #st.text(duo[0])
            #st.text(duo[1])
            player_data = pploc_data[(pploc_data['player_name'] == duo[1]) & (pploc_data['position_name'] == duo[0])]
            end_xs = player_data.get('pass_end_location_x')
            end_ys = player_data.get('pass_end_location_y')
            locs = pd.Series(zip(end_xs, end_ys))
            closest_locs = locs.apply(calculate_nearest_point, args = (locs_removed, ))

            counts_closest = closest_locs.value_counts(normalize = True)

            info = team_averages.loc[duo]
            for index, val in counts_closest.iteritems():
                #st.text(index)
                ax4.arrow(x = info['location_x'], y = info['location_y'], dx = index[0] - info['location_x'], dy = index[1] - info['location_y'], color = 'black', lw = val * 3)

        ax4.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
        st.pyplot(fig4, ax4)

        # ADD INFO ABOUT COUNTS - COME BACK TO

        # OLD VERSION OF GRaPH
        # pitch2 = Pitch(pitch_type = 'statsbomb', pitch_color = 'grass', line_color='white', stripe=True)
        # # specifying figure size (width, height)
        # fig4, ax4  = pitch2.draw(figsize=(16, 8))
        # for duo in player_indexes:
        #     info = team_averages.loc[duo]
        #     ax4.arrow(info['location_x'], info['location_y'], info['pass_length'] * np.cos(info['pass_angle']), info['pass_length'] * np.sin(info['pass_angle']), color = 'black', lw = 3)
        #     ax4.scatter(info['location_x'], info['location_y'], label = duo[0], s = 100)
        #     ax4.text(info['location_x'] + 1, info['location_y'] + 1, s = np.round(info['simple_pass_accuracy'], 2), color = 'yellow', fontweight = 'bold')
        # ax4.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
        # st.pyplot(fig4, ax4)

        #st.text('graph here')

    elif pos_submitted and n_selected_pos != 11:
        st.markdown('Please double check that you have selected 11 players exactly.')

    # RETURN TO TEAM SELECTION
    st.markdown(f"<a href='#{team_select}'>Try a different team?</a>", unsafe_allow_html=True)



