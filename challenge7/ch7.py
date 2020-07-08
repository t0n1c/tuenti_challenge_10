import fileinput
from collections import Counter

str_from = "abcdefghijklmnopqrstuvwxyz" + "0123456789" + ".,;-/'"
str_to = "anihdyujgcvpmlsrxo;kf.,bt/" + "0123456789" + "ewz'-q"

dicc = str.maketrans(str_from, str_to)
# this dictionary was achieved manually by using cryptool and
# the hint given. Here I lay out the process i followed real quick
# the audio is  symphony no. 9 in e minor by Antonín Dvorák
# (8 o.ly.mx.p 1841  1 maf 1904) this looks like a date
# a google search yields Dvorak timelife
# (8 September 1841 – 1 May 1904)
# Two dates actually. It looks like some sort of substitution cipher!
# (8 o.ly.mx.p 1841  1 maf 1904)
# (8 September 1841 – 1 May 1904)
# m->m, o-s, .->e, x->b ...
# monoalphabetic cipher?? probably
# it might be some sort of biographical text about Dvorak
# so it would make sense that things like his name, country, symphonies..s
# show in this text
# also probably what comes right before the date is likely to be the name of
# the author which is Antonín Leopold Dvořák, let's assume only ascii
# characters, first we have to try the simple
# cnncam e.an.fvabyrbc
# b n.rlrne ekrpat
# b nErPrne ekrRAt
# so lets assume thats the name I mean the len of the words are equal!
# Lets play the Wheel of Fortune!! lets try vowelss!
# b nEOPOnD DkORAt
# b LEOPOLD DVORAK
# not bad with all this info that we have we can make more guesses
# a cipher cracker like cryptool will help


def freq_dict(filepath):
    with open(filepath) as fd:
        words = "".join([word.lower() for word in fd])
    freqs = Counter(words)
    return {letter: freq / len(words) for letter, freq in freqs.items()}


def decrypt(line):
    return line.translate(dicc).replace("\n", "")


def main():
    lines = fileinput.input()
    _ = next(lines)
    for i, line in enumerate(lines, 1):
        print(f"Case #{i}: {decrypt(line)}")


if __name__ == "__main__":
    main()
