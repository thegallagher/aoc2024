from typing import Iterator
from pathlib import Path


def parse_file(name) -> Iterator[tuple[int, int]]:
    with Path(__file__).parent.joinpath(name).open() as file:
        for line in file:
            yield parse_line(line)


def parse_line(line: str) -> tuple[int, int]:
    parts = line.split(' ', 1)
    return int(parts[0].strip()), int(parts[1].strip())


def solve(input_file) -> int:
    left_list = []
    right_list = []

    for left, right in parse_file(input_file):
        left_list.append(left)
        right_list.append(right)

    left_list.sort()
    right_list.sort()

    answer = 0
    for left in left_list:
        count = right_list.count(left)
        answer += left * count

    return answer


expected_answer = 31
test_answer = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')