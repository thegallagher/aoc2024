from pathlib import Path
from time import process_time_ns
from typing import Optional


type Vec2 = tuple[int, int]


def vec2_add(a: Vec2, b: Vec2) -> Vec2:
    return a[0] + b[0], a[1] + b[1]


def vec2_sub(a: Vec2, b: Vec2) -> Vec2:
    return a[0] - b[0], a[1] - b[1]


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


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()

    puzzle = parse_file_2d(input_file)
    width = len(puzzle[0])
    height = len(puzzle)
    frequencies: dict[str, list[Vec2]] = {}

    for y in range(0, height):
        for x in range(0, width):
            if puzzle[y][x] != '.':
                frequencies.setdefault(puzzle[y][x], [])
                frequencies[puzzle[y][x]].append((x, y))

    antinodes: set[Vec2] = set()
    for frequency in frequencies:
        antennas = frequencies[frequency]
        for antenna_a in antennas:
            for antenna_b in antennas:
                if antenna_a == antenna_b:
                    continue

                delta = vec2_sub(antenna_a, antenna_b)

                antinode_a = vec2_add(antenna_a, delta)
                if 0 <= antinode_a[0] < width and 0 <= antinode_a[1] < height:
                    antinodes.add(antinode_a)

                antinode_b = vec2_sub(antenna_b, delta)
                if 0 <= antinode_b[0] < width and 0 <= antinode_b[1] < height:
                    antinodes.add(antinode_b)

    answer = len(antinodes)

    return answer, process_time_ns() - start_time


expected_answer = 14
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')