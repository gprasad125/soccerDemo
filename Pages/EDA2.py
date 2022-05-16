import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

def page():

    st.markdown("## Design Your Own Team")

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

    num_games = num_games_df.loc[team_option]['count']
    st.info('We have **' + str(num_games) + '** games worth of data for **' + team_option + '**.')

    def make_color_dict(labels):

        palette = sns.color_palette("husl", len(labels))

        event_colors = {}

        for ind, ev in enumerate(labels):
            event_colors[ev] = palette[ind]

        return event_colors

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

    st.markdown("### Choosing Your Team")
    st.markdown("Design your own version of **" + team_option + "**. You must choose exactly 11 positions (1 goalkeeper, and 10 of your choice). This will show how your selected players might distribute the ball across the field (examining all their passes from the position and where their closest teammate might be).")
    
    st.info("If you're not sure where to start, we recommend choosing a 4-3-3 structure (4 defenders, 3 midfielders, and 3 attackers), as that was by far the most common lineup structure in our data.")

    ppa_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/player_pos_averages.csv").set_index(['team_name','position_name','player_name'])
    team_averages = ppa_data.loc[team_option]

    ppc_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/player_pos_counts.csv").set_index(['team_name','position','player_name'])
    team_counts = ppc_data.loc[team_option]

    pploc_data = pd.read_csv("https://media.githubusercontent.com/media/gprasad125/soccerDemo/main/Data/player_positions_endlocs.csv")

    attack = ['Striker', 'Center Forward', 'Left Wing', 'Right Center Forward', 'Right Wing', 'Striker', 'Left Center Forward', 'Secondary Striker']
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
        pitch = Pitch(pitch_type = 'statsbomb', pitch_color = '#D3D3D3', line_color='white')
        fig, ax  = pitch.draw(figsize=(16, 8))

        dot_locations = []

        pos_dict = make_color_dict(np.array(player_indexes)[:, 0])

        for duo in player_indexes:
            info = team_averages.loc[duo]
            dot_locations.append((info['location_x'], info['location_y']))
            ax.scatter(info['location_x'], info['location_y'], label = duo[0], s = 100, c = pos_dict[duo[0]])
            ax.text(info['location_x'] + 1, info['location_y'] + 1, s = np.round(info['simple_pass_accuracy'], 2), color = 'black', fontweight = 'bold')

        st.markdown('Info about the players you picked:')

        info_text = ""
        unknown_trigger = False

        for i, duo in enumerate(player_indexes):
            locs_removed = dot_locations[0:i] + dot_locations[i+1:]
            player_data = pploc_data[(pploc_data['player_name'] == duo[1]) & (pploc_data['position_name'] == duo[0])]
            game_count = 'an unknown # of'

            if duo in team_counts.index:
            	game_count = str(team_counts.loc[duo]['count'])
            else:
            	unknown_trigger = True

            if duo[0] == 'Goalkeeper':
            	info_text = info_text + 'We have **' + game_count + '** games worth of data for **' + duo[1] + '**.\n'
            elif i == n_selected_pos - 1:
            	info_text = info_text + 'We have **' + game_count + '** games worth of data for **' + duo[1] + '** playing as a **' + duo[0] + '**.'
            else:
            	info_text = info_text + 'We have **' + game_count + '** games worth of data for **' + duo[1] + '** playing as a **' + duo[0] + '**.\n'
            end_xs = player_data.get('pass_end_location_x')
            end_ys = player_data.get('pass_end_location_y')
            locs = pd.Series(zip(end_xs, end_ys))
            closest_locs = locs.apply(calculate_nearest_point, args = (locs_removed, ))

            counts_closest = closest_locs.value_counts(normalize = True)

            info = team_averages.loc[duo]
            for index, val in counts_closest.iteritems():
                #st.text(index)
                ax.arrow(x = info['location_x'], y = info['location_y'] - 0.1, dx = index[0] - info['location_x'], dy = index[1] - info['location_y'], color = pos_dict[duo[0]], lw = val * 10)

            plt.title("Basic Passmap for Your Inputted Version of " + team_option)

        ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
        st.pyplot(fig, ax)

        st.markdown(info_text)

        if unknown_trigger:
        	st.info('To get the number of games associated with a player in a given position, we pulled from the StatsBomb lineup data instead of the events data (which we used to get the passes). This is why at least 1 of the players you selected has an unknown number of games associated with them - the given match may have not been accessible from the StatsBomb lineup data, even if it was from the event data.')

        # OLD VERSION OF GRAPH
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
    team_select = 'selecting-a-team'
    st.markdown(f"<a href='#{team_select}'>Try a different team?</a>", unsafe_allow_html=True)
