import gradio as gr
import pandas as pd
import joblib
import numpy as np

# Load model and metadata
model = joblib.load('joblib/rf_model.joblib')
model_columns = joblib.load('joblib/model_columns.joblib')
teams = joblib.load('joblib/teams.joblib')

# Load your original data once for efficiency
data = pd.read_csv('data/Final_Data.csv')  # Reads the CSV file with the match information
data = data.dropna(subset=['FTR'])

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



# Use the main predict function
gr.Interface(
    fn=predict,  # Change to predict_simple if main function doesn't work
    inputs=[
        gr.Dropdown(teams, label="Home Team"),
        gr.Dropdown(teams, label=" Away Team")
    ],
    outputs=gr.Textbox(label="Prediction Result", lines=12),
    title="Premier League Match Outcome Predictor",
    description="Select two teams to predict the match outcome.",
    theme=gr.themes.Soft()
).launch()