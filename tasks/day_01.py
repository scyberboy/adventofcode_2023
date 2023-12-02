#!/usr/bin/env python

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
    What is the sum of all the calibration values?
    On each line, the calibration value can be found by combining the first digit and the last digit (in that order)
     to form a single two-digit number.
    """
    global input_data
    # 1abc2
    # pqr3stu8vwx
    # a1b2c3d4e5f
    # treb7uchet

    stripped_data = [elem.strip(string.ascii_letters) for elem in input_data]
    # print(f"stripped_data: {stripped_data}")

    numeric_data = [int(elem[0] + elem[-1]) for elem in stripped_data if elem]
    # print(f"numeric_data: {numeric_data}")

    result = sum(numeric_data)

    return result


def translate_from_left(elem: str, wordy_digits, str_digits):
    match_indexes = []
    for idx in range(len(wordy_digits)):
        if wordy_digits[idx] in elem:
            match_indexes.append(elem.index(wordy_digits[idx]))
        else:
            match_indexes.append(1000000000)

    index_in_elem = min(match_indexes)
    index_in_digits = match_indexes.index(index_in_elem)

    new_elem = elem.replace(wordy_digits[index_in_digits], str_digits[index_in_digits], 1)
    return new_elem


def translate_from_right(elem: str, wordy_digits, str_digits):
    match_indexes = []
    for idx in range(len(wordy_digits)):
        if wordy_digits[idx] in elem:
            match_indexes.append(elem.rindex(wordy_digits[idx]))
        else:
            match_indexes.append(-1)

    index_in_elem = max(match_indexes)
    index_in_digits = match_indexes.index(index_in_elem)

    # be careful here, to really translate the right most occurrence ;)
    new_elem = elem[:index_in_elem] \
               + elem[index_in_elem:].replace(wordy_digits[index_in_digits], str_digits[index_in_digits], 1)

    return new_elem


def find_solution_b():
    """
    What is the sum of all the calibration values?
    It looks like some of the digits are actually spelled out with letters:
     one, two, three, four, five, six, seven, eight, and nine also count as valid "digits"
    """
    global input_data
    # two1nine
    # eightwothree
    # abcone2threexyz
    # xtwone3four
    # 4nineeightseven2
    # zoneight234
    # 7pqrstsixteen

    wordy_digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    str_digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    translated_data = input_data.copy()[-100:]

    # for elem in input_data.copy():
    #     blah = list(map(str.replace, [elem] * len(wordy_digits), wordy_digits, str_digits))
    #     print(f"blah: {blah}")
    #     translated_data.append(blah)

    # This kind-a work, but it doesn't take into account that words should be checked and translated consecutively
    #  After one is found on the left, we should start from the right. That's it. Then stop.
    # for idx, args in enumerate(zip(wordy_digits, str_digits)):
    #
    #     print(f"\targs: {args}")
    #     print(f"\targs[]: {[*args] * len(translated_data)}")
    #     translated_data = list(map(str.replace,
    #                                translated_data.copy(),
    #                                [args[0]] * len(translated_data),
    #                                [args[1]] * len(translated_data)))
    #     print(f"\t{idx}: {translated_data}")
    #     print("------------------")

    for idx, elem in enumerate(translated_data):
        print(f"\t{idx}: ori elem -> {elem}")

        # if it's already starts or ends with a digit - skip it :)
        if not re.match(r"^\d", elem):
            elem = translate_from_left(elem, wordy_digits, str_digits)
            print(f"\t{idx}: processed from left elem -> {elem}")
        if not re.match(r".*\d$", elem):
            elem = translate_from_right(elem, wordy_digits, str_digits)
            print(f"\t{idx}: processed from right elem -> {elem}")
        translated_data[idx] = elem

    print(f"\ntranslated_data: {translated_data}\n")

    stripped_data = [elem.strip(string.ascii_letters) for elem in translated_data]
    print(f"stripped_data: {stripped_data}\n")
    numeric_data = [int(elem[0] + elem[-1]) for elem in stripped_data if elem]
    print(f"numeric_data: {numeric_data}\n")

    result = sum(numeric_data)

    return result


# MAIN
def do_main():
    show_elapsed_time()

    # print("read input")
    controlled_input_read()

    show_elapsed_time()
    # print("input_data:", input_data)
    # print("len input_data:", len(input_data))

    result_a = find_solution_a()
    print(f"result_a: {result_a}")
    show_elapsed_time()

    result_b = find_solution_b()
    print(f"result_b: {result_b}")
    show_elapsed_time()


if __name__ == "__main__":
    # execute only if run as a script
    do_main()
