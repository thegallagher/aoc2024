from pathlib import Path
from time import process_time_ns
from typing import Optional


def parse_file_2d(input_file) -> list[list[str]]:
    result = list()
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = parse_line_2d(line)
            if line is not None:
                result.append(line)
    return result


def parse_line_2d(line) -> Optional[list[str]]:
    line = line.strip('\n')
    if line == '':
        return None

    return list(line)


type Vec2 = tuple[int, int]


def vec2_add(a: Vec2, b: Vec2) -> Vec2:
    return a[0] + b[0], a[1] + b[1]


GUARD = '^'
OBSTACLE = '#'
EMPTY = '.'

NORTH = 0, 1
EAST = 1, 0
SOUTH = 0, -1
WEST = -1, 0


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()
    answer = 0

    puzzle = parse_file_2d(input_file)
    width = len(puzzle[0])
    height = len(puzzle)

    location: Vec2 = 0, 0
    direction: Vec2 = 0, -1

    for y in range(0, height):
        for x in range(0, width):
            if puzzle[y][x] == GUARD:
                location = x, y

    while True:
        next_location = vec2_add(location, direction)
        if next_location[0] < 0 or next_location[0] >= width or next_location[1] < 0 or next_location[1] >= height:
            answer += 1
            break

        if puzzle[next_location[1]][next_location[0]] == OBSTACLE:
            match direction:
                case 0, -1:
                    direction = 1, 0
                case 1, 0:
                    direction = 0, 1
                case 0, 1:
                    direction = -1, 0
                case -1, 0:
                    direction = 0, -1
            continue

        location = next_location
        if puzzle[next_location[1]][next_location[0]] == EMPTY:
            puzzle[next_location[1]][next_location[0]] = 'X'
            answer += 1

    return answer, process_time_ns() - start_time


expected_answer = 41
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')