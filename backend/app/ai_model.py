# # C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\ai_model.py
# from transformers import pipeline

# # Load AI model for anomaly detection
# anomaly_detector = pipeline("text-classification", model="distilbert-base-uncased")

# def detect_anomalies(log_message: str) -> bool:
#     result = anomaly_detector(log_message)
#     return result[0]["label"] == "ANOMALY"



# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\utils\trie.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class LogTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, message: str):
        node = self.root
        for char in message:
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True

    def search(self, message: str) -> bool:
        node = self.root
        for char in message:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
