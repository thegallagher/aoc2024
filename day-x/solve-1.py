from pathlib import Path
from typing import Iterator, Optional


def parse_file_1d(input_file) -> Iterator[tuple[int, int]]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = parse_line_1d(line)
            if line is not None:
                yield line


def parse_line_1d(line: str) -> Optional[tuple[int, int]]:
    line = line.strip('\n')
    if line == '':
        return None

    parts = line.split(' ')

    return int(parts[0]), int(parts[1])


def parse_file_2d(input_file) -> list[list[int]]:
    result = list()
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = parse_line_2d(line)
            if line is not None:
                result.append(line)
    return result


def parse_line_2d(line) -> Optional[list[int]]:
    line = line.strip('\n')
    if line == '':
        return None

    result = list()

    for part in line.split(' '):
        result.append(int(part))

    return result


def solve(input_file) -> int:
    answer = 0

    for left, right in parse_file_1d(input_file):
        answer += left * right

    # puzzle = parse_file_2d(input_file)
    # width = len(puzzle[0])
    # height = len(puzzle)
    #
    # for y in range(0, height):
    #     line = 1
    #     for x in range(0, width):
    #         line *= puzzle[y][x]
    #     answer += line

    return answer


expected_answer = 14
test_answer = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')