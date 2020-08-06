import json
from datetime import datetime

import requests
from peewee import fn, SQL

from models import Person


class PersonService:

    def load_persons(self, count):
        response = requests.get('https://randomuser.me/api/?results={}'.format(count))
        return json.loads(response.text)['results']

    def drop_persons(self):
        Person.drop_table()

    def get_persons(self, count):
        results = Person.select().limit(count)
        return [person.name_first + ' ' + person.name_last
                + ' ' + person.gender + ' ' + str(person.dob_age) for person in results]

    def get_gender_percentage(self, gender):
        gender_res = Person.select(fn.COUNT(Person.gender).alias('count')) \
            .where(Person.gender == gender).get()
        persons_res = Person.select(fn.COUNT(Person.gender).alias('count')).get()
        gender_percentage = gender_res.count / persons_res.count * 100
        return gender_percentage

    def get_avg_age(self, gender):
        if gender == 'all':
            res = Person.select(fn.AVG(Person.dob_age).alias('avg_age')).get()
            return res.avg_age
        else:
            res = Person.select(fn.AVG(Person.dob_age).alias('avg_age')) \
                .where(Person.gender == gender).get()
            return res.avg_age

    def most_common(self, col, n):
        if col == 'cities':
            col_name_alias = 'city_name'
            col_name = Person.location_city
        else:
            col_name_alias = 'pswd'
            col_name = Person.login_password

        results = Person.select(col_name.alias(col_name_alias), fn.COUNT(col_name).alias('occur')) \
            .group_by(col_name).order_by(SQL('occur').desc()).limit(n)
        return results

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
            login_uuid=person['login']['uuid'],
            login_username=person['login']['username'],
            login_password=person['login']['password'],
            login_salt=person['login']['salt'],
            login_md5=person['login']['md5'],
            login_sha1=person['login']['sha1'],
            login_sha256=person['login']['sha256'],
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
