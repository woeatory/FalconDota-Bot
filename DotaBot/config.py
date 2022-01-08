import stratz_requests

BOT_TOKEN = 'token'  #token for telegram bot API
STRATZ_TOKEN = 'token' #token for STRATZ API
headers = {'Authorization': 'Bearer ' + STRATZ_TOKEN}

all_heroes = stratz_requests.get_all_heroes()
