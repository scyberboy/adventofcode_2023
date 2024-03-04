#!/usr/bin/env python
import multiprocessing
import os
import pprint
import re
import sys
import time
from threading import Thread
from typing import Optional, Tuple, List


# GLOBALS
input_data = []  # type: list[str]
seeds = []  # type: list[int]
seed_to_soil = []  # type: list[list[int]]
soil_to_fert = []  # type: list[list[int]]
fert_to_wate = []  # type: list[list[int]]
wate_to_ligh = []  # type: list[list[int]]
ligh_to_temp = []  # type: list[list[int]]
temp_to_humi = []  # type: list[list[int]]
humi_to_loca = []  # type: list[list[int]]

start_time_perf = time.perf_counter()
prev_time_perf = time.perf_counter()

input_timeout = 5
day_nr = "unknown"


def _init_globals():
    global day_nr
    # print(f"start {multiprocessing.current_process().name} - _init_globals")

    filename = os.path.basename(__file__)
    day_token = re.search(r"\d+", filename)
    day_nr = day_token.group() if day_token else "unknown"

    # print(f"day_nr [{multiprocessing.current_process().name}]: {day_nr}")


# MISC

def show_elapsed_time():
    global prev_time_perf, start_time_perf
    cur_time_perf = time.perf_counter()
    diff_perf = cur_time_perf - prev_time_perf
    total_elapsed_perf = cur_time_perf - start_time_perf
    print(f"[{total_elapsed_perf:#0.12f}] took: {diff_perf:#0.12f} sec.")


# READ INPUT
def read_input():
    global input_data, day_nr

    # print(f"reading input... START[{multiprocessing.current_process().name}], day_nr:", day_nr)

    cnt = 0
    filename = f"{day_nr}.inp.tmp"
    if not os.path.exists(filename):
        fout = open(filename, "w")

        for line in sys.stdin:
            cnt += 1
            # print(f"[{cnt}] {line}")

            # val = line.strip()
            # if len(val) > 0:
            input_data.append(line.strip())
            fout.write(f"{line.strip()}\n")

        fout.close()

    if len(input_data) == 0:
        # print("no input data on STDIN, try alternative (file read)")
        with open(filename, "r") as fin:
            for line in fin:
                input_data.append(line.strip())

    # print("reading input... END")


def controlled_input_read():
    read_input_thread = Thread(target=read_input, daemon=True, )
    read_input_thread.start()
    read_input_thread.join(timeout=input_timeout)
    if read_input_thread.is_alive():
        print(f"Timeout limit ({input_timeout} sec.) reached - exiting")
        sys.exit(1)

    # sys.exit(125)


# SOLUTIONS
def _fill_globals():
    global seeds, seed_to_soil, soil_to_fert, fert_to_wate, wate_to_ligh, ligh_to_temp, temp_to_humi, humi_to_loca

    # fill seeds
    while (elem := input_data.pop(0)) != "":
        seeds = [int(elem) for elem in elem.split(": ")[1].split()]
    # print(f"seeds: {seeds}")

    # fill seed_to_soil
    while (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        seed_to_soil.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"seed_to_soil: {seed_to_soil}")

    # fill soil_to_fert
    while (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        soil_to_fert.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"soil_to_fert: {soil_to_fert}")

    # fill fert_to_wate
    while (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        fert_to_wate.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"fert_to_wate: {fert_to_wate}")

    # fill wate_to_ligh
    while (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        wate_to_ligh.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"wate_to_ligh: {wate_to_ligh}")

    # fill ligh_to_temp
    while (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        ligh_to_temp.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"ligh_to_temp: {ligh_to_temp}")

    # fill temp_to_humi
    while (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        temp_to_humi.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"temp_to_humi: {temp_to_humi}")

    # fill humi_to_loca
    while input_data and (elem := input_data.pop(0)) != "":
        if not elem[0].isdigit():
            continue
        humi_to_loca.append([int(sub_elem) for sub_elem in elem.split()])
    # print(f"humi_to_loca: {humi_to_loca}")


def _find_destination_id(_map: list[list[int]], _source_id: int) -> Optional[int]:
    dest_id = None

    # print(f"_map: {_map}, _source_id: {_source_id}")

    if not _source_id:
        raise ValueError(f"Got empty _source_id to lookup")

    for dest_start, source_start, size in _map:
        # print(f"dest_start: {dest_start}, source_start: {source_start}, size: {size}")
        if source_start <= _source_id < source_start + size:
            offset = _source_id - source_start
            dest_id = dest_start + offset
            # print("Matched! - breaking")
            break

    # Any source numbers that aren't mapped correspond to the same destination number.
    # print(f"dest_id: {dest_id}")
    return dest_id if dest_id else _source_id


def find_solution_a():
    """
    What is the lowest location number that corresponds to any of the initial seed numbers?
    soil, fert, wate, ligh, temp, humi, loca
    """
    location_ids: list[int] = []

    for seed in seeds:
        id_soil = _find_destination_id(seed_to_soil, seed)
        id_fert = _find_destination_id(soil_to_fert, id_soil)
        id_wate = _find_destination_id(fert_to_wate, id_fert)
        id_ligh = _find_destination_id(wate_to_ligh, id_wate)
        id_temp = _find_destination_id(ligh_to_temp, id_ligh)
        id_humi = _find_destination_id(temp_to_humi, id_temp)
        id_loca = _find_destination_id(humi_to_loca, id_humi)

        if not id_loca:
            raise ValueError(f"Location not found for seed {seed}")
        location_ids.append(id_loca)

    # print(f"location_ids: {location_ids}")
    result = min(location_ids)
    # try 01 -> 84470622 (OK)

    return result


def find_solution_b():
    """
    Consider all the initial seed numbers listed in the ranges on the first line of the almanac.
    What is the lowest location number that corresponds to any of the initial seed numbers?
    soil, fert, wate, ligh, temp, humi, loca
    """
    min_location_id: int = float("inf")

    # now seeds are in ranges: _start, _size, _start, _size, _start, _size, ...
    while seeds:

        _start = seeds.pop(0)
        _size = seeds.pop(0)
        for seed in range(_start, _start + _size):
            id_soil = _find_destination_id(seed_to_soil, seed)
            id_fert = _find_destination_id(soil_to_fert, id_soil)
            id_wate = _find_destination_id(fert_to_wate, id_fert)
            id_ligh = _find_destination_id(wate_to_ligh, id_wate)
            id_temp = _find_destination_id(ligh_to_temp, id_ligh)
            id_humi = _find_destination_id(temp_to_humi, id_temp)
            id_loca = _find_destination_id(humi_to_loca, id_humi)

            if not id_loca:
                raise ValueError(f"Location not found for seed {seed}")

            if id_loca < min_location_id:
                min_location_id = id_loca

        print(f"Current seed range: [{_start} + {_size}]")
        print(f"Min location ids so far: {min_location_id}")
        show_elapsed_time()

    # print(f"min_location_id: {min_location_id}")
    result = min_location_id

    return result


def find_solution_b_opt() -> int:

    global seeds
    seeds_list = seeds

    global seed_to_soil, soil_to_fert, fert_to_wate, wate_to_ligh, ligh_to_temp, temp_to_humi, humi_to_loca

    # Split the seed ranges into chunks for parallel processing
    seed_chunks: List[Tuple[float, float]] = [(seeds_list[i], seeds_list[i + 1]) for i in range(0, len(seeds_list), 2)]
    print("Seed chunks: ", seed_chunks)

    # Further split task chunks within each range
    task_chunks: List[List[Tuple[float, float]]] = [split_range(seed_range) for seed_range in seed_chunks]
    # print("Task chunks: ", task_chunks)

    # Create a pool of worker processes
    num_processes: float = multiprocessing.cpu_count()
    print("Number of processes: ", num_processes)

    min_results: List[int] = []
    for task_list in task_chunks:
        with multiprocessing.Pool(processes=num_processes) as pool:
            combined_results: List[int] = pool.map(worker_function, task_list)

        print(f"Combined results so far: {combined_results}")
        min_results.append(min(combined_results))
        show_elapsed_time()

    print(f"Min results: {min_results}")

    # Get the final one...
    result: int = min(min_results)

    # Try 01 -> 26714516 (OK)
    return result


def worker_function(task_range: Tuple[float, float]) -> float:
    # print("{} says START".format(multiprocessing.current_process().name))
    _init_globals()
    controlled_input_read()
    _fill_globals()

    global seed_to_soil, soil_to_fert, fert_to_wate, wate_to_ligh, ligh_to_temp, temp_to_humi, humi_to_loca

    start_index, end_index = task_range

    result = float("inf")  # Perform the computation on the range[start_index, end_index)

    for seed in range(start_index, end_index):
        id_soil = _find_destination_id(seed_to_soil, seed)
        id_fert = _find_destination_id(soil_to_fert, id_soil)
        id_wate = _find_destination_id(fert_to_wate, id_fert)
        id_ligh = _find_destination_id(wate_to_ligh, id_wate)
        id_temp = _find_destination_id(ligh_to_temp, id_ligh)
        id_humi = _find_destination_id(temp_to_humi, id_temp)
        id_loca = _find_destination_id(humi_to_loca, id_humi)

        if not id_loca:
            raise ValueError(f"Location not found for seed {seed}")

        if id_loca < result:
            result = id_loca

    # Debug info
    # print("{} says that [{}, {}) = {}".format(multiprocessing.current_process().name, start_index, end_index, result))

    return result


def split_range(seed_range: Tuple[float, float]) -> List[Tuple[float, float]]:
    start_index, size = seed_range
    # print(f"start_index: {start_index}, size: {size}")

    # Add logic to split the range into smaller task chunks
    # Let's split on chunks of 1/7 of the size
    chunk_size: float = (size // 7) + 1
    # print(f"chunk_size: {chunk_size}")

    task_chunks: List[Tuple[float, float]] = []
    for i in range(int(size // chunk_size + 1)):
        _idx_from = start_index + i * chunk_size
        _idx_to = min(start_index + (i + 1) * chunk_size, start_index + size)
        task_chunks.append((_idx_from, _idx_to))

    return task_chunks


# MAIN
def do_main():
    _init_globals()

    show_elapsed_time()

    # print("read input")
    controlled_input_read()

    # show_elapsed_time()
    # print("len input_data:", len(input_data))
    # print("input_data: \n", pprint.pformat(input_data))

    _fill_globals()

    result_a = find_solution_a()
    print(f"result_a: {result_a}")
    show_elapsed_time()

    # result_b = find_solution_b()
    # print(f"result_b: {result_b}")
    result_b_opt = find_solution_b_opt()
    print(f"result_b_opt: {result_b_opt}")
    show_elapsed_time()


if __name__ == "__main__":
    # execute only if run as a script
    do_main()
