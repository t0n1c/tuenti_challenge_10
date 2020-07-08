import fileinput

who_beats = {'S': 'P', 'P': 'R', 'R': 'S'}


def play_rps(shape1, shape2):
    if shape1 == shape2:
        return '-'
    elif who_beats[shape1] == shape2:
        return shape1
    else:
        return shape2


def main():
    lines = fileinput.input()
    _ = next(lines)
    for i, line in enumerate(lines, 1):
        print(f'Case #{i}: ' + play_rps(*line.split()))


if __name__ == "__main__":
    main()
