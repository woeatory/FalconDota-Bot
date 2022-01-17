import pandas as pd
import requests
import config


def get_all_heroes():
    df = pd.DataFrame(columns=['heroName'])
    heroID = list()
    url = 'https://api.stratz.com/api/v1/Hero'
    response = requests.get(url=url, headers=config.headers).json()

    for index in range(1, len(response) + 1):
        try:
            heroID.append(response[str(index)]['id'])
            heroName = response[str(index)]['displayName']
            df = df.append({'heroName': heroName}, ignore_index=True)
        except:
            continue
    df.index = heroID
    return df


def find_index(dataframe, search):
    return dataframe[dataframe['heroName'] == search].index.values


def request_hero_info(heroID):
    url = 'https://api.stratz.com/graphql'
    query = '''{
        heroStats {
            winWeek(heroIds: [%d], bracketIds: [IMMORTAL], gameModeIds:[ALL_PICK]) {
                winCount
                matchCount
                week
            }
        }
        }''' % heroID
    response = requests.get(url=url, params={'query': query}, headers=config.headers).json()
    return response


def procces_hero_info(response):
    win_count = 0
    match_count = 0
    for data in response['data']['heroStats']['winWeek']:
        win_count = win_count + data['winCount']
        match_count = match_count + data['matchCount']
    winRate = round(win_count * 100 / match_count, 3)
    return winRate


def find_hero_info(heroName):
    idx = find_index(config.all_heroes, heroName)
    response = request_hero_info(idx)
    winRate = procces_hero_info(response)

    return winRate


def get_logs(matchID):
    pass



