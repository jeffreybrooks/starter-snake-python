# Battlesnake imports
import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

# additional python imports
import argparse

# Battlesnake game startup utilities
from utils import get_arena_bounds, get_snake_color

# Battlesnake game turn utilities
from utils import get_current_head, get_legal_moves, get_open_moves, get_new_head, is_out_of_bounds

@bottle.route('/')
def index():
    return
    '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    global arena
    global snake_color

    data = bottle.request.json

    # Set the arena bounds, which don't change after the start of the game.
    arena = get_arena_bounds(data)

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    return start_response(snake_color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(json.dumps(data))

    head = get_current_head(data)
    open_moves = get_open_moves(head, arena, data)

    if len(open_moves) > 0:
        direction = random.choice(open_moves)
    else:
        direction = random.choice(get_legal_moves(head, arena)) # it's better to hit a snake than a wall

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

def parse_args():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-c', '--color',
                            action='store', dest='color_name', required=False, default='lime', # lime is the starter snake color
                            help='The snake''s color (default="lime")')
    optional.add_argument('-i', '--ip',
                            action='store', dest='ip', required=False, default='0.0.0.0',
                            help='The snake''s ip address (default="0.0.0.0")')
    optional.add_argument('-p', '--port',
                            action='store', dest='port', required=False, default='8080',
                            help='The snake''s port (default="8080")')
    optional.add_argument('-d', '--debug',
                            action='store', dest='debug', required=False, default=True,
                            help='Whether to debug (default=True)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    snake_color = get_snake_color(args.color_name)
    bottle.run(
        application,
        host=os.getenv('IP', args.ip),
        port=os.getenv('PORT', args.port),
        debug=os.getenv('DEBUG', args.debug)
    )
