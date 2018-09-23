'''
This script uses the public nhl api to get schedule information
and print details of any games in the specified date range that
are within the specified time range
'''

import json
import requests
from datetime import datetime,date,timedelta,timezone,time

# specify date range
week_range = 2    # end date is week_range weeks after start
date_filter = {
    'start' : date.today().isoformat(),
    'end'   : (date.today() + timedelta(weeks=week_range)).isoformat()
}

# request json data
url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}".format(
    date_filter['start'],
    date_filter['end']
)
response = requests.get(url)
if response.status_code == 200:
    print('data retreived')
else:
    print('reponse code = {}'.format(response.status_code))
    raise Exception('Error, data was not successfully accessed')

# specify time range
time_filter = {
    'start' :   time(hour=7),
    'end'   :   time(hour=23)
}

data_head = json.loads(response.text) # convert json data into dict

# print limits
print('{} - {} ({} - {})'.format(
    date_filter['start'],
    date_filter['end'],
    time_filter['start'],
    time_filter['end']
))

# process json data to select games with start times within filter limits
date_list = data_head['dates']
watchable_dates = [] # accumulate any dates with watchable games in this list
for date in date_list:

    watchable_date = {
        'date'    : date['date'],
        'games'   : []
    }

    for game in date['games']:
        game_datetime = datetime.strptime(game['gameDate'],'%Y-%m-%dT%H:%M:%SZ')

        #convert to local time
        game_datetime = game_datetime.replace(tzinfo = timezone.utc).astimezone()

        if time_filter['start'] < game_datetime.time() < time_filter['end']:
            # generate list entry
            watchable_game = {
                'time' :   game_datetime.strftime('%H:%M'),
                'home_team'   :   game['teams']['home']['team']['name'],
                'away_team'   :   game['teams']['away']['team']['name']
            }
            watchable_date['games'].append(watchable_game)

    if len(watchable_date['games']) > 0:
        watchable_dates.append(watchable_date) # only append date if watchable game exists

# print results
for date in watchable_dates:
    print('\t{}'.format(date['date'],len(date['games'])))
    for game in date['games']:
        print('\t\t{} @ {} - {}'.format(game['home_team'],game['away_team'],game['time']))

