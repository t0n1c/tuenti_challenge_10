import fileinput
from collections import Counter


es_letters = "abcdefghijklmnopqrstuvwxyzáéíñóúü"
es_letters_cmp = {l: i for i, l in enumerate(es_letters)}


def clean_book(book_path):
    cleaned_book = []
    only_letters = set(es_letters)
    with open(book_path, mode="rt", encoding="UTF-8") as book:
        for line in book:
            if line.strip() == "":
                continue
            lower = [c if c in only_letters else " " for c in line.lower()]
            words = "".join(lower).split()
            words = [word for word in words if len(word) > 2]
            cleaned_line = " ".join(words)
            cleaned_book.append(cleaned_line)
    return cleaned_book


def count_words(book_path):
    book = clean_book(book_path)
    words_count = Counter()
    for line in book:
        for word in line.split():
            words_count[word] += 1
    return words_count


def multisort(items, specs):
    for key, reverse in reversed(specs):
        items = sorted(items, key=key, reverse=reverse)
    return items


def unicode_cmp(item):
    word, _ = item
    return [es_letters_cmp[c] for c in word]


def sort_words_count(words_count):
    items = words_count.items()
    specs = [(lambda item: item[1], True), (unicode_cmp, False)]
    return dict(multisort(items, specs))


def rank_words_count(words_count):
    return list(enumerate(words_count.items(), 1))


def words_lookup_table(ranked_words_count):
    return {word: (freq, rank) for rank, (word, freq) in ranked_words_count}


def ranking_lookup_table(ranked_words_count):
    return {rank: (word, freq) for rank, (word, freq) in ranked_words_count}


def precompute_lookup_tables(book_path):
    """Calculate two lookup tables that store the pairs
    requested by the challenge. These will be later indexed
    by words and ranks, respectively. This algorithm use multisort to get
    the requested order. Multisort relies on sorted() built-in which is stable.
    So we can first order by word, then by count. The algorithm will preserve
    the order by word that was already done."""
    words_count = count_words(book_path)
    sorted_words_count = sort_words_count(words_count)
    ranked_words_count = rank_words_count(sorted_words_count)
    word_lookup = words_lookup_table(ranked_words_count)
    rank_lookup = ranking_lookup_table(ranked_words_count)
    return word_lookup, rank_lookup


def main():
    word_lookup, rank_lookup = precompute_lookup_tables("pg17013.txt")
    lines = fileinput.input()
    _ = next(lines)
    for i, line in enumerate(lines, 1):
        try:
            rank = int(line)
        except ValueError:
            freq, rank = word_lookup[line.strip()]
            res = f"{freq} #{rank}"
        else:
            word, freq = rank_lookup[rank]
            res = f"{word} {freq}"
        print(f"Case #{i}: {res}")


if __name__ == "__main__":
    main()
