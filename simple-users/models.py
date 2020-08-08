from peewee import *

db = SqliteDatabase('persons.db')


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    gender = TextField()
    name_title = TextField()
    name_first = TextField()
    name_last = TextField()
    location_street = TextField()
    location_city = TextField()
    location_state = TextField()
    location_postcode = TextField()
    location_coordinates = TextField()
    location_timezone = TextField()
    email = TextField()
    login_uuid = TextField()
    login_username = TextField()
    login_password = TextField()
    login_salt = TextField()
    login_md5 = TextField()
    login_sha1 = TextField()
    login_sha256 = TextField()
    dob_date = DateTimeField()
    dob_age = SmallIntegerField()
    registered_date = DateTimeField()
    registered_age = SmallIntegerField()
    phone = TextField()
    cell = TextField()
    id_name = TextField()
    id_value = TextField(null=True)
    next_birthday = SmallIntegerField(null=True)


class PersonUnion(BaseModel):
    login_uuid = TextField()
    login_password = TextField()
    val = TextField()
