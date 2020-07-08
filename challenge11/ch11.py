import fileinput


def total_operations(value, exclude):
    """In this challenge I will be using dynamic programming. 
        Bottom up approach i.e. tabular form (flattened table). Any sort of 
        generating-permutations algorithm will make you older if 
        it does not crash before"""

    include = set(range(1, value)) - set(exclude)
    table = [0] * (value + 1)
    table[0] = 1
    for addend in include:
        for sub_value in range(1, value + 1):
            if sub_value >= addend:
                # here is the clever operation
                # sub_value - addend is indeed
                # a subproblem already solved in table!
                table[sub_value] += table[sub_value - addend]
    return table[value]  # our original problem


def main():
    lines = fileinput.input()
    _ = next(lines)
    for i, line in enumerate(lines, 1):
        splitted = line.split()
        try:
            value, exclude = splitted[0], splitted[1:]
        except IndexError:
            value, exclude = splitted[0], []
        value, exclude = int(value), map(int, exclude)
        # print(f"value: {value}")
        # print(f"exclude: {exclude}")

        print(f'Case #{i}: {total_operations(value, exclude)}')


if __name__ == "__main__":
    main()
