from pathlib import Path
from time import process_time_ns


def parse_file(input_file) -> list[int]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        line = file.readline()
        return list(map(int, list(line)))


def build_disk_map(puzzle: list[int]) -> list[int]:
    is_file = True
    file_id = 0
    disk_map: list[int] = []
    for value in puzzle:
        if is_file:
            for _ in range(value):
                disk_map.append(file_id)
            file_id += 1
        else:
            for _ in range(value):
                disk_map.append(-1)

        is_file = not is_file

    return disk_map


def compact_disk_map(disk_map: list[int]):
    end_pos = len(disk_map) - 1
    for start_pos in range(len(disk_map)):
        if end_pos <= start_pos:
            break

        file_id = disk_map[start_pos]
        if file_id == -1:
            while disk_map[end_pos] < 0 and end_pos > start_pos:
                end_pos -= 1

            if end_pos <= start_pos:
                break

            disk_map[start_pos] = disk_map[end_pos]
            disk_map[end_pos] = -1
            end_pos -= 1

def calc_checksum(disk_map: list[int]) -> int:
    checksum = 0
    for pos in range(len(disk_map)):
        if disk_map[pos] < 0:
            break
        checksum += pos * disk_map[pos]
    return checksum


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()

    puzzle = parse_file(input_file)
    disk_map = build_disk_map(puzzle)
    compact_disk_map(disk_map)
    answer = calc_checksum(disk_map)

    return answer, process_time_ns() - start_time


expected_answer = 1928
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')