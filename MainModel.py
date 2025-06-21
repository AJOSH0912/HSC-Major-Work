import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, accuracy_score
import joblib

data = pd.read_csv('Final_match_history_rolling_averages.csv')
# Drop rows with missing target
data = data.dropna(subset=['FTR'])

# Separate features and target
X = data.drop(['FTR', 'date'], axis=1)

# One-hot encode team columns
X = pd.get_dummies(X, columns=['home_team', 'away_team'])

data['FTR'] = data['FTR'].astype(str).str.strip().str.upper()
print(data['FTR'].unique())  # Debug: see what values you have
Y = data['FTR'].map({'H': 0, 'D': 1, 'A': 2})


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Model accuracy: {accuracy:.2f}")
print(classification_report(Y_test, Y_pred, target_names=['HomeWin', 'Draw', 'AwayWin']))

joblib.dump(model, 'rf_model.joblib')
joblib.dump(X.columns, 'model_columns.joblib')
joblib.dump(sorted(set(data['home_team']).union(set(data['away_team']))), 'teams.joblib')