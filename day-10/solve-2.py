from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from time import process_time_ns
from typing import Optional, Generator, Self, Union


type Vec2Tuple = tuple[int, int]
type Vec2Like = Union[Vec2, Vec2Tuple]


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Vec2(self.x - other.x, self.y - other.y)

    def __getitem__(self, item: int) -> Optional[int]:
        match item:
            case 0: return self.x
            case 1: return self.y
            case _: return None


class Matrix[T]:
    _width: int
    _height: int
    _data: list[list[T]]

    def __init__(self, data: list[list[T]]):
        self._data = data
        self._width = len(data[0])
        self._height = len(data)

    def __contains__(self, item: Vec2Like) -> bool:
        return 0 <= item[0] < self._width and 0 <= item[1] < self._height

    def __getitem__(self, item: Vec2Like) -> Optional[T]:
        if item not in self:
            return None
        return self._data[item[0]][item[1]]

    def __iter__(self) -> Generator[Vec2]:
        for y in range(0, self._height):
            for x in range(0, self._width):
                yield Vec2(x, y)

    def __repr__(self) -> str:
        return '\n'.join(map(lambda row: ''.join(row), self._data))


class Directions(Enum):
    NORTH = Vec2(0, -1)
    EAST = Vec2(1, 0)
    SOUTH = Vec2(0, 1)
    WEST = Vec2(-1, 0)


def parse_file_matrix(input_file) -> Matrix[int]:
    result = list()
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = line.strip('\n')
            if line != '':
                result.append(list(map(int, line)))
    return Matrix(result)


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()
    answer = 0

    puzzle = parse_file_matrix(input_file)

    for pos in puzzle:
        if puzzle[pos] == 0:
            answer += get_rating(puzzle, pos, 0)

    return answer, process_time_ns() - start_time


def get_rating(puzzle: Matrix[int], current_pos: Vec2, current_level: int) -> int:
    if current_level == 9:
        return 1

    rating = 0
    next_level = current_level + 1
    for direction in Directions:
        next_pos = current_pos + direction.value
        if puzzle[next_pos] == next_level:
            rating += get_rating(puzzle, next_pos, next_level)

    return rating


expected_answer = 81
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')