import shutil
from datetime import datetime

from person_service import PersonService


# The results are correct only for specially created database
def setup():
    shutil.copy2('./test_db/persons.db', '.')


def test_list_with_len_n_returned_when_load_persons_with_arg_n_called():
    n = 2
    res = PersonService.load_persons(n)
    assert len(res) == n


def test_n_rows_returned_when_get_persons_with_arg_n_called():
    n = 2
    res = PersonService.get_persons(n)
    res = list(r for r in res)
    assert len(res) == n


def test_correct_float_returned_when_get_gender_percentage_called_with_arg_female():
    res = PersonService.get_gender_percentage('female')
    assert res == 48.0


def test_correct_float_returned_when_get_gender_percentage_called_with_arg_male():
    res = PersonService.get_gender_percentage('male')
    assert res == 52.0


def test_correct_int_returned_when_get_avg_age_called_with_arg_all():
    res = PersonService.get_avg_age('all')
    assert res == 49


def test_correct_int_returned_when_get_avg_age_called_with_arg_female():
    res = PersonService.get_avg_age('female')
    assert res == 48


def test_correct_int_returned_when_get_avg_age_called_with_arg_male():
    res = PersonService.get_avg_age('male')
    assert res == 51


def test_n_rows_returned_when_most_common_called_with_arg_cities_n():
    n = 5
    res = PersonService.most_common('cities', n)
    res = list(r for r in res)
    assert len(res) == n


def test_n_rows_returned_when_most_common_called_with_arg_passwords_n():
    n = 5
    res = PersonService.most_common('passwords', n)
    res = list(r for r in res)
    assert len(res) == n


def test_n_rows_returned_when_born_beetween_called_with_valid_arg():
    n = 4
    from_date = datetime.strptime('1964-01-01', '%Y-%m-%d')
    to_date = datetime.strptime('1966-01-01', '%Y-%m-%d')
    res = PersonService.born_between(from_date, to_date)
    res = list(r for r in res)
    assert len(res) == n


def test_1_correct_row_returned_when_get_safest_pswd_called():
    res = PersonService.get_safest_pswd()
    assert res.login_password == 'kordell1'
    assert res.sum_val == 7
