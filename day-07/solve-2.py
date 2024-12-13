from pathlib import Path
from time import process_time_ns
from typing import Iterator, Optional, Generator


def parse_file_1d(input_file) -> Iterator[tuple[int, list[int]]]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            line = parse_line_1d(line)
            if line is not None:
                yield line


def parse_line_1d(line: str) -> Optional[tuple[int, list[int]]]:
    line = line.strip('\n')
    if line == '':
        return None

    parts = line.split(' ')

    return int(parts[0].strip(':')), list(map(int, parts[1:]))


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()
    answer = 0

    for expected, expr in parse_file_1d(input_file):
        for result in calc(expr[1:], expr[0]):
            if result == expected:
                answer += result
                break

    return answer, process_time_ns() - start_time


def calc(expr: list[int], carry: int) -> Generator[int]:
    if len(expr) == 0:
        yield carry
        return

    yield from calc(expr[1:], carry + expr[0])
    yield from calc(expr[1:], carry * expr[0])
    yield from calc(expr[1:], int(f'{carry}{expr[0]}'))


expected_answer = 11387
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')