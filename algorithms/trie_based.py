# algorithms/trie_based.py

class TrieNode:
    def __init__(self):
        self.children = {}             # Dictionary of child nodes
        self.is_end_of_word = False    # Marks the end of a valid word

def build_trie(dictionary):
    root = TrieNode()
    for word in dictionary:
        node = root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end_of_word = True
    return root

def solve(letters, dictionary):
    found_words = set()
    trie_root = build_trie(dictionary)
    used = [False] * len(letters)
    
    def dfs(node, path):
        word = ''.join(path)
        if len(word) >= 2 and node.is_end_of_word:
            found_words.add(word)
        
        for i in range(len(letters)):
            if not used[i] and letters[i] in node.children:
                used[i] = True
                path.append(letters[i])
                dfs(node.children[letters[i]], path)
                path.pop()
                used[i] = False
    
    dfs(trie_root, [])
    return found_words
