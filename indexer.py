from collections import defaultdict
import threading


class Indexer:
    def __init__(self):
        self.index = defaultdict(list)
        self.lock = threading.Lock()

    def index_page(self, url, text):
        with self.lock:
            self.index[url] = text

    def search(self, keyword):
        with self.lock:
            return [url for url, text in self.index.items() if keyword.lower() in text.lower()][:10]
