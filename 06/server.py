import argparse
import socket
import threading
import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
en_stops = set(stopwords.words('english'))

TIMELIMIT = 10


class Worker(threading.Thread):
    def __init__(self, target, args):
        super().__init__(target=target, args=args)


def parse_url(conn, top_size: int, cls: "Master", semaphore):
    with semaphore:
        sem = threading.Semaphore(1)
        with sem:
            cls.urls_counter += 1
        url = conn.recv(1024).decode()
        print(f"Server read: {url}\nNumber of processed URL: {cls.urls_counter}\n")

        try:
            html = requests.get(url=url, timeout=5).text
            text = BeautifulSoup(html, "lxml").text
            words = re.sub(r"<.*?>", "", text)
            words = re.sub(r"[^a-zA-Z\s]+", "", words)
            words = words.split()
            words = [word for word in words if word.lower() not in en_stops]

            top_words = dict(
                Counter(words).most_common(top_size)
            )
            conn.send(f"{url}: {top_words}.\n".encode('utf-8'))
            conn.close()
        except ImportError:
            print(f"Couldn't parse data from {url}.")
        except ValueError:
            print(f"Couldn't read data from {url}.")


class Master:
    def __init__(self, workers_count: int, top_size: int):
        self.workers_count = workers_count
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.settimeout(TIMELIMIT)
        self.server.bind(("127.0.0.1", 8080))
        self.server.listen(5)
        self.top_size = top_size
        self.urls_counter = 0

    def start_server(self):
        while True:
            semaphore = threading.Semaphore(
                self.workers_count
            )
            for _ in range(self.workers_count):
                conn, _ = self.server.accept()

                worker = Worker(
                    target=parse_url,
                    args=(
                        conn,
                        self.top_size,
                        self,
                        semaphore
                    )
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
    except TimeoutError as exs:
        server.close()
        raise KeyboardInterrupt("Time limit. Server stopped.") from exs


if __name__ == "__main__":
    main()
