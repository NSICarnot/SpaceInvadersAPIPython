import hug
import falcon
import os
import dotenv
import sentry_sdk
from core.player import Player
from core.server import Global

dotenv.load_dotenv(".env")

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

@hug.post('/register-score', examples='player=HulkHogan6262&score=100&hash=6f9b9af3cd6e8b8a73c2cdced37fe9f5')
def register_score(player: hug.types.text("Player pseudo"), score: hug.types.accept(int, "The new score", "Invalid new score provided"), hash: hug.types.text("The verification hash")):
    "Register a new score for a player"
    player_obj = Player(player)
    if player_obj.get_md5() == hash:
        if score < 0:
            return {'success': False, 'error': 'score must be positive'}
        elif score > 1000000:
            return {'success': False, 'error': 'score must be less than 1000000'}
        elif score < player_obj.get_score():
            return {'success': False, 'error': 'score must be greater than current score'}
        else:
            player_obj.change_score(score)
            return {'success': True}
    else:
        return {'success': False, 'error': 'invalid hash'}

@hug.get('/player-score', examples='player=HulkHogan6262')
def get_score(player: hug.types.text("Player pseudo")):
    "Get the score of a player"
    player_obj = Player(player)
    score = player_obj.get_score()
    if score == None:
        return {'success': False, 'error': 'player not found'}
    else:
        return {'success': True, 'player': player, 'score': score}

@hug.get('/top', examples='limit=10')
def get_top(limit: hug.types.accept(int, "The max number of entries", "Invalid number provided") = 10):
    "Get the top players"
    global_obj = Global()
    fetched = global_obj.get_top(limit)
    data = []
    for i in fetched:
        data.append({'player': i[0], 'score': i[1]})
    return {'success': True, 'top': data}

@hug.get('/entries')
def get_number_of_entries():
    "Get the number of entries in the database"
    global_obj = Global()
    return {'success': True, 'number-of-entries': global_obj.get_number_of_entries()}

@hug.get('/average')
def get_average():
    "Get the average score of all players"
    global_obj = Global()
    return {'success': True, 'average': global_obj.get_average()}

if __name__ == '__main__':
    hug.API(__name__).http.serve(display_intro=False, port=80)