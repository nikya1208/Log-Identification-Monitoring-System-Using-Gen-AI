# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\utils\trie.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class LogTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, message):
        node = self.root
        for char in message:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, message):
        node = self.root
        for char in message:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
