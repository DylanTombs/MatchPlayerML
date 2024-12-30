import pandas as pd


def process_matches():
    matches = pd.read_csv("matches.csv", index_col=0)

    matches = matches[["Date","Time","Venue","Result","GF","GA","Opponent","xG","xGA","Poss"
                      ,"Referee","Sh","SoT","Dist","FK","PK","PKatt","Team"]]

    matches["Team"] = matches["Team"].astype("category").cat.codes
    matches["Opponent"] = matches["Opponent"].astype("category").cat.codes
    matches["Date"] = pd.to_datetime(matches["Date"])
    matches["Result"] = (matches["Result"] == "W").astype("int")
    matches["Venue"] = matches["Venue"].astype("category").cat.codes
    matches["Opp"] = matches["Opponent"].astype("category").cat.codes
    matches["Hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype("int")
    matches["Day"] = matches["Date"].dt.dayofweek
    matches["Referee"] = matches["Referee"].astype("category").cat.codes

    cols = ["GF","GA","xG","xGA","Poss","Sh","SoT","Dist","FK","PK","PKatt"]
    new_cols = [f"{c}_rolling" for c in cols]

    matches = matches.groupby("Team").apply(lambda x: rolling_averages(x, cols, new_cols))
    matches = matches.droplevel('Team')
    matches.index = range(matches.shape[0])

    matches.to_csv("matches_2024_cleaned.csv")

player_Positions = {"GK":0,
                    "CB":1,
                    "LB":1,
                    "RB":1,
                    "WB":1,
                    "DM":2,
                    "CM":2,
                    "AM":2,
                    "LM":2,
                    "RM":2,
                    "LW":2,
                    "RW":2,
                    "FW":3
}

def process_players():
    players = pd.read_csv("players_reports.csv", index_col=0)

    columns = ["Player", "Pos","Min","Gls","Ast","PK","PKatt","Sh","SoT",
               "CrdY","CrdR","Touches","Tkl","Int","Blocks","xG","npxG","xAG"
               ,"SCA","GCA","Cmp","Att","Cmp%","PrgP","Carries","PrgC","Date","Team"]
    players = players[columns]

    players["Pos"] = players["Pos"].str.split(",").str[0] 
    players["Pos"] = players["Pos"].map(player_Positions).fillna(-1)
    players = players[players["Pos"] != -1]

    players["Player_Code"] = players["Player"].astype("category").cat.codes
    players["Date"] = pd.to_datetime(players["Date"])
    players["Team"] = players["Team"].astype("category").cat.codes


    cols = ["Min","Gls","Ast","PK","PKatt","Sh","SoT",
            "CrdY","CrdR","Touches","Tkl","Int","Blocks","xG","npxG","xAG",
            "SCA","GCA","Cmp","Att","Cmp%","PrgP","Carries","PrgC"]
    new_cols = [f"{c}_rolling" for c in cols]

    
    players = players.groupby("Player").apply(lambda x: rolling_averages(x, cols, new_cols))
    players = players.droplevel('Player')
    players.index = range(players.shape[0])

    players.to_csv("players_2024_cleaned.csv")

def rolling_averages(group, cols, new_cols):
    group = group.sort_values("Date")
    rolling_stats = group[cols].rolling(3, closed='left', min_periods=1).mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

process_matches()
process_players()