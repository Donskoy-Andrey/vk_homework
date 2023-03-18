from typing import IO, List


def searcher(file: str | IO, wordlist: List[str]) -> str:
    clear_wordlist = {word.lower() for word in wordlist}

    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_object:
            for line in file_object.readlines():
                words_in_line = {word.lower().strip() for word in line.split()}
                if len(clear_wordlist & words_in_line) != 0:
                    yield line

    else:
        for line in file:
            words_in_line = {word.lower().strip() for word in line.split()}
            if len(clear_wordlist & words_in_line) != 0:
                yield line
