# MatchPlayerML

This project used ML to predict the results of matches, players, and their goals and assists for each game in Python, using data scraping, data processing, and Sklearn random forest machine learning models to create predictions. 

## Approach:
I took inspiration from [1] whose implementation made me consider there me more factors to match predictions and then also take the modelling to players' performances. Using BeautifulSoup I was able to effectively scrape data from the tables on the statistics website [2] and to process them into data frames using pandas. This was done for each team in the premier league for all their match statistics, and then further done for each player's statistics for each respective match.

This CSV data was then processed to remove unnecessary data columns like player nationality and attendance since such statistics have no effect on player performance or are not known before the match. For the matches model, a random forest classifier is used to determine whether a game is won or lost ( as draws are classified into loses in this model) hence making a classifier more appropriate in the case of classifying the result. For the player model, a random forest regressor is used since multiple values are being predicted and are not classifyable values as goals and assists can range in values. The data was then fit to these respective models and a train and test ratio was found to be most effective. 

##Model Performance Results:
Accuracy: 0.648936170212766

Precision: 0.6288815411155837

Recall: 0.648936170212766

F1 Score: 0.6208606622940329

## Evaluation and Future:
I believe the predictions could be more accurate with predictions using training over multiple seasons which would take in a lot larger range of data, allowing the model to be trained more. This approach was considered however, with the volume of requests and data scraping on one site it seemed ethical to not use such data. Additionally, draws could be predicted for the match model as with further predictions for player statistics like fouls etc.

For further developments, the two models should be able to use each other and in a way bounce off each other as a way to predict how well a player is going to do based on how well the opposition has been doing and their respective player's forms. Conversely, how well the player's forms influence the prediction of the match. 

## Credits:

- [1] https://youtu.be/Nt7WJa2iu0s?si=YPGtKY_-oWDOTcbe, https://youtu.be/0irmDBWLrco?si=Lax5T2ktqBU6LDGL
- [2] https://fbref.com/en/comps/9/Premier-League-Stats
