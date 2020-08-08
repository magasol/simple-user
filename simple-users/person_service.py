import json
import random

import requests
from peewee import fn, SQL

from models import Person, PersonUnion
from person_factory import PersonFactory


class PersonService:

    @staticmethod
    def load_persons(count):
        extras = PersonService._rand_pwd_extras()
        response = requests.get('https://randomuser.me/api/?results={}&password={}3-15'
                                .format(count, extras))
        return json.loads(response.text)['results']

    @staticmethod
    def insert_persons(persons):
        Person.create_table()
        pf = PersonFactory()
        for p in persons:
            p = pf.create_from_json(p)
            p.save()

    @staticmethod
    def drop_persons():
        Person.drop_table()

    @staticmethod
    def get_persons(count):
        results = Person.select().limit(count)
        return results

    @staticmethod
    def get_gender_percentage(gender):
        gender_res = Person.select(fn.COUNT(Person.gender).alias('count')) \
            .where(Person.gender == gender).get()
        persons_res = Person.select(fn.COUNT(Person.gender).alias('count')).get()
        gender_percentage = gender_res.count / persons_res.count * 100
        return gender_percentage

    @staticmethod
    def get_avg_age(gender):
        if gender == 'all':
            res = Person.select(fn.AVG(Person.dob_age).alias('avg_age')).get()
            return res.avg_age
        else:
            res = Person.select(fn.AVG(Person.dob_age).alias('avg_age')) \
                .where(Person.gender == gender).get()
            return res.avg_age

    @staticmethod
    def most_common(col, n):
        if col == 'cities':
            col_name = Person.location_city
        else:
            col_name = Person.login_password

        results = Person.select(col_name, fn.COUNT(col_name).alias('occur')) \
            .group_by(col_name).order_by(SQL('occur').desc()).limit(n)
        return results

    @staticmethod
    def born_between(date_from, date_to):
        results = Person.select().where(Person.dob_date.between(date_from, date_to))
        return results

    @staticmethod
    def get_safest_pswd():
        query_upper_letter = PersonService._prepare_sp_subquery('2', '*[A-Z]*')
        query_lower_letter = PersonService._prepare_sp_subquery('1', '*[a-z]*')
        query_number = PersonService._prepare_sp_subquery('1', '*[0-9]*')
        query_length_min8 = PersonService._prepare_sp_subquery('5', '????????*')
        query_symbol = PersonService._prepare_sp_subquery('3', '*[!"#$%&\'()*+,- ./:;<=>?@\^_`{|}~[\]*')

        query_union = query_upper_letter + query_lower_letter + query_number \
                      + query_length_min8 + query_symbol

        res = PersonService._use_tmp_personunion(query_union)

        return res

    @staticmethod
    def _rand_pwd_extras():
        extras = ''
        for item in ['special,', 'upper,', 'lower,', 'number,']:
            extras += PersonService._rand_add_extra(item)
        return extras

    @staticmethod
    def _rand_add_extra(item):
        r = random.randint(0, 4)
        if r % 4 == 0:
            return item
        else:
            return ''

    @staticmethod
    def _prepare_sp_subquery(val, pattern):
        return Person.select(SQL(val).alias('val'), Person.login_password, Person.login_uuid) \
            .where(Person.login_password % pattern)

    @staticmethod
    def _use_tmp_personunion(query_union):
        PersonUnion.create_table()
        PersonUnion \
            .insert_from(query_union, [PersonUnion.val, PersonUnion.login_password, PersonUnion.login_uuid]) \
            .execute()

        res = PersonUnion \
            .select(fn.sum(PersonUnion.val).alias('sum_val'),
                    PersonUnion.login_password,
                    PersonUnion.login_uuid) \
            .group_by(PersonUnion.login_uuid) \
            .order_by(SQL('sum_val').desc()) \
            .peek()

        PersonUnion.drop_table()

        return res
