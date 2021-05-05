import requests


def get_scorecard(match_id):
    url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com/scorecards.php"

    querystring = {"matchid": match_id, "seriesid": "2780"}

    headers = {
        'x-rapidapi-key': "09f1c7ab99msh7a788e0948da842p1ed1dcjsnbd7378bdcb4d",
        'x-rapidapi-host': "dev132-cricket-live-scores-v1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring).json()

    # for inn in response['fullScorecard']['innings']:
    #     for batsman in inn['batsmen']:
    #         name = batsman['name']
    #         # currentPlayer.original_team = Original_Team.objects.get_or_create(
    #         #     id=inn['team']['id'])
    #         print(name)
    return response


def get_matches():
    url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com/matchseries.php"

    querystring = {"seriesid": "2780", "status": "COMPLETED"}

    headers = {
        'x-rapidapi-key': "09f1c7ab99msh7a788e0948da842p1ed1dcjsnbd7378bdcb4d",
        'x-rapidapi-host': "dev132-cricket-live-scores-v1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring).json()

    match_list = []
    mList = response['matchList']['matches']
    for r in mList:
        if r['status'] == 'COMPLETED':
            match_list.append(r['id'])

    # for m in match_list:
    #     print(str(m))
    return match_list


def league_teams():

    url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com/seriesteams.php"

    querystring = {"seriesid": "2780"}

    headers = {
        'x-rapidapi-key': "09f1c7ab99msh7a788e0948da842p1ed1dcjsnbd7378bdcb4d",
        'x-rapidapi-host': "dev132-cricket-live-scores-v1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    return response.json()


get_scorecard(50809)
