import re
from typing import Iterator
from pathlib import Path


def parse_file(name) -> Iterator[Iterator[int]]:
    with Path(__file__).parent.joinpath(name).open() as file:
        for line in file:
            yield from parse_line(line)


def parse_line(line: str) -> Iterator[tuple[int, int]]:
    matches = re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', line)
    for instr in matches:
        yield int(instr.group(1)), int(instr.group(2))


def solve(input_file) -> int:
    answer = 0

    for left, right in parse_file(input_file):
        answer += left * right

    return answer


expected_answer = 161
test_answer = solve('example-1.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')