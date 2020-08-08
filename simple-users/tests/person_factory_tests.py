import shutil

from models import Person
from person_factory import PersonFactory
from person_service import PersonService


def setup():
    shutil.copy2('./test_db/persons.db', '.')


def test_person_model_returned_when_create_from_json_called_with_valid_arg():
    n = 1
    json = PersonService.load_persons(n)
    pf = PersonFactory()
    res = pf.create_from_json(json[0])
    assert type(res) == Person
