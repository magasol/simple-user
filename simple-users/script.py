import requests
import json

from person import Person


def load_persons():
    response = requests.get("https://randomuser.me/api/?results=100")
    persons = json.loads(response.text)['results']
    persons = list(Person(person) for person in persons)

    for person in persons:
        person.adjust()

    return persons


def list_persons():
    persons = load_persons()
    for i in persons: print(i.data)


if __name__ == '__main__':
    list_persons()
