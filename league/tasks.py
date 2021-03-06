from celery.decorators import task
from celery.utils.log import get_task_logger
from auction.models import Original_Team, Player
from .cricapi import league_teams, get_scorecard, get_matches


logger = get_task_logger(__name__)


@task(name='get_league_teams')
def get_league_teams():
    try:
        teams_fetched = league_teams()
        for t in teams_fetched['seriesTeams']['teams']:
            new_row = Original_Team()
            new_row.id = t['id']
            new_row.name = t['name']
            new_row.shortName = t['shortName']
            new_row.save()
        logger.info('successfully updated original teams')
    except Exception as e:
        logger.info('Couldn\'t update league teams:' + " " + str(e))


@task(name='update_player_stats')
def update_player_stats():
    try:
        matchList = get_matches()
        # reset all player stats
        for p in Player.objects.all():
            p.stats.runs = 0
            p.stats.wickets = 0
            p.stats.save()

        # for every finished match, update player stats
        for m in matchList:
            currentScorecard = get_scorecard(str(m))
            for inn in currentScorecard['fullScorecard']['innings']:
                for batsman in inn['batsmen']:
                    currentPlayer = Player.objects.get_or_create(
                        id=batsman['id'])
                    batsman_name = batsman['name']
                    currentPlayer[0].name = batsman_name
                    currentPlayer[0].original_team = Original_Team.objects.get_or_create(
                        id=inn['team']['id'])[0]
                    currentPlayer[0].save()
                    if(batsman['runs'] == ''):
                        batsman['runs'] = '0'
                    currentPlayer[0].stats.runs += int(batsman['runs'])
                    currentPlayer[0].stats.save()
                for bowler in inn['bowlers']:
                    currentPlayer = Player.objects.get_or_create(
                        id=bowler['id'])
                    bowler_name = bowler['name']
                    currentPlayer[0].name = bowler_name
                    if(inn == currentScorecard['fullScorecard']['innings'][0]):
                        bowling_team = currentScorecard['fullScorecard']['innings'][1]['team']['id']
                    else:
                        bowling_team = currentScorecard['fullScorecard']['innings'][0]['team']['id']
                    currentPlayer[0].original_team = Original_Team.objects.get_or_create(
                        id=bowling_team)[0]
                    currentPlayer[0].save()
                    if(bowler['wickets'] == ''):
                        bowler['wickets'] = '0'
                    currentPlayer[0].stats.wickets += int(
                        bowler['wickets'])
                    currentPlayer[0].stats.save()
        logger.info("Updated Player Stats Successfully")
    except Exception as e:
        logger.info("Couldn't get matches:" + " " + str(e))
