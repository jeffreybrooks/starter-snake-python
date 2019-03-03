""" Battlesnake utilities.
"""

### game startup utilities ###


def get_arena_bounds(data):
    """ Get the min and max [x,y] coordinates of the arena.

        Used to set the arena bounds at the start of the game so
        the bounds don't need to be looked up every turn.
    """
    arena = {'min':{'x':0,'y':0}, 'max':{'x':data['board']['height'] - 1, 'y':data['board']['width'] - 1}}
    return arena


def get_snake_color(color_name):
    """ Get the snake color hex value.

        Used to set the snake color at the start of the game.
        For more colors see: https://www.rapidtables.com/web/color/html-color-codes.html
        TODO: Is it possible to pass snake_color to start() instead of using a global?
    """
    global snake_color
    colors = {'red':'#FF0000',
            'orange':'#FFA500',
            'yellow':'#FFFF00',
            'lime':'#00FF00',
            'green':'#008000',
            'blue':'#0000FF',
            'purple':'#800080'
            }
    try:
        snake_color = colors[color_name]
    except:
        snake_color = colors['lime'] # starter snake color
    return snake_color


### game turn utilities ###


def get_current_head(data):
    """ Get the coordinates of the player's head. """
    head = {'x': data['you']['body'][0]['x'], 'y': data['you']['body'][0]['y']}
    return head


def get_legal_moves(head, arena):
    """ Get the legal (in-bounds) moves from a given position.

        I think this is useful only when there are no open moves.
        Hitting a wall is a "failure" in the official smoke test.
        See: https://rdbrck.com/2018/03/son-robosnake-aggressive-bounty-snake/
    """
    legal_moves = []
    if head['x'] > arena['min']['x']:
        legal_moves.append('left')
    if head['x'] < arena['max']['x']:
        legal_moves.append('right')
    if head['y'] > arena['min']['y']:
        legal_moves.append('up')
    if head['y'] < arena['max']['y']:
        legal_moves.append('down')
    return legal_moves


def get_open_moves(head, arena, data):
    """ Get directions the head can move without hitting a wall or a snake.
        TODO: Handle head-to-head collisions.
    """
    directions = ['up', 'down', 'left', 'right']
    open_moves = []
    for direction in directions:
        direction_is_open = True
        new_head = get_new_head(head, direction)
        if is_out_of_bounds(new_head, arena):
            direction_is_open = False
        else:
            for snake in data['board']['snakes']:
                for segment in snake['body']:
                    if new_head == segment:
                        direction_is_open = False
                        break
        if direction_is_open:
            open_moves.append(direction)
    return open_moves


def get_new_head(head, move):
    """ Get coordinates of the head after a move. """
    new_head = {}
    if move == 'left':
        new_head['x'] = head['x'] - 1
        new_head['y'] = head['y']
    elif move == 'right':
        new_head['x'] = head['x'] + 1
        new_head['y'] = head['y']
    elif move == 'up':
        new_head['x'] = head['x']
        new_head['y'] = head['y'] - 1
    elif move == 'down':
        new_head['x'] = head['x']
        new_head['y'] = head['y'] + 1
    return new_head


def is_out_of_bounds(location, arena):
    """ Determine whether a particular [x,y] location is outside the arena. """
    if (location['x'] < arena['min']['x'] or
        location['x'] > arena['max']['x'] or
        location['y'] < arena['min']['y'] or
        location['y'] > arena['max']['y']):
        return True
    else:
        return False
