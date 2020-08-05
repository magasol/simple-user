from datetime import datetime


class Person:
    _symbols = '!@#$%^&*()_-+={[}]:;\"\'<,>.?/\\| '

    def __init__(self, data):
        self.data = data

    def adjust(self):
        self.data.pop('picture')
        self.data['cell'] = self.data['cell'].translate({ord(i): None for i in self._symbols})
        self.data['phone'] = self.data['phone'].translate({ord(i): None for i in self._symbols})
        self.data['next_birthday'] = (datetime.strptime(self.data['dob']['date'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(
            year=datetime.now().year + 1) - datetime.now()).days
