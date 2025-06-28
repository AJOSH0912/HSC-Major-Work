import numpy as np
import pandas as pd
import os

merged_data2 = pd.read_csv('data/merged_data2.csv') #Reads the CSV file with the match information


"The below first removes any rows with emtpy values becasue teh model will not be able to handle them"



merged_data2 = merged_data2.sort_values(by=['date'], ascending=False) # sort by date in descending order

merged_data2 = merged_data2.dropna() #drop rows with any NaN values



"The below is where we start changing the data so we can feature engineer, we will be adding rolling averages and other features to the data to help the model learn better"
#Initial model accuracy = 0.61


# Creates a new DataFrame with team statistics for both home and away teams so that it shows each teams stats for each game individually ie. not with the other team in the match
def create_team_stats(df):


    home_df = df.copy()
    home_df['team'] = home_df['home_team'] #Creates a new column called  with the same value from the original dataframe
    home_df['home_away'] = 'H' 
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
    home_df['GoalsConceded'] = home_df['FTAG']
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
    away_df['team'] = away_df['away_team']
    away_df['home_away'] = 'A'
    away_df['GoalsScored'] = away_df['FTAG']
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
    away_df['GoalsConceded'] = away_df['FTHG']
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
        'date', 'team', 'home_away', 'GoalsScored', 'HTGoalsScored', 
        'Shots', 'ShotsOnTarget', 'Fouls', 'Corners', 'YellowCards', 'RedCards',
        'B365Odds', 'B365DrawOdds', 'BWOdds', 'BWDrawOdds', 'WHOdds', 'WHDrawOdds',
        'FullTimeResult', 'GoalsConceded', 'HTGoalsConceded', 'shotsConceded', 
        'shotsOnTargetConceded', 'foulsConceded', 'cornersConceded', 
        'yellowCardsConceded', 'redCardsConceded', 'B365OddsAgainst', 'BWOddsAgainst', 'WHOddsAgainst'
    ]
    
    home_stats = home_df[cols]
    away_stats = away_df[cols]
    
    return pd.concat([home_stats, away_stats], ignore_index=True) # Combines the home and away stats vertically into single dataframe

team_stats = create_team_stats(merged_data2) # Create a new DataFrame based on the merged data file
team_stats.to_csv('data/team_stats.csv', index=False) # Saves the team stats to a CSV file


# Creates the columns ffor the average of the last 10 matches for each team
avg_last10_columns = [
    'Average_goals_scored_last10', 'Average_HT_goals_scored_last10',
    'Average_shots_last10', 'Average_shots_on_target_last10', 'Average_fouls_last10',
    'Average_corners_last10', 'Average_yellow_cards_last10', 'Average_red_cards_last10',
    'Average_goals_conceded_last10', 'Average_HT_goals_conceded_last10',
    'Average_shots_conceded_last10', 'Average_shots_on_target_conceded_last10', 'Average_fouls_conceded_last10',
    'Average_corners_conceded_last10', 'Average_yellow_cards_conceded_last10', 'Average_red_cards_conceded_last10',
    'Average_B365Odds_last10', 'Average_B365Odds_Against_last10', 'Average_B365DrawOdds_last10', 'Average_BWOdds_last10', 
    'Average_BWOdds_against_last10', 'Average_BWDrawOdds_last10', 'Average_WHOdds_last10', 'Average_WHOdds_Against_last10', 'Average_WHDrawOdds_last10']

team_stats1 = team_stats.drop(columns=['FullTimeResult'])
Last10_list = [] # List to store the last 10 matches stats for each team

#Finds the average the last 10 matches for each team and appends it to the Last10_list
for index, row in team_stats1.iterrows():
    team_stats_last10 = team_stats1.loc[(team_stats1['team']==row['team']) & (team_stats1['date']<row['date'])].sort_values(by=['date'], ascending=False)
    Last10_list.append(team_stats_last10.iloc[0:10,3:-1].mean(axis=0).values[0:24])

# Creates a DataFrame from the Last10_list and assigns the average last 10 columns to it
avg_lastTen_stats_per_team = pd.DataFrame(Last10_list, columns= avg_last10_columns[:24])
avg_lastTen_stats_per_team.to_csv('data/avg_lastTen_stats_per_team.csv', index=False) # Saves the average last 10 stats per team to a CSV file