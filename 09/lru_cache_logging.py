import logging
import argparse
from lru_cache import LRUCache


class CustomFilterEvenNumber(logging.Filter):
    """
    Leave logs with an even number of elements.
    """

    def filter(self, record):
        if len(record.getMessage()) % 2 == 0:
            return record
        return None


def logger_activate(stdout: bool, custom_filter: bool):
    logger = logging.getLogger()

    if stdout:
        formatter_to_stdout = logging.Formatter(
            "%(levelname)s\t : %(message)s"
        )

        handler_to_stdout = logging.StreamHandler()
        handler_to_stdout.setLevel(logging.DEBUG)
        handler_to_stdout.setFormatter(formatter_to_stdout)

        if custom_filter:
            handler_to_stdout.addFilter(CustomFilterEvenNumber())

        logger.addHandler(handler_to_stdout)
        logger.setLevel(logging.DEBUG)

    formatter_to_file = logging.Formatter(
        "%(levelname)s\t%(asctime)s : %(message)s"
    )

    handler_to_file = logging.FileHandler("lru.log")
    handler_to_file.setLevel(logging.DEBUG)
    handler_to_file.setFormatter(formatter_to_file)

    if custom_filter:
        handler_to_file.addFilter(CustomFilterEvenNumber())

    logger.addHandler(handler_to_file)
    logger.setLevel(logging.DEBUG)

    return logger


def main():
    parser = argparse.ArgumentParser(description="logger script")
    parser.add_argument(
        "-s", "--stdout", action="store_true",
        dest="stdout", help="log to the terminal"
    )
    parser.add_argument(
        "-f", "--filter", action="store_true",
        dest="filter", help="use specific filter"
    )

    arguments = parser.parse_args()
    use_filter = arguments.filter
    use_stdout = arguments.stdout

    logger = logger_activate(use_stdout, use_filter)

    lru = LRUCache(3, logger=logger)
    lru.set("k1", "val1")  # set отсутствующего ключа
    lru.set("k2", "val2")  # set отсутствующего ключа
    lru.set("k3", "val3")  # set отсутствующего ключа
    lru.set("k4", "val3")  # set отсутствующего ключа, когда достигнута ёмкость
    lru.set("k2", "new_val2")  # set существующего ключа

    lru.get("k1")  # get отсутствующего ключа
    lru.get("k2")  # get существующего ключа

    # lru.set([1, 2, 3], [1, 2, 3])  # error с нехэшируемым типом


if __name__ == "__main__":
    main()
