import click

from person_service import PersonService


@click.group()
def commands():
    pass


@click.command(name='info', help="Test if commands are working")
def info():
    click.echo("A program about random persons")


@click.command(name='clear', help="Clear entire database")
def clear_db():
    print("Clearing db")
    ps = PersonService()
    ps.drop_persons()


@click.command(name='load', help="Load persons into database")
@click.option('--count', type=int, default=20, help="Number of new persons loaded")
def load_persons(count):
    print("Downloading")
    ps = PersonService()
    persons = ps.load_persons(count)
    ps.insert_persons(persons)


@click.command(name='list', help="List persons")
@click.option('--count', help="List all persons")
def list_persons(count):
    print("Raading persons")
    ps = PersonService()
    print(ps.get_persons(count))


commands.add_command(info)
commands.add_command(clear_db)
commands.add_command(load_persons)
commands.add_command(list_persons)
commands.add_command(list_persons)

if __name__ == '__main__':
    commands()
