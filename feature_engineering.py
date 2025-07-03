import numpy as np
import pandas as pd
import os
import helper as hp # Importing the helper module for encryption and decryption functions

merged_data2 = pd.read_csv('data/raw_merged_data.csv') #Reads the CSV file with the match information


"The below first removes any rows with emtpy values becasue teh model will not be able to handle them"



merged_data2 = merged_data2.sort_values(by=['date'], ascending=False) # sort by date in descending order

merged_data2 = merged_data2.dropna() #drop rows with any NaN values



"The below is where we start changing the data so we can feature engineer, we will be adding rolling averages and other features to the data to help the model learn better"



# Creates a new DataFrame with team statistics for both home and away teams so that it shows each teams stats for each game individually ie. not with the other team in the match just viewing stats in temrs of a certain team
def create_team_stats(df):


    home_df = df.copy() # Creates a copy of the original dataframe to work with for the home team stats
    home_df['match_id'] = home_df['match_id'] 
    home_df['team'] = home_df['home_team'] #Creates a new column called  with the same value from the original dataframe
    home_df['home_away'] = 'H' # Indicates that this is the home team stats
    home_df['GoalsScored'] = home_df['FTHG']
    home_df['HTGoalsScored'] = home_df['HTHG']
    home_df['Shots'] = home_df['HS']
    home_df['ShotsOnTarget'] = home_df['HST']
    home_df['Fouls'] = home_df['HF']
    home_df['Corners'] = home_df['HC']
    home_df['YellowCards'] = home_df['HY']
    home_df['RedCards'] = home_df['HR']
    home_df['B365Odds'] = home_df['B365H']
    home_df['B365DrawOdds'] = home_df['B365D']
    home_df['BWOdds'] = home_df['BWH']
    home_df['BWDrawOdds'] = home_df['BWD']
    home_df['WHOdds'] = home_df['WHH']
    home_df['WHDrawOdds'] = home_df['WHD']
    home_df['FullTimeResult'] = home_df['FTR']
    home_df['GoalsConceded'] = home_df['FTAG'] #Changing the the aways teams stats to 'conceded' as we are looking at the game from the home team's perspective
    home_df['HTGoalsConceded'] = home_df['HTAG']
    home_df['shotsConceded'] = home_df['AS']
    home_df['shotsOnTargetConceded'] = home_df['AST']
    home_df['foulsConceded'] = home_df['AF']
    home_df['cornersConceded'] = home_df['AC']
    home_df['yellowCardsConceded'] = home_df['AY']
    home_df['redCardsConceded'] = home_df['AR']
    home_df['B365OddsAgainst'] = home_df['B365A']
    home_df['BWOddsAgainst'] = home_df['BWA']
    home_df['WHOddsAgainst'] = home_df['WHA']
    
    # Away team perspective  
    away_df = df.copy()
    away_df['match_id'] = away_df['match_id']
    away_df['team'] = away_df['away_team']
    away_df['home_away'] = 'A'
    away_df['GoalsScored'] = away_df['FTAG'] # Making the columns more readable by renaming them to be more descriptive
    away_df['HTGoalsScored'] = away_df['HTAG']
    away_df['Shots'] = away_df['AS']
    away_df['ShotsOnTarget'] = away_df['AST']
    away_df['Fouls'] = away_df['AF']
    away_df['Corners'] = away_df['AC']
    away_df['YellowCards'] = away_df['AY']
    away_df['RedCards'] = away_df['AR']
    away_df['B365Odds'] = away_df['B365A']
    away_df['BWOdds'] = away_df['BWA']
    away_df['WHOdds'] = away_df['WHA']
    away_df['FullTimeResult'] = away_df['FTR']
    away_df['GoalsConceded'] = away_df['FTHG'] # Changing the the home teams stats to 'conceded' as we are looking at the game from the away team's perspective
    away_df['HTGoalsConceded'] = away_df['HTHG']
    away_df['shotsConceded'] = away_df['HS']
    away_df['shotsOnTargetConceded'] = away_df['HST']
    away_df['foulsConceded'] = away_df['HF']
    away_df['cornersConceded'] = away_df['HC']
    away_df['yellowCardsConceded'] = away_df['HY']
    away_df['redCardsConceded'] = away_df['HR']
    away_df['B365OddsAgainst'] = away_df['B365H']
    away_df['BWOddsAgainst'] = away_df['BWH']
    away_df['WHOddsAgainst'] = away_df['WHH']
    away_df['B365DrawOdds'] = away_df['B365D']
    away_df['BWDrawOdds'] = away_df['BWD']
    away_df['WHDrawOdds'] = away_df['WHD']
    
    # Selects the columns I want: Eg: HTGoalsScored = HTAG , but I want to rename it to HTGoalsScored so that the I can understand it better
    cols = [
        'date', 'match_id', 'team', 'home_away', 'GoalsScored', 'HTGoalsScored', 
        'Shots', 'ShotsOnTarget', 'Fouls', 'Corners', 'YellowCards', 'RedCards',
        'B365Odds', 'B365DrawOdds', 'BWOdds', 'BWDrawOdds', 'WHOdds', 'WHDrawOdds',
        'FullTimeResult', 'GoalsConceded', 'HTGoalsConceded', 'shotsConceded', 
        'shotsOnTargetConceded', 'foulsConceded', 'cornersConceded', 
        'yellowCardsConceded', 'redCardsConceded', 'B365OddsAgainst', 'BWOddsAgainst', 'WHOddsAgainst'
    ]
    
    #Makes 2 new dataframes for the home and away teams with the selected columns so we can stack on top of each other
    home_stats = home_df[cols]
    away_stats = away_df[cols]
    
    return pd.concat([home_stats, away_stats], ignore_index=True) # Combines the home and away stats vertically into single dataframe

team_stats = create_team_stats(merged_data2) # Create a new DataFrame based on the merged data file


'The below is where we start getting the rolling averages for the last 10 matches. This is the reason we needed to stack each team vertically.'

avg_last10_columns = [
    'Average_goals_scored_last10', 'Average_HT_goals_scored_last10',
    'Average_shots_last10', 'Average_shots_on_target_last10', 'Average_fouls_last10',
    'Average_corners_last10', 'Average_yellow_cards_last10', 'Average_red_cards_last10',
    'Average_B365_odds_last10', 'Average_B365_draw_odds_last10', 'Average_BW_odds_last10',
    'Average_BW_draw_odds_last10', 'Average_WH_odds_last10', 'Average_WH_draw_odds_last10', 
    'Average_FullTimeResult_last10',
    'Average_goals_conceded_last10', 'Average_HT_goals_conceded_last10',
    'Average_shots_conceded_last10', 'Average_shots_on_target_conceded_last10',
    'Average_fouls_conceded_last10', 'Average_corners_conceded_last10',
    'Average_yellow_cards_conceded_last10', 'Average_red_cards_conceded_last10',
    'Average_B365_odds_against_last10', 'Average_BW_odds_against_last10',
    'Average_WH_odds_against_last10']

team_stats = team_stats.sort_values(['team', 'date']) # Sorts the team stats by team and date to ensure the last 10 matches are correctly calculated
#team_stats.to_csv('data/temp/team_stats.csv', index=False) # Saves the sorted team stats to a CSV file

#Calclates the rolling average for the last 10 matches for each team by taking all the columns 4th and onward and 
# calculating the rolling average for each team with a window of 10 matches, shifting by 1 to avoid including the current match in the average
rolling_average_last10 = (

team_stats
    .groupby('team')
    .apply(lambda group: group.iloc[:, 4:].shift(1).rolling(window=10, min_periods=1).mean())
    .reset_index(level=0, drop=True)

)


rolling_average_last10.columns = avg_last10_columns # Renames the columns to the average last 10 matches columns
rolling_average_last10.drop(columns=['Average_FullTimeResult_last10'], inplace=True) # Drops the FullTimeResult column as it is not needed for the rolling average
rolling_average_last10 = pd.concat([team_stats[['team', 'date', 'match_id' , 'home_away']], rolling_average_last10], axis=1) # Combines the team, date, home_away columns with the rolling average columns
#rolling_average_last10.to_csv('data/temp/rolling_average_last10.csv', index=False) # Saves the rolling average last 10 matches to a CSV file



'The below is where we start getting the rolling averages for the last 5 matches. This will take into account home and away matches separately giving us more features'

avg_last5_home_columns = [
    'Average_goals_scored_last5', 'Average_HT_goals_scored_last5',
    'Average_shots_last5', 'Average_shots_on_target_last5', 'Average_fouls_last5',
    'Average_corners_last5', 'Average_yellow_cards_last5', 'Average_red_cards_last5',
    'Average_B365_odds_last5', 'Average_B365_draw_odds_last5', 'Average_BW_odds_last5',
    'Average_BW_draw_odds_last5', 'Average_WH_odds_last5', 'Average_WH_draw_odds_last5',
    'Average_FullTimeResult_last5',
    'Average_goals_conceded_last5', 'Average_HT_goals_conceded_last5',
    'Average_shots_conceded_last5', 'Average_shots_on_target_conceded_last5',
    'Average_fouls_conceded_last5', 'Average_corners_conceded_last5',
    'Average_yellow_cards_conceded_last5', 'Average_red_cards_conceded_last5',
    'Average_B365_odds_against_last5', 'Average_BW_odds_against_last5',
    'Average_WH_odds_against_last5']


home_matches = team_stats[team_stats['home_away'] == 'H'].copy() # Filters the team stats for home matches

home_matches = home_matches.sort_values(['team', 'date']) # Sorts the home matches by team and date

# Calculates the rolling average for the last 5 matches for each team by taking all the columns 4th and onward and
# calculating the rolling average for each team with a window of 5 matches, shifting by 1 to avoid including the current match in the average
rolling_average_last5_home = (
    home_matches
    .groupby('team')
    .apply(lambda group: group.iloc[:, 4:].shift(1).rolling(window=5, min_periods=1).mean())
    .reset_index(level=0, drop=True)
)

rolling_average_last5_home.columns = avg_last5_home_columns # Renames the columns to the average last 5 matches columns
rolling_average_last5_home.drop(columns=['Average_FullTimeResult_last5'], inplace=True) # Drops the FullTimeResult column as it is not needed for the rolling average
rolling_average_last5_home = pd.concat([home_matches[['team', 'date', 'match_id']], rolling_average_last5_home], axis=1) # Combines the team and date columns with the rolling average columns
# rolling_average_last5_home.to_csv('data/temp/rolling_average_last5_home.csv', index=False) # Saves the rolling average last 5 home matches to a CSV file



avg_last5_away_columns = [
    'Average_goals_scored_last5', 'Average_HT_goals_scored_last5',
    'Average_shots_last5', 'Average_shots_on_target_last5', 'Average_fouls_last5',
    'Average_corners_last5', 'Average_yellow_cards_last5', 'Average_red_cards_last5',
    'Average_B365_odds_last5', 'Average_B365_draw_odds_last5', 'Average_BW_odds_last5',
    'Average_BW_draw_odds_last5', 'Average_WH_odds_last5', 'Average_WH_draw_odds_last5',
    'Average_FullTimeResult_last5',
    'Average_goals_conceded_last5', 'Average_HT_goals_conceded_last5',
    'Average_shots_conceded_last5', 'Average_shots_on_target_conceded_last5',
    'Average_fouls_conceded_last5', 'Average_corners_conceded_last5',
    'Average_yellow_cards_conceded_last5', 'Average_red_cards_conceded_last5',
    'Average_B365_odds_against_last5', 'Average_BW_odds_against_last5',
    'Average_WH_odds_against_last5']

away_matches = team_stats[team_stats['home_away'] == 'A'].copy() # Filters the team stats for away matches
away_matches = away_matches.sort_values(['team', 'date']) # Sorts the away matches by team and date

#Calculates rolling average for the last 5 away matches
rolling_average_last5_away = (
    away_matches
    .groupby('team')
    .apply(lambda group: group.iloc[:, 4:].shift(1).rolling(window=5, min_periods=1).mean())
    .reset_index(level=0, drop=True)
)

rolling_average_last5_away.columns = avg_last5_away_columns # Renames the columns to the average last 5 matches columns
rolling_average_last5_away.drop(columns=['Average_FullTimeResult_last5'], inplace=True) # Drops the FullTimeResult column as it is not needed for the rolling average
rolling_average_last5_away = pd.concat([away_matches[['team', 'date', 'match_id']], rolling_average_last5_away], axis=1) # Combines the team and date columns with the rolling average columns
#rolling_average_last5_away.to_csv('data/temp/rolling_average_last5_away.csv', index=False) # Saves the rolling average last 5 away matches to a CSV file 

# Renames the columns to include team_1_ for the away team for when we merge later
rolling_average_last5_home.columns = rolling_average_last5_home.columns[:3].tolist() + ['team_1_'+str(col) for col in rolling_average_last5_home.columns[3:]] 

# Renames the columns to include team_2_ for the away team for when we merge later
rolling_average_last5_away.columns = rolling_average_last5_away.columns[:3].tolist() + ['team_2_'+str(col) for col in rolling_average_last5_away.columns[3:]] 

# Merges the last 5 home and away matches dataframes on team, date and match_id
Last5_Home_Away = pd.merge( rolling_average_last5_home, rolling_average_last5_away, on=['match_id' , 'date'], how='left') 

# Last5_Home_Away.to_csv('data/temp/Last5_Home_Away.csv', index=False) # Saves the last 5 home and away matches to a CSV file

# Creates a copy of the rolling average last 10 matches for home teams so that we can put them side to side again with pd merge
home_team = rolling_average_last10[rolling_average_last10['home_away'] == 'H'].copy() 
away_team = rolling_average_last10[rolling_average_last10['home_away'] == 'A'].copy() 

# Drops the team and home_away columns from the home and away teams dataframes so that we can merge them later without doubling up
home_team = home_team.drop(['team', 'home_away'], axis=1)  # Keep only match_id, date, and stats
away_team = away_team.drop(['team', 'home_away'], axis=1)  # Keep only match_id, date, and stats

home_team.columns = home_team.columns[:3].tolist() + ['team_1_'+str(col) for col in home_team.columns[3:]] # Renames the columns to include team_1_ for the home team for when we merge later
away_team.columns = away_team.columns[:3].tolist() + ['team_2_'+str(col) for col in away_team.columns[3:]] # Renames the columns to include team_2_ for the away team for when we merge later

last10_stats = pd.merge(home_team, away_team, on=['match_id', 'date'], how='left') # Merges the last 10 home and away matches dataframes on team, date and match_id

last10_stats = last10_stats.dropna().reset_index(drop=True) # Drops any rows with empty values
Last5_Home_Away = Last5_Home_Away.dropna().reset_index(drop=True) # Drops any rows with empty values

# Merges the last 5 home and away matches with the last 10 home and away matches on team, date and match_id giving us our almost finished dataset
Combined_data = pd.merge(Last5_Home_Away, last10_stats, on=['match_id', 'date'], how='left') 
#Combined_data.to_csv('data/Combined_data.csv', index=False) # Saves the final data to a CSV file

# Merges the combined data with the original merged data to get the FullTimeResult column since it is our target variable
Final_data = pd.merge(Combined_data, merged_data2[['date', 'match_id', 'FTR']], on=['match_id', 'date'], how='left') # Merges the final data with the team stats to get the FullTimeResult column

Final_data.to_csv('data/Final_data.csv', index=False) # Saves the final data with the FullTimeResult column to a CSV file
hp.encrypt_file('data/Final_data.csv', 'app.key')