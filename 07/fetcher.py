import re
import sys
import argparse
from typing import Callable
from collections import Counter

import aiohttp
import asyncio

from nltk.corpus import stopwords


TOP_SIZE: int = 5
en_stops = {*stopwords.words('english'), "hlist", "wikipedia"}


async def fetch_url(url: str, semaphore: asyncio.locks.Semaphore):
    async with aiohttp.ClientSession() as session:
        async with semaphore:
            async with session.get(url) as resp:
                text = await resp.read()
                text = text.decode()

                words = re.sub(r"<.*?>", "", text)
                words = re.sub(rf"[^a-zA-Z\s]+", "", words)
                words = words.split()
                words = [word for word in words if word.lower() not in en_stops]

                top_words = dict(
                    Counter(words).most_common(TOP_SIZE)
                )

                return "{" + f"'{url}': {top_words}" + "}"


async def fetch_batch(file: str, semaphore: asyncio.locks.Semaphore, callback: Callable = print):
    tasks = []
    with open(file, "r") as file:
        for url in file:
            tasks.append(asyncio.create_task(fetch_url(url.strip(), semaphore)))

            result = await asyncio.gather(*tasks)
            callback(result[-1])
    return result


def main():
    if sys.argv[1] == "-c":
        parser = argparse.ArgumentParser(description="fetcher script")
        parser.add_argument("-c", dest="workers_count", default=1, type=int)
        parser.add_argument("file", default="urls.txt", type=str)
        args = parser.parse_args()
        workers_count = args.workers_count
        file = args.file
    else:
        workers_count = int(sys.argv[1])
        file = sys.argv[2]

    semaphore = asyncio.Semaphore(workers_count)
    asyncio.run(fetch_batch(file, semaphore))


if __name__ == '__main__':
    main()
