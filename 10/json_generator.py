import random
import sys
from faker import Faker


SEED = 42
FILESIZE = int(sys.argv[1])

def main():
    Faker.seed(SEED)
    fake = Faker(locale="Ru_ru")

    # Clear File if exists
    open("json_database.txt", "w").close()

    with open(file="json_database.txt", mode="w", encoding="utf-8") as file:
        for _ in range(FILESIZE):
            data = {
                "name": fake.name(),
                "sex": random.randint(0, 1),
                "age": random.randint(18, 70),
                "number": fake.phone_number(),
                "address": fake.address(),
                'company': fake.company(),
                "country": fake.country(),
            }

            json_str = "{" + f"\"name\": \"{data['name']}\", " \
                        f"\"number\": \"{data['number']}\"," \
                        f"\"sex\": {data['sex']},"\
                        f"\"age\": {data['age']}," \
                        f"\"address\": \"{data['address']}\"," \
                       f"\"company\": \"{data['company']}\"," \
                       f"\"country\": \"{data['country']}\"" \
                       + "}\n"
            file.write(json_str)

if __name__ == "__main__":
    main()