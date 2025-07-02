import soccerdata as sd
import pandas as pd
import os
import csv

def update_team_name_df(df) -> pd.DataFrame:
    df_copy = df.copy()  # Work on a copy to avoid modifying original
    
    # Use the more efficient replace method instead of iterrows
    team_name_mapping = {
        'Manchester Utd': 'Man United',
        'Manchester City': 'Man City',
        'Tottenham Hotspur': 'Tottenham',
        'Brighton & Hove Albion': 'Brighton',
        'West Ham United': 'West Ham',
        'Newcastle Utd': 'Newcastle',
        'Wolverhampton Wanderers': 'Wolves',
        'Leicester City': 'Leicester',
        'Sheffield United': 'Sheffield Utd',
        "Nott'ham Forest": "Nott'm Forest",
        'Ipswich Town': 'Ipswich'
    }
    
    # Replace all team names at once - this is much more efficient and avoids the Series ambiguity error
    df_copy['team'] = df_copy['team'].replace(team_name_mapping)
    return df_copy

def get_store_data(league: str) -> pd.DataFrame:

    
    fbref = sd.FBref(leagues=league, seasons=2425)
    df =  fbref.read_team_season_stats(stat_type="standard") #Calls the specific dataset
    df1 = fbref.read_team_season_stats(stat_type="passing")
    df2 =  fbref.read_team_season_stats(stat_type="keeper")
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
    
    df =  update_team_name_df(df) #Calls the specific dataset
    df1 = update_team_name_df(df1)
    df2 = update_team_name_df(df2)
    df3 = update_team_name_df(df3)
    df4 = update_team_name_df(df4)
    df5 = update_team_name_df(df5)
    df6 = update_team_name_df(df6)
    df7 = update_team_name_df(df7)
    df8 = update_team_name_df(df8)

    # df1.to_csv(f"{league}passing.csv", index=False)  # Save each DataFrame to a CSV file
    # df2.to_csv(f"{league}keeper.csv", index=False)
    # df3.to_csv(f"{league}defense.csv", index=False)
    # df4.to_csv(f"{league}possession.csv", index=False)
    # df5.to_csv(f"{league}shooting.csv", index=False)
    # df6.to_csv(f"{league}goal_shot_creation.csv", index=False)
    # df7.to_csv(f"{league}misc.csv", index=False)
    # df8.to_csv(f"{league}playing_time.csv", index=False)
    # df.to_csv(f"{league}standard.csv", index=False)

    # Flatten multi-index columns if present for all DataFrames
    dfs = [df, df1, df2, df3, df4, df5, df6, df7, df8]
    for i, d in enumerate(dfs):
        d.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in d.columns] #Combines both rows of the heading so that it is all 1 row and can be called on
        # print(f"df{i} columns: {d.columns.tolist()}")  # Debuging purposes


    df = df[['team', 'league', 'season', 'Performance Gls' , "Poss" , "Expected xAG" , "Expected xG" , "Per 90 Minutes G+A"]]
    df1 = df1[['team', 'league', 'season', 'Ast' , 'PPA']]
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
        os.remove(filename) # Removes existing 'Combined.csv' file so that when run, a new file will be created

    return df_combined  # Returns the combined DataFrame with all the relevant data

def get_season_stats(df):
    
    Seasonal_Stats = df.copy()  # Creates a copy of the combined DataFrame to avoid modifying the original data
    Seasonal_Stats['team'] = Seasonal_Stats['team']
    Seasonal_Stats['Goals_This_Season'] = Seasonal_Stats['Performance Gls']
    Seasonal_Stats['Possession_This_Season(%)'] = Seasonal_Stats['Poss']
    Seasonal_Stats['Expected_Assisted_Goals(%)'] = Seasonal_Stats['Expected xAG']
    Seasonal_Stats['Likelyhood_Of_Shot_Scoring'] = Seasonal_Stats['Expected xG']
    Seasonal_Stats['Goals_and_Assists_Per_90_Minutes'] = Seasonal_Stats['Per 90 Minutes G+A']
    Seasonal_Stats['Assists_This_Season'] = Seasonal_Stats['Ast']
    Seasonal_Stats['Passes_into_the_Penalty_Box'] = Seasonal_Stats['PPA']
    Seasonal_Stats['Save_Percentage'] = Seasonal_Stats['Performance Save%']
    Seasonal_Stats['Wins'] = Seasonal_Stats['Performance W']
    Seasonal_Stats['Losses'] = Seasonal_Stats['Performance L']
    Seasonal_Stats['Overall_Touches'] = Seasonal_Stats['Touches Touches']
    Seasonal_Stats['Touches_in_Attacking_Third'] = Seasonal_Stats['Touches Att 3rd']
    Seasonal_Stats['Successful_Take_Ons(%)'] = Seasonal_Stats['Take-Ons Succ%']
    Seasonal_Stats['Shots_This_Season'] = Seasonal_Stats['Standard Sh']
    Seasonal_Stats['Shot_Creating_Actions'] = Seasonal_Stats['SCA SCA']
    Seasonal_Stats['Shot_Creating_Actions_PassDead'] = Seasonal_Stats['SCA Types PassDead']
    Seasonal_Stats['Goal_Creating_Actions'] = Seasonal_Stats['GCA GCA']
    Seasonal_Stats['Goal_Creating_Actions_PassLive'] = Seasonal_Stats['GCA Types PassLive']
    Seasonal_Stats['Average_Points_Per_Match'] = Seasonal_Stats['Team Success PPM']
    Seasonal_Stats['Goal_Difference'] = Seasonal_Stats['Team Success +/-']
    
    columns = [
        'team', 'Goals_This_Season', 'Possession_This_Season(%)', 'Expected_Assisted_Goals(%)',
        'Likelyhood_Of_Shot_Scoring', 'Goals_and_Assists_Per_90_Minutes', 'Assists_This_Season',
        'Passes_into_the_Penalty_Box', 'Save_Percentage', 'Wins', 'Losses', 'Overall_Touches',
        'Touches_in_Attacking_Third', 'Successful_Take_Ons(%)', 'Shots_This_Season',
        'Shot_Creating_Actions', 'Shot_Creating_Actions_PassDead', 'Goal_Creating_Actions',
        'Goal_Creating_Actions_PassLive', 'Average_Points_Per_Match', 'Goal_Difference'
        ]
    
    Seasonal_Stats = Seasonal_Stats[columns]  # Selects only the relevant columns for the seasonal stats DataFrame
    return Seasonal_Stats  # Returns the seasonal stats DataFrame

df_combined = get_store_data('ENG-Premier League')  # Calls the function to get the combined data for the Premier League
Seasonal_stats = get_season_stats(df_combined)  # Calls the function to get the seasonal stats from the combined data

Seasonal_stats.to_csv('data/Combined.csv', index=False) #Turns the data into a csv file so that it can be viewed

