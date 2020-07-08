import fileinput


def predict_winner(matches):
    losers = set()
    for p1, p2, w in matches:
        if w == 1:
            losers.add(p2)
        elif w == 0:
            losers.add(p1)
    players = set(range(1, len(losers)+1))
    return list(players - losers)[0]


def main():
    lines = fileinput.input()
    num_of_cases = int(next(lines))
    for i in range(1, num_of_cases+1):
        num_of_matches = int(next(lines))
        matches = []
        for _ in range(num_of_matches):
            match = [int(c) for c in next(lines).split()]
            matches.append(match)
        winner = predict_winner(matches)
        print(f'Case #{i}: {winner}')


if __name__ == "__main__":
    main()
