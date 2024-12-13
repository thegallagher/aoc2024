from typing import Iterator
from pathlib import Path


def parse_file(name) -> Iterator[list[int]]:
    with Path(__file__).parent.joinpath(name).open() as file:
        for line in file:
            yield parse_line(line)


def parse_line(line: str) -> list[int]:
    parts = line.split(' ')
    return list(map(int, parts))


def solve(input_file) -> int:
    answer = 0

    for report in parse_file(input_file):
        if is_safe(iter(report)):
            answer += 1
        else:
            for i in range(0, len(report)):
                filtered_report = report.copy()
                del filtered_report[i]
                if is_safe(iter(filtered_report)):
                    answer += 1
                    break

    return answer


def is_safe(report: Iterator[int]) -> bool:
    last = next(report)
    x = next(report)
    is_increasing = x > last

    if x == last or x > last + 3 or x < last - 3:
        return False

    last = x

    for x in report:
        if (is_increasing and x <= last) or (not is_increasing and x >= last) or x > last + 3 or x < last - 3:
            return False

        last = x

    return True


expected_answer = 4
test_answer = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')