import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import numpy as np
import joblib

data = pd.read_csv('data/Final_Data.csv') #Reads the CSV file with the match information

# 1. FEATURE ENGINEERING - Add more predictive features
def add_engineered_features(df):
    # Goal difference features
    df['team_1_goal_diff'] = df.get('team_1_Average_goals_scored_last10', 0) - df.get('team_1_Average_goals_conceded_last10', 0)
    df['team_2_goal_diff'] = df.get('team_2_Average_goals_scored_last10', 0) - df.get('team_2_Average_goals_conceded_last10', 0)
    
    # Form comparison
    df['goal_diff_comparison'] = df['team_1_goal_diff'] - df['team_2_goal_diff']
    
    # Odds-based features (bookmaker predictions)
    if 'team_1_Average_B365_odds_last10' in df.columns and 'team_2_Average_B365_odds_last10' in df.columns:
        df['odds_ratio'] = df['team_1_Average_B365_odds_last10'] / df['team_2_Average_B365_odds_last10']
        df['draw_likelihood'] = 1 / df.get('team_1_Average_B365_draw_odds_last10', 3.0)  # Higher when draw odds are lower
    
    # Attacking vs Defensive strength
    if 'team_1_Average_shots_last10' in df.columns:
        df['team_1_attack_strength'] = (df.get('team_1_Average_shots_last10', 0) + df.get('team_1_Average_goals_scored_last10', 0)) / 2
        df['team_2_attack_strength'] = (df.get('team_2_Average_shots_last10', 0) + df.get('team_2_Average_goals_scored_last10', 0)) / 2
        df['attack_balance'] = abs(df['team_1_attack_strength'] - df['team_2_attack_strength'])
    
    return df

# Apply feature engineering
data = add_engineered_features(data)

X = data.drop(['FTR', 'date', 'match_id'], axis=1)

# 2. HANDLE CLASS IMBALANCE - Check distribution
print("Class distribution:")
print(data['FTR'].value_counts())
print("\nClass proportions:")
print(data['FTR'].value_counts(normalize=True))

# Label encode teams
le_team_x = LabelEncoder()
le_team_y = LabelEncoder()

X['team_x_encoded'] = le_team_x.fit_transform(X['team_x'])
X['team_y_encoded'] = le_team_y.fit_transform(X['team_y'])

# Drop the original team columns
X = X.drop(['team_x', 'team_y'], axis=1)

# Save the encoders for later use in predictions
joblib.dump(le_team_x, 'team_x_encoder.joblib')
joblib.dump(le_team_y, 'team_y_encoder.joblib')

#X.to_csv('data/Final_Data_Encoded.csv', index=False)

Y = data['FTR']

Y = Y - 1

# 3. STRATIFIED SPLIT to maintain class distribution
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

# 4. COMPUTE CLASS WEIGHTS for imbalanced data
class_weights = compute_class_weight('balanced', classes=np.unique(Y), y=Y)
class_weight_dict = {i: class_weights[i-1] for i in np.unique(Y)}
print(f"Class weights: {class_weight_dict}")

# 5. TRY MULTIPLE MODELS WITH DIFFERENT APPROACHES

# Model 1: Random Forest with class weights
rf_model = RandomForestClassifier(
    n_estimators=500,  # Increased trees
    random_state=42,
    class_weight='balanced',  # Handle imbalanced classes
    max_depth=15,  # Prevent overfitting
    min_samples_split=10,
    min_samples_leaf=5,
    bootstrap=True
)

# Model 2: XGBoost (often better for tabular data)
xgb_model = xgb.XGBClassifier(
    n_estimators=500,
    random_state=42,
    learning_rate=0.05,  # Lower learning rate
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,  # L1 regularization
    reg_lambda=1.0,  # L2 regularization
    scale_pos_weight=class_weights[1]/class_weights[0],  # Handle imbalance
    objective='multi:softprob',
    eval_metric='mlogloss'
)

# Model 3: Logistic Regression with class weights
lr_model = LogisticRegression(
    random_state=42,
    class_weight='balanced',  # Handle imbalanced classes
    max_iter=1000,  # Increase iterations for convergence
    solver='lbfgs',  # Good solver for multiclass problems
    multi_class='multinomial'  # Use multinomial for 3-class problem
)
# Train and evaluate both models
models = {'RandomForest': rf_model, 'LogisticRegression': lr_model,'XGBoost': xgb_model}
best_model = None
best_accuracy = 0

for name, model in models.items():
    print(f"\n--- Training {name} ---")
    model.fit(X_train, Y_train)
    
    Y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    
    print(f"{name} accuracy: {accuracy:.3f}")
    print(f"{name} Classification Report:")
    print(classification_report(Y_test, Y_pred, target_names=['HomeWin', 'Draw', 'AwayWin']))
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# 6. FEATURE IMPORTANCE ANALYSIS
print(f"\n--- Best Model: {best_model_name} with accuracy {best_accuracy:.3f} ---")

if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 15 Most Important Features:")
    print(feature_importance.head(15))

# 7. ADVANCED: Try ensemble with probability threshold adjustment
def predict_with_threshold(model, X_test, draw_threshold=0.25):
    """Adjust draw prediction threshold"""
    probabilities = model.predict_proba(X_test)
    predictions = []
    
    for prob in probabilities:
        if prob[1] > draw_threshold:  # If draw probability > threshold (index 1 = draw in 0-indexed)
            predictions.append(1)  # Predict draw (0-indexed)
        else:
            predictions.append(np.argmax(prob))  # Predict class with highest prob (0-indexed)
    
    return np.array(predictions)

# Test different thresholds for draw prediction
print("\n--- Testing Draw Threshold Optimization ---")
for threshold in [0.2, 0.25, 0.3, 0.35]:
    Y_pred_thresh = predict_with_threshold(best_model, X_test, threshold)
    accuracy_thresh = accuracy_score(Y_test, Y_pred_thresh)
    print(f"Threshold {threshold}: Accuracy {accuracy_thresh:.3f}")
    
    # Check draw recall specifically - now using 0-indexed labels
    from sklearn.metrics import recall_score
    draw_recall = recall_score(Y_test, Y_pred_thresh, labels=[0, 1, 2], average=None)[1]  # Index 1 for draw
    print(f"  Draw recall: {draw_recall:.3f}")

# Update classification report to use 0-indexed labels
for name, model in models.items():
    print(f"\n--- Training {name} ---")
    model.fit(X_train, Y_train)
    
    Y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    
    print(f"{name} accuracy: {accuracy:.3f}")
    print(f"{name} Classification Report:")
    print(classification_report(Y_test, Y_pred, target_names=['HomeWin', 'Draw', 'AwayWin']))
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# Save the best model
joblib.dump(best_model, f'best_model_{best_model_name.lower()}.joblib')
joblib.dump(X.columns, 'model_columns.joblib')