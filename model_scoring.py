import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, accuracy_score
import joblib
import helper as hp  # Importing the helper module for encryption and decryption functions

data=hp.decrypt_csv_file('data/Final_Data.csv.encrypted', 'app.key') # Decrypts the CSV file containing the match data


X = data.drop(['FTR', 'date' , 'match_id'], axis=1) #Features are plotted on the X axis

X = pd.get_dummies(X, columns=['team_x', 'team_y']) # One-hot encodes the team columns so that the model can understand them

Y = data['FTR']


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)  # Splits the data into training and testing sets, with 30% of the data used for testing
model = RandomForestClassifier(n_estimators=300, random_state=42) # Initialises the Random Forest model with 100 trees
model.fit(X_train, Y_train) # Fits the model to the training data


Y_pred = model.predict(X_test) # Makes predictions on the test data
accuracy = accuracy_score(Y_test, Y_pred) # Calculates the accuracy of the model
print(f"Model accuracy: {accuracy:.2f}") # Prints the accuracy of the model
print(classification_report(Y_test, Y_pred, target_names=['HomeWin', 'Draw', 'AwayWin'])) # Prints the classification report, which includes precision, recall, and F1-score for each class

joblib.dump(model, 'joblib/rf_model.joblib') # Saves the trained model to a file for use in the UI so that the model does not have to be retrained every time the UI is run
joblib.dump(X.columns, 'joblib/model_columns.joblib') 
joblib.dump(sorted(set(data['team_x']).union(set(data['team_y']))), 'joblib/teams.joblib')