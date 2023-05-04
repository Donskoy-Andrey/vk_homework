import unittest
from unittest import mock
from fetcher import fetch_url, fetch_batch
import aiohttp
import asyncio


class TestFetcher(unittest.TestCase):
    def setUp(self):
        self.url = "https://google.com"
        self.html = b"<html><body><p>This is a super test test</p></body></html>"
        self.file = "urls_small.txt"

    async def run_test_fetch_url(self):
        with mock.patch.object(aiohttp.ClientSession, 'get') as mock_get:
            mock_resp = mock.Mock()
            mock_resp.read.return_value = asyncio.to_thread(lambda: self.html)

            mock_get.return_value.__aenter__.return_value = mock_resp

            result = await fetch_url(self.url, asyncio.Semaphore(1))

            expected_result = {
                self.url:
                {"test": 2, "super": 1}
            }

            self.assertEqual(result, f"{expected_result}")

    async def run_test_fetch_batch(self):
        with mock.patch.object(aiohttp.ClientSession, 'get') as mock_get:
            mock_resp = mock.Mock()
            mock_resp.read.return_value = asyncio.to_thread(lambda: self.html)

            mock_get.return_value.__aenter__.return_value = mock_resp
            callback_mock = mock.Mock()

            result = await fetch_batch(self.file, asyncio.Semaphore(1), callback_mock)

            expected_result = {
                "https://en.wikipedia.org/wiki/SEEPZ":
                {"test": 2, "super": 1}
            }

            callback_mock.assert_called_once_with(f"{expected_result}")

    def test_fetch_url(self):
        asyncio.run(self.run_test_fetch_url())

    def test_fetch_batch(self):
        asyncio.run(self.run_test_fetch_batch())
