# nhl_upcoming_games
python script to display upcoming nhl games with good faceoff time

This python script uses the [public NHL API](https://statsapi.web.nhl.com/api/v1/schedule) to get schedule information about upcoming nhl games. By default, the script pulls all games occurring in the next two weeks. The script then collects information for games that start during reasonable hours in the user's timezone. By default, this is defined as 07:00 < reasonable < 23:00. Finally, the script prints the information for each of the qualifying games, including date, faceoff time, home team and away team.
