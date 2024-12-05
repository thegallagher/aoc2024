from pathlib import Path


def parse_file(name) -> list[list[str]]:
    puzzle = list()
    with Path(__file__).parent.joinpath(name).open('r') as file:
        for line in file:
            puzzle.append(list(line.strip('\n')))
    return puzzle


def solve(input_file) -> int:
    puzzle = parse_file(input_file)
    width = len(puzzle[0])
    height = len(puzzle)

    answer = 0

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if puzzle[y][x] != 'A':
                continue

            nw = puzzle[y - 1][x - 1]
            sw = puzzle[y + 1][x + 1]
            ne = puzzle[y - 1][x + 1]
            se = puzzle[y + 1][x - 1]
            mas1 = f'{nw}A{sw}'
            mas2 = f'{ne}A{se}'

            if (mas1 == 'SAM' or mas1 == 'MAS') and (mas2 == 'SAM' or mas2 == 'MAS'):
                answer += 1

    return answer


expected_answer = 9
test_answer = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')