import json
import requests
import re #regex

def get_json_data(uri, offline):
    """
    retrieve json data for uri
    either from offline file, or online url
    """
    #TODO detect offline from uri
    if offline:
        response = open(uri, 'r')
        return json.load(response)
    else:
        response = requests.get(uri,headers = {'User-agent': 'nhlbot'})

        if response.status_code == 200:
            print('data retreived')
        else:
            print('reponse code = {}'.format(response.status_code))
            raise Exception('Error, data was not successfully accessed')

        return json.loads(response.text)

def get_thread_link(offline=False):
    """
    retrieve links for active game threads
    """
    if offline:
        thread_uri = 'nhlstreams.json'
    else:
        thread_uri = "https://reddit.com/r/nhlstreams/.json"

    data_head = get_json_data(thread_uri, offline)

    thread_list = []

    # assemble threads with "Game Thread" flair into list
    for thread_raw in data_head['data']['children']:
        if thread_raw['data']['link_flair_text'] == "Game Thread":
            # print(thread_raw['data']['title'])
            thread = {
                'title' : thread_raw['data']['title'].replace('Game Thread: ',''),
                'url'   : thread_raw['data']['url']
            }
            thread_list.append(thread)
    # print thread options
    for thread_idx,thread in enumerate(thread_list):
        print('{} - {}'.format(thread_idx,thread['title']))

    # get selection
    thread_selection = int(input())
    print('Selected: {}'.format(thread['title']))

    # return .json url
    return thread['url'] + '.json'

def get_stream_link(stream_uri, offline=False):
    """
    retreive links for streams
    """
    if offline:
        stream_uri = 'game.json'
    else:
        pass # use existing stream_uri
    data_head = get_json_data(stream_uri, offline)
    # with open('game.json', 'r') as response:
        # data_head = json.load(response) # convert json data into dict

    comment_list =[]
    link_list = []

    pattern = re.compile('\[.*?\]\(http.+?\)')

    # pull all links and link text from comments
    for comment_raw in data_head[1]['data']['children'][1:]:
        linkMatchIter = pattern.finditer(comment_raw['data']['body'])
        for linkMatch in linkMatchIter:
            link_list.append(linkMatch.group())

    print('\n'.join(link_list[:10]))

offline=False
stream_uri = get_thread_link(offline)
get_stream_link(stream_uri,offline)
