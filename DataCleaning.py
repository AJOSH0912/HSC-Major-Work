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
    team_season_stats_passing.to_csv((league + 'passing.csv') , index=True)
    team_season_stats_shooting = fbref.read_team_season_stats(stat_type="shooting")
    team_season_stats_shooting.to_csv((league + 'shooting.csv') , index=True)
    team_season_stats_defense = fbref.read_team_season_stats(stat_type="defense")
    team_season_stats_defense.to_csv((league + 'defense.csv') , index=True)
    team_season_stats_possession = fbref.read_team_season_stats(stat_type="possession")
    team_season_stats_possession.to_csv((league + 'possession.csv') , index=True)
    team_season_stats_goalkeeping = fbref.read_team_season_stats(stat_type="keeper")
    team_season_stats_goalkeeping.to_csv((league + 'keeper.csv') , index=True)
    team_season_stats_gsc = fbref.read_team_season_stats(stat_type="goal_shot_creation")
    team_season_stats_gsc.to_csv((league + 'goal_shot_creation.csv') , index=True)
    team_season_stats_misc = fbref.read_team_season_stats(stat_type="misc")
    team_season_stats_misc.to_csv((league + 'misc.csv') , index=True)

get_store_data('ENG-Premier League')

def extract_columns_to_new_csv(input_filename, output_filename): # A function to make a final csv table with all required information
    # Read with multi-index columns
    df = pd.read_csv(input_filename, header=[0, 1])
    df.columns = [(str(a).strip(), str(b).strip()) for a, b in df.columns]
    print(df.columns.tolist()) # Print all column names for debugging
    team_col = next((col for col in df.columns if col[0].lower() == 'team'), None) # Ensure case-insensitive match
    gls_col = next((col for col in df.columns if col[1] == 'Gls'), None) # Match the second level of the multi-index
    poss_col = next((col for col in df.columns if col[0] == 'Poss'), None) # Match the first level of the multi-index
    print(f"team_col: {team_col}, gls_col: {gls_col}, poss_col: {poss_col}") # Debugging output
    df_selected = pd.DataFrame() # Create an empty DataFrame to store selected columns
    if team_col: df_selected['team'] = df[team_col] #
    if gls_col: df_selected['Gls'] = df[gls_col]
    if poss_col: df_selected['Poss'] = df[poss_col]
    df_selected.to_csv(output_filename, index=False)

input_filename = 'ENG-Premier Leaguestandard.csv'
output_filename = 'selected_columns.csv'

extract_columns_to_new_csv(input_filename, output_filename)


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

