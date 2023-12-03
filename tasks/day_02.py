#!/usr/bin/env python

import math
import os
import re
import string
import sys
import time
from threading import Thread

# GLOBALS
input_data: list[str] = []
prev_time = time.process_time()
input_timeout = 5

filename = os.path.basename(__file__)
day_token = re.search(r"\d+", filename)
day_nr = day_token.group() if day_token else "unknown"
print(f"day_nr: {day_nr}")

# Day specific (globals)
MAX_NR_CUBES = {"red": 12,
                "green": 13,
                "blue": 14}


# MISC

def show_elapsed_time():
    global prev_time
    cur_time = time.process_time()
    diff = cur_time - prev_time
    prev_time = cur_time
    print(f"[{cur_time}] took: {diff} sec.")


# READ INPUT
def read_input():
    global input_data

    # print("reading input... START")

    cnt = 0
    for line in sys.stdin:
        cnt += 1
        # print(f"[{cnt}] {line}")

        # val = line.strip()
        # if len(val) > 0:
        input_data.append(line.strip())

    # print("reading input... END")


def controlled_input_read():
    read_input_thread = Thread(target=read_input, daemon=True, )
    read_input_thread.start()
    read_input_thread.join(timeout=input_timeout)
    if read_input_thread.is_alive():
        print(f"Timeout limit ({input_timeout} sec.) reached - exiting")
        sys.exit(1)


# SOLUTIONS
def _is_game_possible(cube_seqs: list[str]) -> bool:
    global MAX_NR_CUBES

    # cube_seqs: ['8 green, 6 blue, 20 red', '5 blue, 4 red, 13 green', '5 green, 1 red']
    for elem in cube_seqs:
        parts = elem.split(", ")
        # parts: ['8 green', '6 blue', '20 red']
        for cube in parts:
            value = int(cube.split()[0])
            color = cube.split()[1]
            if value > MAX_NR_CUBES[color]:
                return False

    return True


def find_solution_a():
    """
    Determine which games would have been possible if the bag had been loaded with only
     12 red cubes, 13 green cubes, and 14 blue cubes.
    What is the sum of the IDs of those games?
    """
    global input_data
    possible_game_id: list[int] = []

    for line in input_data:
        parts = line.split(": ")
        game_id = int(parts[0].strip(string.ascii_letters))
        cube_seqs = parts[1].split("; ")
        if _is_game_possible(cube_seqs):
            possible_game_id.append(game_id)

    result = sum(possible_game_id)

    return result


def _find_set_power(cube_seqs: list[str]) -> int:
    min_cube_set = {}

    # cube_seqs: ['8 green, 6 blue, 20 red', '5 blue, 4 red, 13 green', '5 green, 1 red']
    for elem in cube_seqs:
        parts = elem.split(", ")
        # parts: ['8 green', '6 blue', '20 red']
        for cube in parts:
            value = int(cube.split()[0])
            color = cube.split()[1]
            if value > min_cube_set.get(color, 0):
                min_cube_set[color] = value

    result = math.prod(min_cube_set.values())
    # print(f"result: {result}")

    return result


def find_solution_b():
    """
    What is the fewest number of cubes of each color that could have been in the bag to make the game possible?
    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
    For each game, find the minimum set of cubes that must have been present.
    What is the sum of the power of these sets?
    """

    global input_data
    set_power: list[int] = []

    for line in input_data:
        parts = line.split(": ")
        cube_seqs = parts[1].split("; ")
        set_power.append(_find_set_power(cube_seqs))

    result = sum(set_power)

    return result


# MAIN
def do_main():
    show_elapsed_time()

    # print("read input")
    controlled_input_read()

    show_elapsed_time()
    # print("len input_data:", len(input_data))
    # print("input_data", input_data)

    result_a = find_solution_a()
    print(f"result_a: {result_a}")
    show_elapsed_time()

    result_b = find_solution_b()
    print(f"result_b: {result_b}")
    show_elapsed_time()


if __name__ == "__main__":
    # execute only if run as a script
    do_main()
