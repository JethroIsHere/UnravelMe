# algorithms/brute_force.py
from itertools import permutations

def solve(letters, dictionary):
    found_words = set()            # Store unique valid words
    n = len(letters)               # Number of input letters
    
    # Loop over word lengths from 2 to n
    for length in range(2, n + 1):
        # Generate all permutations for this length
        for perm in permutations(letters, length):
            word = ''.join(perm)   # Join tuple into a string
            if word in dictionary: # Check if it's a valid word
                found_words.add(word)
    
    return found_words
