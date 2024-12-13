import re
from typing import Iterator, Optional
from pathlib import Path
import enum


class Instr(enum.Enum):
    DO = enum.auto()
    DONT = enum.auto()
    MUL = enum.auto()


def parse_file(name) -> Iterator[tuple[Instr, Optional[int], Optional[int]]]:
    with Path(__file__).parent.joinpath(name).open() as file:
        for line in file:
            yield from parse_line(line)


def parse_line(line: str) -> Iterator[tuple[Instr, Optional[int], Optional[int]]]:
    matches = re.finditer(r"(do|don't|mul)\((?:(\d{1,3}),(\d{1,3}))?\)", line)
    for instr in matches:
        match instr.group(1):
            case 'do':
                yield Instr.DO, None, None
            case "don't":
                yield Instr.DONT, None, None
            case 'mul':
                yield Instr.MUL, int(instr.group(2)), int(instr.group(3))


def solve(input_file) -> int:
    answer = 0
    enabled = True

    for instr, left, right in parse_file(input_file):
        match instr, enabled:
            case Instr.DO, False:
                enabled = True
            case (Instr.DONT, True):
                enabled = False
            case Instr.MUL, True:
                answer += left * right

    return answer


expected_answer = 48
test_answer = solve('example-2.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')