import unittest
from unittest import mock
from unittest.mock import call
from server import Master
from client import Client
import socket


class FakeGetResult:
    def __init__(self):
        self.text = r"<html>Hello world!<\html>"


class TestServer(unittest.TestCase):
    def setUp(self):
        self.url = "https://google.com"

    def test_server_initial_params(self):
        master = Master(workers_count=2, top_size=7)
        self.assertEqual(
            master.server.gettimeout(),
            10
        )
        self.assertEqual(
            master.server.getsockname(),
            ("127.0.0.1", 8080)
        )
        self.assertEqual(master.workers_count, 2)
        self.assertEqual(master.top_size, 7)

        master.close()

    def test_input_output(self):
        master = Master(workers_count=2, top_size=7)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(("127.0.0.1", 8080))
            client.send(self.url.encode('utf-8'))

            with mock.patch('server.print') as fake:
                with mock.patch("server.requests.get") as fake_get:
                    fake_get.return_value = FakeGetResult()
                    try:
                        master.start_server()
                    except Exception:
                        pass
                    finally:
                        self.assertEqual(
                            [call(f'Server read: {self.url}\nNumber of processed URL: 1\n')],
                            fake.call_args_list
                        )
        master.close()

    def test_timeout(self):
        master = Master(workers_count=2, top_size=7)
        with self.assertRaises(socket.timeout):
            master.start_server()
        master.close()


class TestClient(unittest.TestCase):

    def test_client_initial_params(self):
        client = Client()
        self.assertEqual(client.threads_count, 10)
        self.assertEqual(client.urls_path, "urls.txt")

    def test_extract_urls(self):
        client = Client(threads=1, urls_path="urls_small.txt")

        with mock.patch('client.Client.run_threads') as threads_fake:
            client.start_client()
            threads_fake.return_value = None

            self.assertEqual(
                [call([['https://en.wikipedia.org/wiki/SEEPZ']])],
                threads_fake.call_args_list
            )

    def test_extract_urls_txt(self):
        client = Client(threads=1, urls_path="urls.txt")

        with mock.patch('client.Client.run_threads') as threads_fake:
            client.start_client()
            threads_fake.return_value = None

            self.assertEqual(
                len(*threads_fake.call_args_list[0][0][0]),
                9
            )
