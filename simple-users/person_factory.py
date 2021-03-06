from datetime import datetime

from models import Person


class PersonFactory:
    def __init__(self):
        self.json = None

    def create_from_json(self, json):
        self.json = json
        self._adjust()
        return Person(
            gender=json['gender'],
            name_title=json['name']['title'],
            name_first=json['name']['first'],
            name_last=json['name']['last'],
            location_street=json['location']['street'],
            location_city=json['location']['city'],
            location_state=json['location']['state'],
            location_postcode=json['location']['postcode'],
            location_coordinates=json['location']['coordinates'],
            location_timezone=json['location']['timezone'],
            email=json['email'],
            login_uuid=json['login']['uuid'],
            login_username=json['login']['username'],
            login_password=json['login']['password'],
            login_salt=json['login']['salt'],
            login_md5=json['login']['md5'],
            login_sha1=json['login']['sha1'],
            login_sha256=json['login']['sha256'],
            dob_date=json['dob']['date'],
            dob_age=json['dob']['age'],
            registered_date=json['registered']['date'],
            registered_age=json['registered']['age'],
            phone=json['phone'],
            cell=json['cell'],
            id_name=json['id']['name'],
            id_value=json['id']['value'],
            next_birthday=json['next_birthday']
        )

    def _adjust(self):
        self.json.pop('picture')
        symbols = '!"#$%&\'()*+,- ./:;<=>?@\^_`{|}~[\]'
        self.json['cell'] = self.json['cell'].translate({ord(i): None for i in symbols})
        self.json['phone'] = self.json['phone'].translate({ord(i): None for i in symbols})
        try:
            self.json['next_birthday'] = (
                        datetime.strptime(self.json['dob']['date'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                            year=datetime.now().year + 1) - datetime.now()).days
        except ValueError:
            self.json['next_birthday'] = None
