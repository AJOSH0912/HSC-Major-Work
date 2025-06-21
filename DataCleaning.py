import soccerdata as sd
import pandas as pd
import os
import csv

def get_store_data(league: str) -> None:

    file_suffixes = ['standard' , 'passing', 'shooting', 'defense', 'possession', 'keeper', 'goal_shot_creation' , 'misc', 'playing_time']  # List of file suffixes for the CSV files

    # Delete old CSV files when the run button is pressed
    for suffix in file_suffixes:
        filename = f"{league}{suffix}.csv"
        if os.path.exists(filename):
            os.remove(filename)

    fbref = sd.FBref(leagues=league, seasons=2425)

    df = fbref.read_team_season_stats(stat_type="standard") #Calls the specific dataset
    df1 = fbref.read_team_season_stats(stat_type="passing")
    df2 = fbref.read_team_season_stats(stat_type="keeper")
    df3 = fbref.read_team_season_stats(stat_type="defense")
    df4 = fbref.read_team_season_stats(stat_type="possession")
    df5 = fbref.read_team_season_stats(stat_type="shooting")
    df6 = fbref.read_team_season_stats(stat_type="goal_shot_creation")
    df7 = fbref.read_team_season_stats(stat_type="misc")
    df8 = fbref.read_team_season_stats(stat_type="playing_time")
    df = df.reset_index() # Resetting the index so that 'team' , 'league' and 'season' are put back into the heading and out of the data columns
    df1 = df1.reset_index()
    df2 = df2.reset_index()
    df3 = df3.reset_index()
    df4 = df4.reset_index()
    df5 = df5.reset_index()
    df6 = df6.reset_index()
    df7 = df7.reset_index()
    df8 = df8.reset_index()

    df1.to_csv(f"{league}passing.csv", index=False)  # Save each DataFrame to a CSV file
    df2.to_csv(f"{league}keeper.csv", index=False)
    df3.to_csv(f"{league}defense.csv", index=False)
    df4.to_csv(f"{league}possession.csv", index=False)
    df5.to_csv(f"{league}shooting.csv", index=False)
    df6.to_csv(f"{league}goal_shot_creation.csv", index=False)
    df7.to_csv(f"{league}misc.csv", index=False)
    df8.to_csv(f"{league}playing_time.csv", index=False)
    df.to_csv(f"{league}standard.csv", index=False)

    # Flatten multi-index columns if present for all DataFrames
    dfs = [df, df1, df2, df3, df4, df5, df6, df7, df8]
    for i, d in enumerate(dfs):
        d.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in d.columns] #Combines both rows of the heading so that it is all 1 row and can be called on
        # print(f"df{i} columns: {d.columns.tolist()}")  # Debuging purposes


    df = df[['team', 'league', 'season', 'Performance Gls' , "Poss" , "Expected xAG" , "Expected xG" , "Per 90 Minutes G+A"]]
    df1 = df1[['team', 'league', 'season', 'Ast' , 'Total Att', 'PPA']]
    df2 = df2[['team', 'league', 'season', 'Performance Save%', 'Performance W', 'Performance L']]
    df3 = df3[['team', 'league', 'season']]
    df4 = df4[['team', 'league', 'season', 'Touches Touches', 'Touches Att 3rd', 'Take-Ons Succ%' ]]
    df5 = df5[['team', 'league', 'season', 'Standard Sh']]
    df6 = df6[['team', 'league', 'season' , 'SCA SCA', 'SCA Types PassDead', 'GCA GCA', 'GCA Types PassLive']]
    df7 = df7[['team', 'league', 'season']]
    df8 = df8[['team', 'league', 'season', 'Team Success PPM', 'Team Success +/-']]

    df_combined = pd.merge(df, df1, on=['team', 'league', 'season'], how='left') #Merges all the dataframes 
    df_combined = pd.merge(df_combined, df2, on=['team', 'league', 'season'], how='left')
    df_combined = pd.merge(df_combined, df3, on=['team', 'league', 'season'], how='left')
    df_combined = pd.merge(df_combined, df4, on=['team', 'league', 'season'], how='left')
    df_combined = pd.merge(df_combined, df5, on=['team', 'league', 'season'], how='left')
    df_combined = pd.merge(df_combined, df6, on=['team', 'league', 'season'], how='left')
    df_combined = pd.merge(df_combined, df7, on=['team', 'league', 'season'], how='left')
    df_combined = pd.merge(df_combined, df8, on=['team', 'league', 'season'], how='left')


    filename = 'Combined.csv'  # Name of the output file
    if os.path.exists(filename):  # Check if 'Combined.csv' exists
        os.remove(filename) # Removes existing 'Combined.Csv' file so that when run, a new file will be created

    df_combined.to_csv('Combined.csv', index=True) #Turns the data into a csv file so that it can be viewed


get_store_data('ENG-Premier League')

mh = sd.MatchHistory(leagues="ENG-Premier League", seasons=[2425])

#Read the game data
match_history_df = mh.read_games()

csv_filename = "premier_league_match_history.csv"


match_history_df = match_history_df.drop(columns=[ 'AF', 'HF', 'HY', 'AY', 'referee', 'BFH','BFD','BFA','1XBH','1XBD','1XBA','BFEH','BFED','BFEA','BFE>2.5','BFE<2.5','BFEAHH','BFEAHA','BFCH','BFCA','1XBCH','1XBCD','1XBCA','BFECH','BFECD','BFECA','BFEC>2.5','BFEC<2.5','BFECAHH','BFECAHA','BFCD'])  # Drop unnecessary columns
match_history_df.to_csv(csv_filename, index=False)

