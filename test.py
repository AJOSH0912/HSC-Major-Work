import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import xgboost as xgb
from imblearn.over_sampling import RandomOverSampler

data = pd.read_csv('Final_match_history_rolling_averages.csv')
# Drop rows with missing target
data = data.dropna(subset=['FTR'])

# Separate features and target
X = data.drop(['FTR', 'date'], axis=1)

# One-hot encode team columns
X = pd.get_dummies(X, columns=['home_team', 'away_team'])

Y = data['FTR'].map({'H': 0, 'D': 1, 'A': 2})


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Oversample the minority classes in the training set
ros = RandomOverSampler(random_state=42)
X_resampled, Y_resampled = ros.fit_resample(X_train, Y_train)

# Train XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
model.fit(X_resampled, Y_resampled)

# Evaluate
Y_pred = model.predict(X_test)
print(f"Model accuracy: {accuracy_score(Y_test, Y_pred):.2f}")
print(classification_report(Y_test, Y_pred, target_names=['HomeWin', 'Draw', 'AwayWin']))