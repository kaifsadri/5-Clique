from collections import defaultdict, Counter
from time import perf_counter

with open("words.txt", "r") as words:
    lex = list(w.upper() for w in words.read().split() if len(w) == len(set(w)) == 5)
print(f"\nFound {len(lex)} suitable words in the input provided.")

# Giving highest value to the least common letters
cnts = Counter()
for word in lex:
    cnts += Counter(word)
print(f"Order of letters by frequency is {''.join(cnts)}.")

M = dict((letter, 1 << n) for n, letter in enumerate("".join(cnts)))
R = dict((v, k) for (k, v) in M.items())

# Calculating bit masks and filtering anagrams
BitMasks = defaultdict(set)
for word in lex:
    bm = 0
    for letter in word:
        bm |= M[letter]
    BitMasks[bm].add(word)
# putting words with uncommon letters first. This speeds up the search
L = sorted(BitMasks.keys(), reverse=True)
# Now start looking
s = 0
N = len(L)
start = perf_counter()
stamp = perf_counter()
for n1 in range(N - 4):
    for n2 in range(n1 + 1, N - 3):
        if (L[n1] & L[n2]) == 0:
            for n3 in range(n2 + 1, N - 2):
                if (L[n1] & L[n3]) == 0 and (L[n2] & L[n3]) == 0:
                    for n4 in range(n3 + 1, N - 1):
                        if (
                            (L[n1] & L[n4]) == 0
                            and (L[n2] & L[n4]) == 0
                            and (L[n3] & L[n4]) == 0
                        ):
                            for n5 in range(n4 + 1, N):
                                if (
                                    (L[n1] & L[n5]) == 0
                                    and (L[n2] & L[n5]) == 0
                                    and (L[n3] & L[n5]) == 0
                                    and (L[n4] & L[n5]) == 0
                                ):
                                    s += 1
                                    print(
                                        f"\nSolution {s:3d} after {perf_counter()-stamp:.3f}:\n"
                                        f"{BitMasks[L[n1]]}\t{BitMasks[L[n2]]}"
                                        f"\t{BitMasks[L[n3]]}\t{BitMasks[L[n4]]}\t{BitMasks[L[n5]]}"
                                    )
                                    print(
                                        f"Excluded from clique: {R[((1<<26)-1)^(L[n1] | L[n2] | L[n3] | L[n4] | L[n5])]}"
                                    )
                                    stamp = perf_counter()
print(f"\n{s} solutions found in {perf_counter()-start:.3f}.\n")
