from enum import Enum
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


class Direction(Enum):
    NORTH = 0, -1
    EAST = 1, 0
    SOUTH = 0, 1
    WEST = -1, 0

    def turn(self):
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()
    answer = 0

    puzzle = parse_file_2d(input_file)
    width = len(puzzle[0])
    height = len(puzzle)

    # Find the starting point of the guard
    origin_pos: Vec2 = 0, 0
    origin_direction: Direction = Direction.NORTH

    for y in range(0, height):
        for x in range(0, width):
            if puzzle[y][x] == GUARD:
                origin_pos = x, y

    # Find the path taken by the guard
    pos: Vec2 = origin_pos
    direction = origin_direction
    path: list[tuple[Vec2, Direction]] = []
    visited: set[Vec2] = set()

    while True:
        match vec2_add(pos, direction.value):
            case x, y if x < 0 or y < 0 or x >= width or y >= height:
                break

            case x, y if puzzle[y][x] == OBSTACLE:
                direction = direction.turn()

            case pos if not pos in visited:
                path.append((pos, direction))
                visited.add(pos)

    # Test placing obstacle at all points on the path
    start_pos = origin_pos
    start_direction: Direction = origin_direction
    for (obstacle_x, obstacle_y), obstacle_direction in path:
        pos = start_pos
        direction: Direction = start_direction
        puzzle[obstacle_y][obstacle_x] = OBSTACLE
        visited: dict[Vec2, set[Direction]] = {}

        while True:
            match vec2_add(pos, direction.value):
                case x, y if x < 0 or y < 0 or x >= width or y >= height:
                    break

                case x, y if puzzle[y][x] == OBSTACLE:
                    direction = direction.turn()

                case pos if pos not in visited:
                    visited[pos] = {direction}

                case pos if direction not in visited[pos]:
                    visited[pos].add(direction)

                case _:
                    answer += 1
                    break

        start_pos = obstacle_x, obstacle_y
        start_direction = obstacle_direction
        puzzle[obstacle_y][obstacle_x] = EMPTY

    return answer, process_time_ns() - start_time


expected_answer = 6
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')