from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from time import process_time_ns
from typing import Optional, Self, Union, Generator

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


def parse_file_matrix(input_file) -> Matrix[str]:
    result = list()
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = line.strip('\n')
            if line != '':
                result.append(list(line))
    return Matrix(result)


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()
    answer = 0

    puzzle = parse_file_matrix(input_file)

    complete: set[Vec2] = set()
    inside_queue: list[Vec2] = []
    outside_queue: list[Vec2] = [Vec2(0, 0)]

    while len(outside_queue) > 0:
        start = outside_queue.pop()
        inside_queue.append(start)
        region_id = puzzle[start]
        region_area = 0
        region_perimeter = 0

        while len(inside_queue) > 0:
            node = inside_queue.pop()
            if node in complete or node not in puzzle:
                continue
            complete.add(node)

            region_area += 1
            for direction in Directions:
                adjacent_node = node + direction.value
                if adjacent_node not in puzzle:
                    region_perimeter += 1
                    continue
                if puzzle[adjacent_node] == region_id:
                    inside_queue.append(adjacent_node)
                else:
                    region_perimeter += 1
                    outside_queue.append(adjacent_node)

        answer += region_area * region_perimeter

    return answer, process_time_ns() - start_time


expected_answer = 1930
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')