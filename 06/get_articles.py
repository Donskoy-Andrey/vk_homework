import requests

open("urls.txt", "w").close()  # Clean file
PAGES = 100

with open("urls.txt", "a") as file:
    for page_index in range(PAGES):
        print(f"Page {page_index} from {PAGES}.")
        page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        file.write(f"{page.url}\n")
