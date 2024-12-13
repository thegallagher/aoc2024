from functools import cmp_to_key
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

    rules_dict: dict[int, set[int]] = {}

    for before, after in parse_file_rules(file_rules):
        if after not in rules_dict:
            rules_dict[after] = set()
        rules_dict[after].add(before)

    def fn_sort(a, b) -> int:
        if a == b:
            return 0
        elif b in rules_dict and a in rules_dict[b]:
            return -1
        return 1

    for update in parse_file_updates(file_updates):
        if is_valid(rules_dict, update):
            continue

        update.sort(key=cmp_to_key(fn_sort))
        middle = floor(len(update) / 2.0)
        answer += update[middle]

    return answer

# Quadratic time solution
# def is_valid(rules_dict: dict[int, set[int]], update: list[int]) -> bool:
#     for i in range(0, len(update) - 1):
#         first = update[i]
#         for n in range(i, len(update)):
#             current = update[n]
#             if first in rules_dict and current in rules_dict[first]:
#                 return False
#
#     return True


# Linear time solution (not needed for this puzzle but preparing myself for more complexity)
def is_valid(rules_dict: dict[int, set[int]], update: list[int]) -> bool:
    not_allowed: set[int] = set()
    for page in update:
        if page in not_allowed:
            return False

        if page in rules_dict:
            not_allowed.update(rules_dict[page])

    return True


expected_answer = 123
test_answer = solve('example-rules.txt', 'example-updates.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input-rules.txt', 'input-updates.txt')
print(f'Answer: {real_answer}')