#!/usr/bin/env python
import math
import os
import pprint
import re
import sys
import time
import typing
from collections import OrderedDict
from threading import Thread
from typing import Optional

# GLOBALS
input_data = []
prev_time = time.process_time()
input_timeout = 5

filename = os.path.basename(__file__)
day_token = re.search(r"\d+", filename)
day_nr = day_token.group() if day_token else "unknown"
print(f"day_nr: {day_nr}")


class Array2D:
    """
    This class will abstract an underlying data which is list of strings:
     - each element is a row (accessible by Y)
     - each character of a string is a column (accessible by X)
       X X X X X X X X X X X X
     Y data[0][0]...data[9][0]
     Y data[0][1]...data[9][1]
     Y .......................
     Y data[0][9]...data[9][9]
    And will make it accessible as C-style 2-dimensional array :)
    With few convenient methods...
    """

    __data: list[str] = []
    __size_x: int = 0  # nr of columns
    __size_y: int = 0  # nr of rows

    def __init__(self, data: list[str], size_x: int = None, size_y: int = None):
        self.__data = data

        if size_x:
            self.__size_x = size_x
        elif len(data) > 0:
            self.__size_x = len(data[0])
        else:
            self.__size_x = 0

        if size_y:
            self.__size_y = size_y
        else:
            self.__size_y = len(data)

    def __repr__(self):
        return f"Array(X size: {self.size_x}, Y size: {self.size_y}\nDATA: {self.data}\n)"

    @property
    def data(self) -> list[str]:
        return self.__data

    @data.setter
    def data(self, new_data):
        self.__data = new_data

    @property
    def size_x(self) -> int:
        return self.__size_x

    @size_x.setter
    def size_x(self, new_x):
        self.__size_x = new_x

    @property
    def size_y(self) -> int:
        return self.__size_y

    @size_y.setter
    def size_y(self, new_y):
        self.__size_y = new_y

    def get_nr_elements(self) -> int:
        return self.size_x * self.size_y

    def get_linear_element(self, linear_nr) -> Optional[str]:
        if linear_nr > self.get_nr_elements():
            return None
        _y = linear_nr // self.size_x
        _x = (linear_nr - 1) % self.size_x

        return self.data[_y][_x]

    def valid_coords(self, _x: int, _y: int) -> bool:
        if 0 <= _x < self.size_x and 0 <= _y < self.size_y:
            return True
        else:
            return False

    def get_element(self, _x: int, _y: int) -> Optional[str]:
        if self.valid_coords(_x, _y):
            return self.data[_y][_x]
        else:
            return None

    def get_neighbours(self, _x: int, _y: int) -> list[(int, int)]:
        """
        :param _x:
        :param _y:
        :return: List with coordinates as tuple (x,y) of all neighbours of the given element
        """
        neigh_offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
        neighs = []
        for x_off, y_off in neigh_offsets:
            neigh_x = _x + x_off
            neigh_y = _y + y_off
            if self.valid_coords(neigh_x, neigh_y):
                neighs.append((neigh_x, neigh_y))
        return neighs


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
def find_solution_a():
    """
    Any number adjacent to a symbol (*#+1$....), even diagonally, is a "part number" and should be included in your sum.
    (Periods (.) do not count as a symbol.)
    What is the sum of all the part numbers in the engine schematic?
    """
    global input_data

    engine_map = Array2D(input_data)
    # print(f"engine_map: {engine_map}")

    part_numbers: list[int] = []

    curr_nr_str = ""
    curr_nr_neighs_coords: set[(int, int)] = set()
    for _y in range(engine_map.size_y):
        for _x in range(engine_map.size_x):
            # print(f"Inner FOR: x({_x}), y({_y})")
            curr_elem = engine_map.get_element(_x, _y)
            # print(f"curr_elem: {curr_elem}")

            if curr_elem.isdigit():
                curr_nr_str += curr_elem
                curr_elem_neighs = engine_map.get_neighbours(_x, _y)
                # print(f"curr_elem_neighs: {curr_elem_neighs}")
                curr_nr_neighs_coords.update(curr_elem_neighs)

            if ((not curr_elem.isdigit() and len(curr_nr_str) > 0)
                    or (_x == engine_map.size_x - 1)):  # we have something already
                # print(f"curr_nr_str: {curr_nr_str}")
                # print(f"curr_nr_neighs_coords: {curr_nr_neighs_coords}")
                neigh_values = [engine_map.get_element(_n_x, _n_y) for _n_x, _n_y in curr_nr_neighs_coords]
                # print(f"neigh_values: {neigh_values}")
                symbol_neigh = [elem for elem in neigh_values if not elem.isdigit() and elem != "."]
                if symbol_neigh:
                    curr_nr = int(curr_nr_str)
                    # print(f"VLIZA <--({_x}, {_y}): {curr_nr_str}")
                    part_numbers.append(curr_nr)
                elif curr_nr_str:
                    # print(f"NEVLIZA <--({_x}, {_y}): {curr_nr_str}")
                    pass
                curr_nr_str = ""
                curr_nr_neighs_coords = set()

    result = sum(part_numbers)

    # ret 1 & 2 -> 8474516 (too high) :(
    # ret 3     -> 532331
    return result


def _find_number(engine_map: Array2D, _x: int, _y: int) -> list[(int, int)]:
    # return a list of coordinates of a whole  number, starting from one if its digits
    result: list[(int, int)] = [(_x, _y)]

    # 1. check left
    _start = _x
    while True:
        _start -= 1
        elem = engine_map.get_element(_start, _y)
        if elem and elem.isdigit():
            result.append((_start, _y))
            # print(f"check left, result: {result}")
        else:
            # print("check left, break")
            break

    # 2. check right
    _end = _x
    while True:
        _end += 1
        elem = engine_map.get_element(_end, _y)
        if elem and elem.isdigit():
            result.append((_end, _y))
            # print(f"check right, result: {result}")
        else:
            # print("check right, break")
            break

    return sorted(result)


def _get_numbers(engine_map: Array2D, neighs_values_sorted: dict[(int, int): str]) -> list[int]:
    # neighs_values_sorted: {(2, 0): '7', (2, 2): '3', (3, 2): '5'}
    result: list[int] = []
    processed: set[(int, int)] = set()
    for _x, _y in neighs_values_sorted:
        if (_x, _y) in processed:
            continue
        number_coors = _find_number(engine_map, _x, _y)
        # print(f"({_x, _y}) -> got number coors: {number_coors}")
        processed.update(number_coors)
        number_value = int("".join([engine_map.get_element(_nx, _ny) for _nx, _ny in number_coors]))
        # print(f"({_x, _y}) -> got number value: {number_value}")
        result.append(number_value)

    return result


def find_solution_b():
    """
    A gear is any * symbol that is adjacent to exactly two part numbers.
    Its gear ratio is the result of multiplying those two numbers together.
    What is the sum of all the gear ratios in your engine schematic?
    """
    global input_data

    engine_map = Array2D(input_data)
    # print(f"engine_map: {engine_map}")

    gear_ratio: list[int] = []

    for _y in range(engine_map.size_y):
        for _x in range(engine_map.size_x):
            curr_elem = engine_map.get_element(_x, _y)
            if curr_elem == "*":
                # print("------------")
                curr_elem_neighs = engine_map.get_neighbours(_x, _y)
                # print(f"curr_elem_neighs: {curr_elem_neighs}")
                neighs_numeric_values = [((_n_x, _n_y), num_val) for _n_x, _n_y in curr_elem_neighs
                                         if (num_val := engine_map.get_element(_n_x, _n_y)).isdigit()]
                # print(f"neighs_numeric_values: {neighs_numeric_values}")
                neighs_values_sorted = dict(sorted(neighs_numeric_values))
                # print(f"neighs_values_sorted: {neighs_values_sorted}")

                if len(neighs_numeric_values) >= 2:  # we're interested :)
                    # ------------
                    # curr_elem_neighs: [(2, 1), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (3, 2), (2, 2)]
                    # neighs_numeric_values: [((2, 0), '7'), ((3, 2), '5'), ((2, 2), '3')]
                    # neighs_values_sorted: {(2, 0): '7', (2, 2): '3', (3, 2): '5'}
                    # ------------
                    numbers = _get_numbers(engine_map, neighs_values_sorted)
                    # print(f"numbers: {numbers}")
                    if len(numbers) == 2:
                        # print(f"numbers: {numbers}")
                        gear_ratio.append(math.prod(numbers))
                        # print(f"gear_ratio: {gear_ratio}")

    result = sum(gear_ratio)

    # try 01 -> 82301120 (OK) :)

    return result


# MAIN
def do_main():
    show_elapsed_time()

    # print("read input")
    controlled_input_read()

    show_elapsed_time()
    # print("len input_data:", len(input_data))
    # print("input_data:\n", pprint.pformat(input_data))

    result_a = find_solution_a()
    print(f"result_a: {result_a}")
    show_elapsed_time()

    result_b = find_solution_b()
    print(f"result_b: {result_b}")
    show_elapsed_time()


if __name__ == "__main__":
    # execute only if run as a script
    do_main()
