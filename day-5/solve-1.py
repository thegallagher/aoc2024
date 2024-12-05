from math import floor
from pathlib import Path
from typing import Iterator, Optional


def parse_file_rules(input_file) -> Iterator[tuple[int, int]]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = parse_line_rules(line)
            if line is not None:
                yield line


def parse_line_rules(line: str) -> Optional[tuple[int, int]]:
    line = line.strip('\n')
    if line == '':
        return None

    parts = line.split('|')

    return int(parts[0]), int(parts[1])


def parse_file_updates(input_file) -> Iterator[list[int]]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = parse_line_updates(line)
            if line is not None:
                yield line


def parse_line_updates(line: str) -> Optional[list[int]]:
    line = line.strip('\n')
    if line == '':
        return None

    return list(map(int, line.split(',')))


def solve(file_rules, file_updates) -> int:
    answer = 0

    rules = list(parse_file_rules(file_rules))

    for update in parse_file_updates(file_updates):
        if is_valid(rules, update):
            middle = floor(len(update) / 2.0)
            answer += update[middle]

    return answer


def is_valid(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for i in range(0, len(update) - 1):
        first = update[i]
        for n in range(i, len(update)):
            current = update[n]
            for before, after in rules:
                if current == before and first == after:
                    return False

    return True


expected_answer = 143
test_answer = solve('example-rules.txt', 'example-updates.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input-rules.txt', 'input-updates.txt')
print(f'Answer: {real_answer}')