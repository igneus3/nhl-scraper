from enum import IntEnum

class PlayNotFoundError(Exception):
    pass

class PlayType(IntEnum):
    FACEOFF = 502
    HIT = 503
    GIVEAWAY = 504
    GOAL = 505
    SHOT_ON_GOAL = 506
    MISSED_SHOT = 507
    BLOCKED_SHOT = 508
    PENALTY = 509
    STOPPAGE = 516
    PERIOD_START = 520
    PERIOD_END = 521
    SHOOTOUT_COMPLETE = 523
    GAME_END = 524
    TAKEAWAY = 525
    DELAYED_PENALTY = 535
    FAILED_SHOT_ATTEMPT = 537

def get_playerId_maybe(play, key):
    result = None

    if 'details' in play and key in play['details']:
        result = play['details'][key]

    return result

def update_player_maybe(playerId, players, update):
    if playerId is not None:
        players[playerId].call(update)

def process_play(play, players):
    match play['typeCode']:

        case PlayType.FACEOFF:
            winner = get_playerId_maybe(play, 'winningPlayerId')
            update_player_maybe(winner, players, 'add_faceoff_win')

            loser = get_playerId_maybe(play, 'losingPlayerId')
            update_player_maybe(loser, players, 'add_faceoff_loss')

        case PlayType.SHOT_ON_GOAL:
            shooter = get_playerId_maybe(play, 'shootingPlayerId')
            update_player_maybe(shooter, players, 'add_shot_on_goal')

            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats

        case PlayType.TAKEAWAY:
            taker = get_playerId_maybe(play, 'playerId')
            update_player_maybe(taker, players, 'add_takeaway')

        case PlayType.PENALTY:
            committer = get_playerId_maybe(play, 'committedByPlayerId') 
            update_player_maybe(committer, players, 'add_penalty_committed')

            drawer = get_playerId_maybe(play, 'drawnByPlayerId') 
            update_player_maybe(drawer, players, 'add_penalty_drawn')

            server = get_playerId_maybe(play, 'servedByPlayerId') 
            update_player_maybe(server, players, 'add_penalty_served')

        case PlayType.MISSED_SHOT:
            shooter = get_playerId_maybe(play, 'shootingPlayerId')
            update_player_maybe(shooter, players, 'add_missed_shot')

            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats

        case PlayType.BLOCKED_SHOT:
            shooter = get_playerId_maybe(play, 'shootingPlayerId')
            update_player_maybe(shooter, players, 'add_shot')

            blocker = get_playerId_maybe(play, 'blockingPlayerId')
            update_player_maybe(blocker, players, 'add_blocked_shot')

        case PlayType.HIT:
            hitter = get_playerId_maybe(play, 'hittingPlayerId')
            update_player_maybe(hitter, players, 'add_hit_given')

            hittee = get_playerId_maybe(play, 'hitteePlayerId')
            update_player_maybe(hittee, players, 'add_hit_received')

        case PlayType.GOAL:
            scorer = get_playerId_maybe(play, 'scoringPlayerId')
            update_player_maybe(scorer, players, 'add_goal')

            assist1 = get_playerId_maybe(play, 'assist1PlayerId')
            update_player_maybe(assist1, players, 'add_primary_assist')

            assist2 = get_playerId_maybe(play, 'assist2PlayerId')
            update_player_maybe(assist1, players, 'add_secondary_assist')

            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats
            # if goalie is not None:

        case PlayType.GIVEAWAY:
            giver = get_playerId_maybe(play, 'playerId')
            update_player_maybe(giver, players, 'add_giveaway')

        case PlayType.FAILED_SHOT_ATTEMPT:
            shooter = get_playerId_maybe(play, 'shootingPlayerId')
            update_player_maybe(shooter, players, 'add_so_failed_shot')

            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats

        case PlayType.STOPPAGE | \
             PlayType.PERIOD_START | \
             PlayType.PERIOD_END | \
             PlayType.SHOOTOUT_COMPLETE | \
             PlayType.GAME_END | \
             PlayType.DELAYED_PENALTY: 
            # Skipping plays I'm not interested in currently
            pass

        case _:
            # Raising error for any play types I have not discovered yet
            raise PlayNotFoundError()


def process_play_with_logging(play, players):
    try:
        process_play(play, players)
    except PlayNotFoundError as e:
        e.add_note('TypeCode = {0}'.format(play['typeCode']))
        e.add_note('Desc = {0}'.format(play['typeDescKey']))
        e.add_note('Event ID = {0}'.format(play['eventId']))
        raise e
