import json
from datetime import datetime

import requests
from peewee import OperationalError

from models import Person


class PersonService:

    def load_persons(self, count):
        response = requests.get('https://randomuser.me/api/?results={}'.format(count))
        return json.loads(response.text)['results']

    def drop_persons(self):
        Person.drop_table()

    def get_persons(self, count):
        try:
            query = Person.select().limit(count)
            return [person.name_first + ' ' + person.name_last for person in query]
        except OperationalError:
            print('Database is empty please download some persons first')

    def insert_persons(self, persons):
        print('Inserting persons into db')
        Person.create_table()
        for p in persons:
            p = self.parse_person(p)
            p.save()
        print('Done, downloaded {} new persons'.format(len(persons)))

    def parse_person(self, person):
        self.adjust(person)
        return Person(
            gender=person['gender'],
            name_title=person['name']['title'],
            name_first=person['name']['first'],
            name_last=person['name']['last'],
            location_street=person['location']['street'],
            location_city=person['location']['city'],
            location_state=person['location']['state'],
            location_postcode=person['location']['postcode'],
            location_coordinates=person['location']['coordinates'],
            location_timezone=person['location']['timezone'],
            email=person['email'],
            login=person['login'],
            dob_date=person['dob']['date'],
            dob_age=person['dob']['age'],
            registered_date=person['registered']['date'],
            registered_age=person['registered']['age'],
            phone=person['phone'],
            cell=person['cell'],
            id_name=person['id']['name'],
            id_value=person['id']['value'],
            next_birthday=person['next_birthday']
        )

    def adjust(self, person):
        person.pop('picture')
        symbols = '!@#$%^&*()_-+={[}]:;\'\'<,>.?/\\| '
        person['cell'] = person['cell'].translate({ord(i): None for i in symbols})
        person['phone'] = person['phone'].translate({ord(i): None for i in symbols})
        try:
            person['next_birthday'] = (datetime.strptime(person['dob']['date'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                year=datetime.now().year + 1) - datetime.now()).days
        except ValueError:
            person['next_birthday'] = None
