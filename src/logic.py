from calendar import c
import random
from typing import List, Dict

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""


def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "gbaby",
        "color": "#0b49da",
        "head": "gamer",
        "tail": "coffee",
    }


def choose_move(data: dict) -> str:
    my_snake = data["you"]     

    my_head = my_snake["head"]

    my_body = my_snake["body"]

    possible_moves = ["up", "down", "left", "right"]

    possible_moves = _avoid_my_neck(my_body, possible_moves)

    board = data['board']
    board_height = board['height']
    board_width = board['width']

    possible_moves = avoid_walls(
        board_height, board_width, my_head, possible_moves)
    possible_moves = avoid_snakes(my_head, possible_moves, board["snakes"])
    possible_moves = avoid_hazards(my_head, possible_moves, board["hazards"])

    move = find_food(my_head, possible_moves, board["food"])

    return move


def avoid_walls(height, width, my_head, possible_moves):
    if (height - 1 == my_head['y']):
        possible_moves.remove('up')
    if (my_head['y'] == 0):
        possible_moves.remove('down')
    if (width - 1 == my_head['x']):
        possible_moves.remove('right')
    if (my_head['x'] == 0):
        possible_moves.remove('left')
    return possible_moves


def avoid_snakes(my_head, possible_moves, snakes):
    for snake in snakes:
        possible_moves =  avoid_hazards(my_head, possible_moves, snake['body'])
    return possible_moves

def avoid_hazards(my_head, possible_moves, hazards):
    for hazard in hazards:
        if (hazard['x'] != my_head['x'] and hazard['y'] != my_head['y']):
            continue
        if (hazard['y'] - 1 == my_head['y']):
            if 'up' in possible_moves:
                possible_moves.remove('up')
        if (hazard['y'] + 1 == my_head['y']):
            if 'down' in possible_moves:
                possible_moves.remove('down')
        if (hazard['x'] - 1 == my_head['x']):
            if 'right' in possible_moves:
                possible_moves.remove('right')
        if (hazard['x'] + 1 == my_head['x']):
            if 'left' in possible_moves:
                possible_moves.remove('left')
    return possible_moves



def myfunc(my_x, my_y, food):
    return abs(my_x - food['x']) + abs(my_y - food['y'])


def find_food(my_head, possible_moves, foods):
    closest_food = {'x': 1000000, 'y': 1000000}
    for food in foods:
        if myfunc(my_head['x'], my_head['y'], food) < myfunc(my_head['x'], my_head['y'], closest_food):
            closest_food = food
    if closest_food['x'] > my_head['x'] and 'right' in possible_moves:
        return 'right'
    if closest_food['y'] > my_head['y'] and 'up' in possible_moves:
        return 'up'
    if 'left' in possible_moves and closest_food['x'] < my_head['x']:
        return 'left'
    if 'down' in possible_moves and closest_food['y'] < my_head['y']:
        return 'down'
    return possible_moves[0]


def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    my_head = my_body[0] 

    my_neck = my_body[1]

    if my_neck["x"] < my_head["x"]: 
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]: 
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]: 
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]: 
        possible_moves.remove("up")

    return possible_moves
