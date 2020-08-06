import json

import requests
from peewee import fn, SQL

from models import Person
from person_factory import PersonFactory


class PersonService:

    def load_persons(self, count):
        response = requests.get('https://randomuser.me/api/?results={}'.format(count))
        return json.loads(response.text)['results']

    def drop_persons(self):
        Person.drop_table()

    def get_persons(self, count):
        results = Person.select().limit(count)
        return results

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

    def born_between(self, date_from, date_to):
        results = Person.select().where(Person.dob_date.between(date_from, date_to))
        return results

    def insert_persons(self, persons):
        print('Inserting persons into db')
        Person.create_table()
        for p in persons:
            pf = PersonFactory()
            p = pf.create_from_json(p)
            p.save()
        print('Done, downloaded {} new persons'.format(len(persons)))
