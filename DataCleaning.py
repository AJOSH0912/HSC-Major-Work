import soccerdata as sd
import pandas as pd
import os
import csv

def get_store_data(league: str) -> None:

    file_suffixes = ['standard' , 'passing', 'shooting', 'defense', 'possession', 'keeper', 'goal_shot_creation' , 'misc']

    # Delete old CSV files when the run button is pressed
    for suffix in file_suffixes:
        filename = f"{league}{suffix}.csv"
        if os.path.exists(filename):
            os.remove(filename)

    fbref = sd.FBref(leagues=league, seasons=2425)


# Asigns the different data to a variable and turns it into a csv file so I can see the data clearly
    team_season_stats_standard = fbref.read_team_season_stats(stat_type="standard")
    team_season_stats_standard = team_season_stats_standard.reset_index()
    team_season_stats_standard.to_csv((league + 'standard.csv') , index=True)
    team_season_stats_passing = fbref.read_team_season_stats(stat_type="passing")
    team_season_stats_passing = team_season_stats_passing.reset_index()
    team_season_stats_passing.to_csv((league + 'passing.csv') , index=True)
    team_season_stats_shooting = fbref.read_team_season_stats(stat_type="shooting")
    team_season_stats_shooting = team_season_stats_shooting.reset_index()
    team_season_stats_shooting.to_csv((league + 'shooting.csv') , index=True)
    team_season_stats_defense = fbref.read_team_season_stats(stat_type="defense")
    team_season_stats_defense = team_season_stats_defense.reset_index()
    team_season_stats_defense.to_csv((league + 'defense.csv') , index=True)
    team_season_stats_possession = fbref.read_team_season_stats(stat_type="possession")
    team_season_stats_possession = team_season_stats_possession.reset_index()
    team_season_stats_possession.to_csv((league + 'possession.csv') , index=True)
    team_season_stats_goalkeeping = fbref.read_team_season_stats(stat_type="keeper")
    team_season_stats_goalkeeping = team_season_stats_goalkeeping.reset_index()
    team_season_stats_goalkeeping.to_csv((league + 'keeper.csv') , index=True)
    team_season_stats_gsc = fbref.read_team_season_stats(stat_type="goal_shot_creation")
    team_season_stats_gsc = team_season_stats_gsc.reset_index()
    team_season_stats_gsc.to_csv((league + 'goal_shot_creation.csv') , index=True)
    team_season_stats_misc = fbref.read_team_season_stats(stat_type="misc")
    team_season_stats_misc = team_season_stats_misc.reset_index()
    team_season_stats_misc.to_csv((league + 'misc.csv') , index=True)
    team_season_stats_playing_time = fbref.read_team_season_stats(stat_type="playing_tme")
    team_season_stats_playing_time = team_season_stats_playing_time.reset_index()
    team_season_stats_playing_time.to_csv((league + 'playing_time.csv') , index=True)

get_store_data('ENG-Premier League')



# def extract_columns_to_new_csv_multi(input_files, output_filename, column_map):
#     dfs = {}
#     for fname, _ in input_files:
#         df = pd.read_csv(fname, header=[0, 1])
#         df.columns = [(str(a).strip(), str(b).strip()) for a, b in df.columns]
#         dfs[fname] = df
#     out = pd.DataFrame()
#     for outcol, (fname, coltuple) in column_map.items():
#         out[outcol] = dfs[fname][coltuple]
#     out.to_csv(output_filename, index=False)

# output_filename = 'selected_columns.csv'


# Below is script for debugging purposes, it prints specific columns from a CSV file to ensure that the index has been reset and all values are in their proper positions so that they can be called

# def print_specific_columns(filename, column_indices):
#     with open(filename, 'r') as file:
#         csv_reader = csv.reader(file)
#         for row in csv_reader:
#             selected_columns = [row[i] for i in column_indices]
#             print(selected_columns)

# filename = 'ENG-Premier Leaguestandard.csv'
# column_indices = [0, 2]

# print_specific_columns(filename, column_indices)

