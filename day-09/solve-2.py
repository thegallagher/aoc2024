from pathlib import Path
from time import process_time_ns
from typing import Optional


def parse_file(input_file) -> list[int]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        line = file.readline()
        return list(map(int, list(line)))


def build_file_blocks_list(puzzle: list[int]) -> list[tuple[int, int]]:
    is_file = True
    file_blocks = []
    position = 0
    for value in puzzle:
        if is_file:
            file_blocks.append((position, value))

        position += value
        is_file = not is_file

    return file_blocks


def build_empty_blocks_list(puzzle: list[int]) -> list[tuple[int, int]]:
    is_file = True
    empty_blocks = []
    position = 0
    for value in puzzle:
        if not is_file:
            empty_blocks.append((position, value))

        position += value
        is_file = not is_file

    return empty_blocks


def defrag_file_blocks(file_blocks: list[tuple[int, int]], empty_blocks: list[tuple[int, int]]):
    for i in range(len(file_blocks) - 1, 0, -1):
        file_pos, file_size = file_blocks[i]
        empty_pos = find_empty(empty_blocks, file_size, file_pos)
        if empty_pos is None:
            continue

        file_blocks[i] = empty_pos, file_size


def find_empty(empty_blocks: list[tuple[int, int]], size: int, end_pos: int) -> Optional[int]:
    for i in range(len(empty_blocks)):
        empty_pos, empty_size = empty_blocks[i]
        if empty_size < size:
            continue
        if empty_pos >= end_pos:
            return None

        new_pos = empty_pos + size
        new_size = empty_size - size
        if new_size == 0:
            del empty_blocks[i]
        else:
            empty_blocks[i] = (new_pos, new_size)
        return empty_pos

    return None


def calc_checksum_blocks(file_blocks: list[tuple[int, int]]) -> int:
    checksum = 0
    for file_id in range(len(file_blocks)):
        file_pos, file_size = file_blocks[file_id]
        for i in range(file_pos, file_pos + file_size):
            checksum += file_id * i
    return checksum


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()

    puzzle = parse_file(input_file)
    file_blocks = build_file_blocks_list(puzzle)
    empty_blocks = build_empty_blocks_list(puzzle)
    defrag_file_blocks(file_blocks, empty_blocks)
    answer = calc_checksum_blocks(file_blocks)

    return answer, process_time_ns() - start_time


expected_answer = 2858
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')