import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, accuracy_score
import joblib

data = pd.read_csv('data/merged_data2.csv') #Reads the CSV file with the match information



X = data.drop(['FTR', 'date' , 'referee', 'HTR', 'FTHG', 'FTAG', 'HTHG', 'HTAG'], axis=1) #Features are plotted on the X axis

X = pd.get_dummies(X, columns=['home_team', 'away_team']) # One-hot encodes the team columns so that the model can understand them

data['FTR'] = data['FTR'].astype(str).str.strip().str.upper() # Ensures that the target variable is in the correct format
Y = data['FTR'].map({'H': 0, 'D': 1, 'A': 2}) # Maps the target variable to numerical values: Home Win = 0, Draw = 1, Away Win = 2


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)  # Splits the data into training and testing sets, with 30% of the data used for testing
model = RandomForestClassifier(n_estimators=200, random_state=42) # Initialises the Random Forest model with 100 trees
model.fit(X_train, Y_train) # Fits the model to the training data


Y_pred = model.predict(X_test) # Makes predictions on the test data
accuracy = accuracy_score(Y_test, Y_pred) # Calculates the accuracy of the model
print(f"Model accuracy: {accuracy:.2f}") # Prints the accuracy of the model
print(classification_report(Y_test, Y_pred, target_names=['HomeWin', 'Draw', 'AwayWin'])) # Prints the classification report, which includes precision, recall, and F1-score for each class

joblib.dump(model, 'rf_model.joblib') # Saves the trained model to a file for use in the UI so that the model does not have to be retrained every time the UI is run
joblib.dump(X.columns, 'model_columns.joblib') 
joblib.dump(sorted(set(data['home_team']).union(set(data['away_team']))), 'teams.joblib')