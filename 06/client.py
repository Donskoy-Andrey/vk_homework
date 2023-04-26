import socket
import argparse
import threading
from server import TIMELIMIT


class Client:
    def __init__(self, threads: int = 10, urls_path: str = "urls.txt"):
        self.threads_count = threads  # amount of threads
        self.urls_path = urls_path  # file with urls

    def start_client(self):
        with open(self.urls_path, "r") as file:
            urls = [url.strip() for url in file.readlines()]

            chunk_size = len(urls) // self.threads_count
            url_chunks = [
                urls[i: i + chunk_size]
                for i in range(0, len(urls), chunk_size)
            ]
        self.run_threads(url_chunks)

    def run_threads(self, url_chunks: list):
        threads = []

        for thread_index in range(self.threads_count):
            threads.append(
                threading.Thread(
                    target=self.send_urls,
                    args=(url_chunks[thread_index],)
                )
            )

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    @staticmethod
    def send_url(url: str):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMELIMIT)
        client_socket.connect(("127.0.0.1", 8080))
        client_socket.send(url.encode('utf-8'))
        print(f'Client sent: {url}\n{client_socket.recv(1024).decode()}')
        client_socket.close()

    def send_urls(self, urls: list):
        for url in urls:
            self.send_url(url)


def main():
    parser = argparse.ArgumentParser(description="client script")
    parser.add_argument("-m", dest="threads", default=10, type=int)
    parser.add_argument("-u", dest="urls", default="urls.txt", type=str)
    args = parser.parse_args()
    threads = args.threads
    urls_path = args.urls_path

    client = Client(threads, urls_path)
    client.start_client()


if __name__ == '__main__':
    main()
