import argparse
import socket
import threading
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
en_stops = set(stopwords.words('english'))

TIMELIMIT = 10
urls_counter = 0


class Worker(threading.Thread):
    def __init__(self, target, args):
        super().__init__(target=target, args=args)


def parse_url(conn, top_size: int):
    global urls_counter
    urls_counter += 1
    url = conn.recv(1024).decode()
    print(f"Server read: {url}\nNumber of processed URL: {urls_counter}\n")

    html = requests.get(url=url).text
    text = BeautifulSoup(html, "lxml").text
    words = re.sub(r"<.*?>", "", text)
    words = re.sub(rf"[^a-zA-Z\s]+", "", words)
    words = words.split()
    words = [word for word in words if word.lower() not in en_stops]

    top_words = dict(
        Counter(words).most_common(top_size)
    )
    conn.send(f"{url}: {top_words}.\n".encode('utf-8'))
    conn.close()


class Master:
    def __init__(self, workers_count: int, top_size: int):
        self.workers_count = workers_count
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.settimeout(TIMELIMIT)
        self.server.bind(("127.0.0.1", 8080))
        self.server.listen(5)
        self.top_size = top_size

    def start_server(self):
        while True:
            for worker_index in range(self.workers_count):
                conn, address = self.server.accept()

                worker = Worker(
                    target=parse_url, args=(conn, self.top_size)
                )
                worker.start()

    def close(self):
        self.server.close()


def main():
    parser = argparse.ArgumentParser(description="server script")
    parser.add_argument("-w", dest="workers_count", default=5, type=int)
    parser.add_argument("-k", dest="top_size", default=5, type=int)
    args = parser.parse_args()
    workers_count = args.workers_count
    top_size = args.top_size

    server = Master(workers_count, top_size)

    try:
        server.start_server()
    except TimeoutError as err:
        print("Time limit. Server stopped.")
        global urls_counter
        urls_counter = 0
    finally:
        server.close()


if __name__ == "__main__":
    main()
