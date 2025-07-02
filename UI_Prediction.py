import gradio as gr
import pandas as pd
import joblib
import numpy as np


data = pd.read_csv('data/Final_Data.csv')  # Reads the CSV file with the match information
data = data.dropna(subset=['FTR'])
team_stats = pd.read_csv('data/Combined.csv')  # Reads the CSV file with the team statistics
player_stats = pd.read_csv('data/Final_Player_Stats.csv')  # Reads the CSV file with the player statistics

# Load model and metadata
model = joblib.load('joblib/rf_model.joblib')
model_columns = joblib.load('joblib/model_columns.joblib')
teams = team_stats['team'].unique().tolist()  # Get unique teams from the team stats DataFrame



def get_prediction_rows(home_team, away_team):


    home_team_columns = ['team_x','team_1_Average_goals_scored_last5','team_1_Average_HT_goals_scored_last5','team_1_Average_shots_last5',
    'team_1_Average_shots_on_target_last5','team_1_Average_fouls_last5','team_1_Average_corners_last5',
    'team_1_Average_yellow_cards_last5','team_1_Average_red_cards_last5','team_1_Average_B365_odds_last5',
    'team_1_Average_B365_draw_odds_last5','team_1_Average_BW_odds_last5','team_1_Average_BW_draw_odds_last5',
    'team_1_Average_WH_odds_last5','team_1_Average_WH_draw_odds_last5','team_1_Average_goals_conceded_last5',
    'team_1_Average_HT_goals_conceded_last5','team_1_Average_shots_conceded_last5','team_1_Average_shots_on_target_conceded_last5',
    'team_1_Average_fouls_conceded_last5','team_1_Average_corners_conceded_last5','team_1_Average_yellow_cards_conceded_last5',
    'team_1_Average_red_cards_conceded_last5','team_1_Average_B365_odds_against_last5','team_1_Average_BW_odds_against_last5',
    'team_1_Average_WH_odds_against_last5','Average_goals_scored_last10_x','team_1_Average_HT_goals_scored_last10',
    'team_1_Average_shots_last10','team_1_Average_shots_on_target_last10','team_1_Average_fouls_last10',
    'team_1_Average_corners_last10','team_1_Average_yellow_cards_last10','team_1_Average_red_cards_last10',
    'team_1_Average_B365_odds_last10','team_1_Average_B365_draw_odds_last10','team_1_Average_BW_odds_last10',
    'team_1_Average_BW_draw_odds_last10','team_1_Average_WH_odds_last10','team_1_Average_WH_draw_odds_last10',
    'team_1_Average_goals_conceded_last10','team_1_Average_HT_goals_conceded_last10','team_1_Average_shots_conceded_last10',
    'team_1_Average_shots_on_target_conceded_last10','team_1_Average_fouls_conceded_last10',
    'team_1_Average_corners_conceded_last10','team_1_Average_yellow_cards_conceded_last10',
    'team_1_Average_red_cards_conceded_last10','team_1_Average_B365_odds_against_last10',
    'team_1_Average_BW_odds_against_last10','team_1_Average_WH_odds_against_last10'	]

    away_team_columns = ['team_y','team_2_Average_goals_scored_last5','team_2_Average_HT_goals_scored_last5','team_2_Average_shots_last5',
    'team_2_Average_shots_on_target_last5','team_2_Average_fouls_last5','team_2_Average_corners_last5',
    'team_2_Average_yellow_cards_last5','team_2_Average_red_cards_last5','team_2_Average_B365_odds_last5',
    'team_2_Average_B365_draw_odds_last5','team_2_Average_BW_odds_last5','team_2_Average_BW_draw_odds_last5',
    'team_2_Average_WH_odds_last5','team_2_Average_WH_draw_odds_last5','team_2_Average_goals_conceded_last5',
    'team_2_Average_HT_goals_conceded_last5','team_2_Average_shots_conceded_last5','team_2_Average_shots_on_target_conceded_last5',
    'team_2_Average_fouls_conceded_last5','team_2_Average_corners_conceded_last5','team_2_Average_yellow_cards_conceded_last5',
    'team_2_Average_red_cards_conceded_last5','team_2_Average_B365_odds_against_last5','team_2_Average_BW_odds_against_last5',
    'team_2_Average_WH_odds_against_last5','Average_goals_scored_last10_y','team_2_Average_HT_goals_scored_last10',
    'team_2_Average_shots_last10','team_2_Average_shots_on_target_last10','team_2_Average_fouls_last10',
    'team_2_Average_corners_last10','team_2_Average_yellow_cards_last10','team_2_Average_red_cards_last10',
    'team_2_Average_B365_odds_last10','team_2_Average_B365_draw_odds_last10','team_2_Average_BW_odds_last10',
    'team_2_Average_BW_draw_odds_last10','team_2_Average_WH_odds_last10','team_2_Average_WH_draw_odds_last10',
    'team_2_Average_goals_conceded_last10','team_2_Average_HT_goals_conceded_last10','team_2_Average_shots_conceded_last10',
    'team_2_Average_shots_on_target_conceded_last10','team_2_Average_fouls_conceded_last10',
    'team_2_Average_corners_conceded_last10','team_2_Average_yellow_cards_conceded_last10',
    'team_2_Average_red_cards_conceded_last10','team_2_Average_B365_odds_against_last10',
    'team_2_Average_BW_odds_against_last10','team_2_Average_WH_odds_against_last10']

    home_row = data[data['team_x'] == home_team].iloc[-1][home_team_columns]
    away_row = data[data['team_y'] == away_team].iloc[-1][away_team_columns]

    return pd.DataFrame([np.concatenate((home_row, away_row))], columns=home_team_columns + away_team_columns)

prediction_row = get_prediction_rows('Arsenal', 'Man City')
prediction_row.to_csv()

# Function to predict match outcome
def predict(home_team, away_team):
    if home_team == away_team:
        return "Please select two different teams."
    if home_team not in teams or away_team not in teams:
        return "Invalid team selection. Please select from the available teams."
    prediction_row = get_prediction_rows(home_team, away_team)
    prediction_row = prediction_row.reindex(columns=model_columns, fill_value=0)  # Ensure all columns are present
    prediction_row = prediction_row.fillna(0)  # Fill any NaN values with 0
    prediction_proba = model.predict_proba(prediction_row)
    result = {
        'Home Win': prediction_proba[0][0],
        'Draw': prediction_proba[0][1],
        'Away Win': prediction_proba[0][2]
    }
    return f"Home Win: {result['Home Win']:.2f}\nDraw: {result['Draw']:.2f}\nAway Win: {result['Away Win']:.2f} "




def view_team_stats(team, selected_columns):
    if team not in teams:
        return pd.DataFrame({"Message": ["Invalid team selection. Please select from the available teams."]})
    
    team_data = team_stats[team_stats['team'] == team]
    if team_data.empty:
        return pd.DataFrame({"Message": [f"No data available for {team}."]})
    
    available_columns = [col for col in selected_columns if col in team_data.columns]
    if not available_columns:
        return pd.DataFrame({"Message": ["No valid columns selected."]})
    
    # Include team column and selected columns
    columns_to_show = ['team'] + available_columns
    filtered_data = team_data[columns_to_show]
    
    return filtered_data

available_stat_columns = [col for col in team_stats.columns if col != 'team']




def view_player_stats(player_name, selected_columns):

    player_exists = player_stats['player'].str.lower().str.contains(player_name.lower(), na=False).any()
    
    if not player_exists:
        return pd.DataFrame({"Message": ["Invalid player selection. Please choose a current premier league player."]})
    
    
    player_data = player_stats[player_stats['player'].str.lower().str.contains(player_name.lower(), na=False)]
    
    available_columns = [col for col in selected_columns if col in player_data.columns]
    if not available_columns:
        return pd.DataFrame({"Message": ["No valid columns selected."]})
    
    columns_to_show = ['player', 'team'] + available_columns
    player_data = player_data[columns_to_show]
    
    if player_data.empty:
        return pd.DataFrame({"Message": ["Please enter a player name."]})
    
    
    return player_data

available_player_columns = [col for col in player_stats.columns if col not in ['player', 'team']]


# Use the main predict function
prediction_interface = gr.Interface(
    fn=predict,  # Change to predict_simple if main function doesn't work
    inputs=[
        gr.Dropdown(teams, label="Home Team"),
        gr.Dropdown(teams, label=" Away Team")
    ],
    outputs=gr.Textbox(label="Prediction Result", lines=12),
    title="Premier League Match Outcome Predictor",
    description="Select two teams to predict the match outcome.",
    theme=gr.themes.Soft()
)


team_stats_interface = gr.Interface(
    fn=view_team_stats,
    inputs=[
        gr.Dropdown(teams, label="Select Team"),
        gr.CheckboxGroup(
            choices = available_stat_columns,
            label="Select Statistics",
            value = available_stat_columns[:5],
        )],
    outputs=gr.Dataframe(label="Team Statistics"),
    title="Team Statistics Viewer",
    description="Select a team to view its statistics.",
    theme=gr.themes.Soft()
)

player_stats_interface = gr.Interface(
    fn=view_player_stats,
    inputs=[
        gr.Textbox(label="Enter Player Name", placeholder="e.g., 'Chris Wood'"),
        gr.CheckboxGroup(
            choices=available_player_columns, 
            label="Select Statistics",
            value=available_player_columns[:5],  
        )
    ],
    outputs=gr.Dataframe(label="Player Statistics"),
    title="Player Statistics Viewer",
    description="Enter a player's name to view their statistics.",
    theme=gr.themes.Soft()
)

UI = gr.TabbedInterface(
    [prediction_interface, team_stats_interface, player_stats_interface],
    tab_names=["Match Outcome Prediction", "Team Seasonal Statistics" , "Player Statistics Viewer"],
    title="Premier League Match Prediction and Statistics Viewer",
)

UI.launch()