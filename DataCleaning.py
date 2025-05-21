import soccerdata as sd
import pandas as pd
import os

def get_store_data(league: str) -> None:

    file_suffixes = ['standard' , 'passing', 'shooting', 'defense', 'possession', 'keeper', 'goal_shot_creation' , 'misc']

    # Delete old CSV files when the run button is pressed
    for suffix in file_suffixes:
        filename = f"{league}{suffix}.csv"
        if os.path.exists(filename):
            os.remove(filename)

    fbref = sd.FBref(leagues=league, seasons=2425)

    team_season_stats_standard = fbref.read_team_season_stats(stat_type="standard")
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