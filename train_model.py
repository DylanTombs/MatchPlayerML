from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import pickle

matches = pd.read_csv("matches_cleaned.csv", index_col=0)
players = pd.read_csv("players_cleaned.csv", index_col=0)

date_testing = "2024-12-01"

match_rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
players_rf = RandomForestRegressor(n_estimators=50, min_samples_split=10, random_state=1)

match_predictors = ["Team","Venue", "Opponent", "Day","Referee"]
cols = ["GF","GA","xG","xGA","Poss","Sh","SoT","Dist","FK","PK","PKatt"]
match_predictors = match_predictors + [f"{c}_rolling" for c in cols]

cols = ["Min","Gls","Ast","PK","PKatt","Sh","SoT","xG","npxG","xAG"]
            
player_predictors = [f"{c}_rolling" for c in cols]

match_targets = ["Result"]
player_targets = ["Gls","Ast"]

def players_make_predictions(data, player_predictions):
    players_rf.predict(data [player_predictions])

def train_matches_model():
    train = matches[matches["Date"] < date_testing] 
    test  = matches[matches["Date"] > date_testing]

    match_rf.fit(train[match_predictors], train[match_targets])
    predictions = match_rf.predict(test[match_predictors])

    actual = test[match_targets]

    print("Accuracy:", accuracy_score(actual, predictions))
    print("Precision:", precision_score(actual, predictions, average='weighted'))
    print("Recall:", recall_score(actual, predictions, average='weighted'))
    print("F1 Score:", f1_score(actual, predictions, average='weighted'))

def train_players_model():
    train = players[players["Date"] < date_testing] 
    test  = players[players["Date"] > date_testing]
    
    players_rf.fit(train[player_predictors], train[player_targets])
    predictions = players_rf.predict(test[player_predictors])

    predictions = np.round(predictions)
    actual = test[player_targets]

    mse = mean_squared_error(actual, predictions)
    r2 = r2_score(actual, predictions)

    print("Mean Squared Error:", mse)
    print("R-squared:", r2)

def store_model(model, model_name):
    with open(f"{model_name}.pkl", "wb") as file:
        pickle.dump(model, file)

def open_model(model_name):
    with open(f"{model_name}.pkl", "rb") as file:
        return pickle.load(file)
    


