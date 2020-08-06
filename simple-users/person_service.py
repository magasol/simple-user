import json

import requests
from peewee import fn, SQL

from models import Person, PersonUnion
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

    def get_safest_pswd(self):
        query_upper_letter = self.prepare_sf_subquery('p1', '2', '*[A-Z]*')
        query_lower_letter = self.prepare_sf_subquery('p2', '1', '*[a-z]*')
        query_number = self.prepare_sf_subquery('p3', '1', '*[0-9]*')
        query_length_min8 = self.prepare_sf_subquery('p4', '5', '????????*')

        # TODO add symbol check

        query_union = query_upper_letter + query_lower_letter + query_number + query_length_min8

        PersonUnion.create_table()
        PersonUnion\
            .insert_from(query_union, [PersonUnion.val, PersonUnion.login_password, PersonUnion.login_uuid])\
            .execute()

        res = PersonUnion \
            .select(fn.sum(PersonUnion.val).alias('sum_val'),
                    PersonUnion.login_password.alias('pswd'),
                    PersonUnion.login_uuid) \
            .group_by(PersonUnion.login_uuid) \
            .order_by(SQL('sum_val').desc()) \
            .peek()

        PersonUnion.drop_table()

        return res

    def prepare_sf_subquery(self, alias, val, pattern):
        p = Person.alias(alias)
        return p.select(SQL(val).alias('val'), p.login_password, p.login_uuid) \
            .where(p.login_password % pattern)
