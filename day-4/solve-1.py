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

    for y in range(0, height):
        for x in range(0, width):
            if puzzle[y][x] != 'X':
                continue

            if x >= 3 and y >= 3 and puzzle[y - 1][x - 1] == 'M' and puzzle[y - 2][x - 2] == 'A' and puzzle[y - 3][x - 3] == 'S':
                answer += 1
            if y >= 3 and puzzle[y - 1][x] == 'M' and puzzle[y - 2][x] == 'A' and puzzle[y - 3][x] == 'S':
                answer += 1
            if x < width - 3 and y >= 3 and puzzle[y - 1][x + 1] == 'M' and puzzle[y - 2][x + 2] == 'A' and puzzle[y - 3][x + 3] == 'S':
                answer += 1
            if x < width - 3 and puzzle[y][x + 1] == 'M' and puzzle[y][x + 2] == 'A' and puzzle[y][x + 3] == 'S':
                answer += 1
            if x < width - 3 and y < height - 3 and puzzle[y + 1][x + 1] == 'M' and puzzle[y + 2][x + 2] == 'A' and puzzle[y + 3][x + 3] == 'S':
                answer += 1
            if y < height - 3 and puzzle[y + 1][x] == 'M' and puzzle[y + 2][x] == 'A' and puzzle[y + 3][x] == 'S':
                answer += 1
            if x >= 3 and y < height - 3 and puzzle[y + 1][x - 1] == 'M' and puzzle[y + 2][x - 2] == 'A' and puzzle[y + 3][x - 3] == 'S':
                answer += 1
            if x >= 3 and puzzle[y][x - 1] == 'M' and puzzle[y][x - 2] == 'A' and puzzle[y][x - 3] == 'S':
                answer += 1

    return answer


expected_answer = 18
test_answer = solve('example.txt')
assert test_answer == expected_answer, f'Expected {expected_answer}, got {test_answer}'

real_answer = solve('input.txt')
print(f'Answer: {real_answer}')