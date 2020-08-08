import click
import requests
from peewee import OperationalError

from person_service import PersonService


@click.group()
def commands():
    pass


@commands.command(name='info', help="About program")
def info():
    print("A program about randomly generated persons data")


@commands.command(name='clear', help="Remove persons from database")
def clear_db():
    print("Clearing db")
    PersonService.drop_persons()


@commands.command(name='load', help="Load persons into database")
@click.argument('count', type=int, default=20)
def load_persons(count):
    print("Downloading")
    try:
        persons = PersonService.load_persons(count)
    except requests.exceptions.ConnectionError:
        print("Could not download due to connection error.")
    else:
        print('Inserting persons into db')
        PersonService.insert_persons(persons)
        print('Done, downloaded {} new persons'.format(len(persons)))


@commands.command(name='list', help="List persons")
@click.argument('count', type=int, default=10)
def list_persons(count):
    print("Reading persons")
    try:
        persons = PersonService.get_persons(count)
        for p in persons:
            print(p.name_first, p.name_last, p.gender, p.dob_age)
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='gender-percentage', help="Count percentage")
@click.argument('gender', type=click.Choice(['male', 'female']))
def gender_percentage(gender):
    try:
        print("{}: {}%".format(gender, PersonService.get_gender_percentage(gender)))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='average-age', help="Count average age of men or women or general (by default)")
@click.argument('gender', default='all', type=click.Choice(['male', 'female', 'all']))
def gender_avg_age(gender):
    try:
        print("{}: {}".format(gender, PersonService.get_avg_age(gender)))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='most-common-cities', help="Show most common cities and number of its occurrences")
@click.argument('n', default='1', type=int)
def most_common_cities(n):
    try:
        results = PersonService.most_common('cities', n)
        for r in results:
            print("{}, {}".format(r.location_city, r.occur))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='most-common-passwords', help="Show most common passwords and number of its occurrences")
@click.argument('n', default='1', type=int)
def most_common_passwords(n):
    try:
        results = PersonService.most_common('passwords', n)
        for r in results:
            print("{}, {}".format(r.login_password, r.occur))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='born', help="List persons born between given dates")
@click.argument('date_from', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.argument('date_to', type=click.DateTime(formats=["%Y-%m-%d"]))
def get_persons_born(date_from, date_to):
    try:
        persons = PersonService.born_between(date_from, date_to)
        for p in persons:
            print("{} {}, born: {}".format(p.name_first, p.name_last, p.dob_date))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='safest-password', help="Show safest password")
def safest_password():
    try:
        res = PersonService.get_safest_pswd()
        print(res.login_password, res.sum_val)
    except OperationalError:
        print('Database is empty please download some persons first')


if __name__ == '__main__':
    commands()
