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
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Personalize
        "head": "default",  # TODO: Personalize
        "tail": "default",  # TODO: Personalize
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    # A dictionary of coordinates like {"x": 0, "y": 0}
    my_head = my_snake["head"]
    # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_body = my_snake["body"]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)

    # TODO: Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    board = data['board']
    board_height = board['height']
    board_width = board['width']

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.
    possible_moves = avoid_walls(
        board_height, board_width, my_head, possible_moves)
    possible_moves = avoid_snakes(my_head, possible_moves, board["snakes"])
    possible_moves = avoid_hazards(my_head, possible_moves, board["hazards"])

    move = find_food(my_head, possible_moves, board["food"])
    print(move)

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

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
    my_head = my_body[0]  # The first body coordinate is always the head
    # The segment of body right after the head is the 'neck'
    my_neck = my_body[1]

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves
