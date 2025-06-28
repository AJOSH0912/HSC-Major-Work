import gradio as gr
import pandas as pd
import joblib

# Load model and metadata
model = joblib.load('rf_model.joblib')
model_columns = joblib.load('model_columns.joblib')
teams = joblib.load('teams.joblib')

# Load your original data once for efficiency
data = pd.read_csv('data/merged_data2.csv')  # Reads the CSV file with the match information
data = data.dropna(subset=['FTR'])

def predict(home_team, away_team):
    wassup = "hello"

    return wassup


gr.Interface(
    fn=predict,
    inputs=[
        gr.Dropdown(teams, label="Home Team"),
        gr.Dropdown(teams, label="Away Team")
    ],
    outputs="text",
    title="Premier League Match Outcome Predictor"
).launch()