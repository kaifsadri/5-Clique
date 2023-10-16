from collections import defaultdict, Counter
from time import perf_counter

start = perf_counter()
L = list()
S = set()
for w in open("words.txt", "r").read().split():
    if len(w) == len(set(w)) == 5:
        L.append(w.upper())
        S.add(frozenset(w.upper()))
print(f"{len(L)} words with 5 unique letters.")
print(f"{len(S)} unique words not including anagrams.")
# Giving highest value to the least common letters
cnts = Counter()
for word in S:
    cnts += Counter(word)
C = "".join(c[0] for c in cnts.most_common())
print(f"Order of letters by decreasing frequency is {C}.")
M = dict((letter, 1 << n) for n, letter in enumerate(C))
R = dict((v, k) for (k, v) in M.items())
# Calculating bit masks and filtering anagrams
BitMasks = defaultdict(set)
for word in L:
    bm = 0
    for letter in word:
        bm |= M[letter]
    BitMasks[bm].add(word)
B = sorted(BitMasks, reverse=True)  # This sorting speeds up finding the first result.
# Dict mapping all lesser words that do not overlap with a bitmask.
D = dict()
for i, word in enumerate(B):
    D[word] = set(b for b in B[i + 1 :] if b & word == 0)
N = 0
for w1 in B:
    for w2 in (s1 := D[w1]):
        for w3 in (s2 := s1 & D[w2]):
            for w4 in (s3 := s2 & D[w3]):
                for w5 in s3 & D[w4]:
                    N += 1
                    print(
                        f"Solution {N:3d} at {perf_counter()-start:.2f}s: {' '.join(repr(BitMasks[w]) for w in (w1, w2, w3, w4, w5))} "
                        f"Excludes : {R[((1<<26)-1)^(w1|w2|w3|w4|w5)]}"
                    )
print(f"{N} solutions found in {perf_counter() - start:.2f}.")
