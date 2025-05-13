# algorithms/backtracking.py

def solve(letters, dictionary):
    found_words = set()
    used = [False] * len(letters)  # Track used letters
    
    def backtrack(path):
        word = ''.join(path)
        if len(word) >= 2 and word in dictionary:
            found_words.add(word)
        
        for i in range(len(letters)):
            if not used[i]:
                used[i] = True
                path.append(letters[i])
                backtrack(path)   # Recursively explore further
                path.pop()        # Undo the last choice (backtrack)
                used[i] = False
    
    backtrack([])  # Start with an empty path
    return found_words
