'''
This script uses the public nhl api to get schedule information
and print details of any games in the specified date range that
are within the specified time range
'''

import json
import requests
from datetime import datetime,date,timedelta,timezone,time

def generate_filtered_game_list_entry(game, game_datetime_local):
    # generate list entry
    filtered_game = {
        'time' :   game_datetime_local.strftime('%H:%M'),
        'home_team'   :   game['teams']['home']['team']['name'],
        'away_team'   :   game['teams']['away']['team']['name']
    }
    return filtered_game

# specify filter values and generate request modifier
week_range = 2    # end date is week_range weeks after start
date_filter = {
    'start' : date.today().isoformat(),
    'end'   : (date.today() + timedelta(weeks=week_range)).isoformat()
}
request_modifier = "startDate={}&endDate={}".format(
    date_filter['start'],
    date_filter['end']
)

selection = input('(r)angers, (e)arly or (a)ll?\n')
if selection == 'r':
    print('rangers selected')
    rangers_id = '3'
    request_modifier = "teamId={}&".format(rangers_id) + request_modifier
elif selection == 'e':
    print('early selected')
    time_filter = {
        'start' :   time(hour=7),
        'end'   :   time(hour=23)
    }
elif selection == 'a':
    print('all selected')
else:
    print('selection not recognised')

# request json data
url = "https://statsapi.web.nhl.com/api/v1/schedule?" + request_modifier
response = requests.get(url)
if response.status_code == 200:
    print('data retreived')
else:
    print('reponse code = {}'.format(response.status_code))
    raise Exception('Error, data was not successfully accessed')

data_head = json.loads(response.text) # convert json data into dict

# print limits
print('{} - {}'.format(
    date_filter['start'],
    date_filter['end']
))

# process json data to select games with start times within filter limits
date_list = data_head['dates']
filtered_dates = [] # accumulate any dates with filtered games in this list
for date in date_list:

    filtered_date = {
        'date'    : date['date'],
        'games'   : []
    }

    for game in date['games']:
        game_datetime = datetime.strptime(game['gameDate'],'%Y-%m-%dT%H:%M:%SZ')

        #convert to local time
        game_datetime_local = game_datetime.replace(tzinfo = timezone.utc).astimezone()

        if selection == 'e':
            if time_filter['start'] < game_datetime_local.time() < time_filter['end']:
                filtered_date['games'].append(generate_filtered_game_list_entry(game, game_datetime_local))
        else:
            filtered_date['games'].append(generate_filtered_game_list_entry(game, game_datetime_local))

    if len(filtered_date['games']) > 0:
        filtered_dates.append(filtered_date) # only append date if filtered game exists

# print results
for date in filtered_dates:
    print('\t{}'.format(date['date'],len(date['games'])))
    for game in date['games']:
        print('\t\t{} @ {} - {}'.format(game['home_team'],game['away_team'],game['time']))
