import soccerdata as sd
import pandas as pd


mh = sd.MatchHistory(leagues="ENG-Premier League", seasons=[2023, 2024])

#Read the game data
match_history_df = mh.read_games()

csv_filename = "premier_league_match_history.csv"


match_history_df = match_history_df.drop(columns=['Div' , 'Date', 'AF', 'Hf', 'HY', 'AY', 'Referee',])
match_history_df.to_csv(csv_filename, index=False)

