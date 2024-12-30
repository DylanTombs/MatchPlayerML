import requests 
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"


years = list([2024])
date_pattern = r"(\w+)-(\d+)-(\d+)"

all_matches = []
all_player_reports = []

map_name = {"Brighton and Hove Albion": "Brighton",
               "Manchester United": "Manchester Utd",
               "Newcastle United": "Newcastle Utd", 
               "Tottenham Hotspur": "Tottenham", 
               "West Ham United": "West Ham", 
               "Wolverhampton Wanderers": "Wolves",
               "Nottingham Forest": "Nott'ham Forest"} 

for year in years:
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text, features="lxml")                        
    standings_table = soup.select('table.stats_table')[0]      # css selector 

    links = [l.get("href") for l in standings_table.find_all('a')]  # get team urls from css selector
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]            # get absolute links
    
    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"
    
    for team_url in team_urls:
        try:
            team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
            name = map_name.get(team_name,team_name)
            print(name)
            team_data = requests.get(team_url)
            time.sleep(10)
            matches = pd.read_html(team_data.text, match="Scores & Fixtures ")[0]

            team_soup = BeautifulSoup(team_data.text, features="lxml")
            matches_links = team_soup.select('table.stats_table')[1]

            report_links = [l.get("href") for l in matches_links.find_all('a')]
            report_links = list(set([l for l in report_links if '/matches/' in l])) 
            report_links = [l for l in report_links if 'Premier-League' in l]
  
            report_urls = [f"https://fbref.com{l}" for l in report_links]        

            for report_url in report_urls:
                report_data = requests.get(report_url)
                time.sleep(5)
                report = pd.read_html(report_data.text, match=f"{name} Player Stats Table")[0]
                report.columns = report.columns.droplevel()

                date = re.search(date_pattern, report_url)
                month_name, day, year = date.groups()
                month_number = datetime.strptime(month_name, "%B").month
                date = f"{year}-{month_number}-{day}"

                report["Date"] = date
                report["Team"] = team_name

                all_player_reports.append(report)

            links = [l.get("href") for l in team_soup.find_all('a')]
            links = [l for l in links if l and 'all_comps/shooting/' in l]
            team_data = requests.get(f"https://fbref.com{links[0]}")
            shooting = pd.read_html(team_data.text, match="Shooting ")[0]
            shooting.columns = shooting.columns.droplevel()
            team_info = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")

        
            team_info = team_info[team_info["Comp"] == "Premier League"]
        
            team_info["Team"] = team_name

            all_matches.append(team_info)
            print("complete")

            time.sleep(15)
        except ValueError:
            print(ValueError)
            continue



match_df = pd.concat(all_matches, ignore_index=True)
match_df.to_csv("matches.csv")
player_report_df = pd.concat(all_player_reports, ignore_index=True)
player_report_df.to_csv("players_reports.csv")