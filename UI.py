import gradio as gr
import pandas as pd
import joblib

# Load model and metadata
model = joblib.load('rf_model.joblib')
model_columns = joblib.load('model_columns.joblib')
teams = joblib.load('teams.joblib')


def predict(home_team, away_team):
    print("testing")


gr.Interface(
    fn=predict,
    inputs=[
        gr.Dropdown(teams, label="Home Team"),
        gr.Dropdown(teams, label="Away Team")
    ],
    outputs="text",
    title="Premier League Match Outcome Predictor"
).launch()