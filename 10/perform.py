import time
import json
import ujson
import cjson


def main():
    for package in [json, ujson, cjson]:
        loads = package.loads
        dumps = package.dumps

        with open(file="json_database.txt", mode="r", encoding="utf-8") as file:
            loading_time = 0
            dumping_time = 0
            for line in file:
                line = line.strip()

                start = time.time()
                tmp = loads(line)
                loading_time += time.time() - start

                start = time.time()
                dumps(tmp)
                dumping_time += time.time() - start
            print(
                f"{package.__name__}: \t loading time: {loading_time: .3f}s \t dumping time: {dumping_time: .3f}s"
            )

if __name__ == "__main__":
    main()
