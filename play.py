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

def update_player_stat(play, players, player_key, player_update_func):
    player_id = None
    if 'details' in play and player_key in play['details']:
        player_id = play['details'][player_key]

    if player_id is not None:
        players[player_id].call(player_update_func)

def process_play(play, players):
    match play['typeCode']:

        case PlayType.FACEOFF:
            update_player_stat(play, players, 'winningPlayerId', 'add_faceoff_win')
            update_player_stat(play, players, 'losingPlayerId', 'add_faceoff_loss')

        case PlayType.SHOT_ON_GOAL:
            update_player_stat(play, players, 'shootingPlayerId', 'add_shot_on_goal')
            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats

        case PlayType.TAKEAWAY:
            update_player_stat(play, players, 'playerId', 'add_takeaway')

        case PlayType.PENALTY:
            update_player_stat(play, players, 'committedByPlayerId', 'add_penalty_committed') 
            update_player_stat(play, players, 'drawnByPlayerId', 'add_penalty_drawn') 
            update_player_stat(play, players, 'servedByPlayerId', 'add_penalty_served') 

        case PlayType.MISSED_SHOT:
            update_player_stat(play, players, 'shootingPlayerId', 'add_missed_shot')
            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats

        case PlayType.BLOCKED_SHOT:
            update_player_stat(play, players, 'shootingPlayerId', 'add_shot')
            update_player_stat(play, players, 'blockingPlayerId', 'add_blocked_shot')

        case PlayType.HIT:
            update_player_stat(play, players, 'hittingPlayerId', 'add_hit_given')
            update_player_stat(play, players, 'hitteePlayerId', 'add_hit_received')

        case PlayType.GOAL:
            update_player_stat(play, players, 'scoringPlayerId', 'add_goal')
            update_player_stat(play, players, 'assist1PlayerId', 'add_primary_assist')
            update_player_stat(play, players, 'assist2PlayerId', 'add_secondary_assist')
            goalie = get_playerId_maybe(play, 'goalieInNetId')
            # TODO: Add goalie stats
            # if goalie is not None:

        case PlayType.GIVEAWAY:
            update_player_stat(play, players, 'playerId', 'add_giveaway')

        case PlayType.FAILED_SHOT_ATTEMPT:
            update_player_stat(play, players, 'shootingPlayerId', 'add_so_failed_shot')
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
