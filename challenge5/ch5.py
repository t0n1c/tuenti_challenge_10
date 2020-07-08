import fileinput

# tuentistic indexes

VALID_INDEXES = {1, 4, 7, 10, 13, 16, 19}


def is_tuentistic(number):
    for i, digit in enumerate(reversed(str(number))):
        if digit == "2" and i in VALID_INDEXES:
            return True
    return False


def max_addends_len(number):
    quo, mod = divmod(number, 20)
    ones = quo * 9
    if ones >= mod:
        return quo
    else:
        return 'IMPOSSIBLE'
        
        
def main():
    lines = fileinput.input()
    _ = next(lines)
    for i, line in enumerate(lines, 1):
        number = int(line)
        res = max_addends_len(number)
        print(f"Case #{i}: {res}")


if __name__ == "__main__":
    main()

"""
from collections import deque
import inflect
p = inflect.engine()
n = int('1'*25)
n2 = 4611686018427387904

ndigits = 20 
dq = deque(['1' for _ in range(ndigits-1)] + ['2'])
for i in range(ndigits):
    number = ''.join(list(dq))
    words = p.number_to_words(number).lower()
    if 'twenty' in words:
        print(f"{number} -> { i }")
    dq.rotate(-1)
"""
