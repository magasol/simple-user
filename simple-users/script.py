import click
from peewee import OperationalError

from person_service import PersonService

ps = PersonService()


@click.group()
def commands():
    pass


@commands.command(name='info', help="About program")
def info():
    click.echo("A program about randomly generated persons data")


@commands.command(name='clear', help="Clear entire database")
def clear_db():
    print("Clearing db")
    ps.drop_persons()


@commands.command(name='load', help="Load persons into database")
@click.argument('count', type=int, default=20)
def load_persons(count):
    print("Downloading")
    persons = ps.load_persons(count)
    ps.insert_persons(persons)


@commands.command(name='list', help="List persons")
@click.argument('count', type=int, default=10)
def list_persons(count):
    print("Raading persons")
    try:
        print(ps.get_persons(count))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='gender-percentage', help="Count percentage")
@click.argument('gender', type=click.Choice(['male', 'female']))
def gender_percentage(gender):
    try:
        print("{}: {}%".format(gender, ps.get_gender_percentage(gender)))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='average-age', help="Count average age of men or women or general (by default)")
@click.argument('gender', default='all', type=click.Choice(['male', 'female', 'all']))
def gender_avg_age(gender):
    try:
        print("{}: {}".format(gender, ps.get_avg_age(gender)))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='most-common-cities', help="Show most common cities and number of its occurrences")
@click.argument('n', default='1', type=int)
def most_common_cities(n):
    try:
        results = ps.most_common('cities', n)
        for r in results:
            print("{}, {}".format(r.city_name, r.occur))
    except OperationalError:
        print('Database is empty please download some persons first')


@commands.command(name='most-common-passwords', help="Show most common passwords and number of its occurrences")
@click.argument('n', default='1', type=int)
def most_common_passwords(n):
    try:
        results = ps.most_common('passwords', n)
        for r in results:
            print("{}, {}".format(r.pswd, r.occur))
    except OperationalError:
        print('Database is empty please download some persons first')


if __name__ == '__main__':
    commands()
