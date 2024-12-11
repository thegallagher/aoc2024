from pathlib import Path
from time import process_time_ns
from typing import Iterator


def parse_file(input_file) -> Iterator[int]:
    with Path(__file__).parent.joinpath(input_file).open() as file:
        for line in file:
            yield from map(int, line.split(' '))


def solve(input_file) -> tuple[int, int]:
    start_time = process_time_ns()
    answer = 0
    puzzle = list(parse_file(input_file))

    for stone in puzzle:
        answer += count_stones(stone, 25)

    return answer, process_time_ns() - start_time


def count_stones(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return count_stones(1, blinks - 1)
    elif len(str(stone)) % 2 == 0:
        middle = int(len(str(stone)) / 2)
        left = int(str(stone)[:middle])
        right = int(str(stone)[middle:])
        return count_stones(left, blinks - 1) + count_stones(right, blinks - 1)
    else:
        return count_stones(stone * 2024, blinks - 1)


expected_answer = 55312
test_answer, test_time = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'
print(f'Test: {test_answer} ({test_time / 1_000_000.0:.2f}ms)')

real_answer, real_time = solve('input.txt')
print(f'Answer: {real_answer} ({real_time / 1_000_000.0:.2f}ms)')