from collections import UserDict
from datetime import datetime
import re

class Name():
    def __init__(self, value):
        if value is None or str(value).strip() == '':
            raise ValueError('Name.Required')

        self.__value = str(value)

    def __str__(self):
        return self.__value

class Phone():
    def __init__(self, value):
        value = str(value)

        if not value.isdigit():
            raise ValueError("Phone.NotNumeric")

        if len(value) != 10:
            raise ValueError('Phone.LengthMustBe10')

        self.__value = str(value)

    def __str__(self):
        return self.__value

class Birthday():
    def __init__(self, value):
        try:
            self.__value = datetime.strptime(str(value).strip(), "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday.Invalid")

    def compare(self, other):
        if isinstance(other, Birthday):
            return self.__value - other.__value
        else:
            raise ValueError("Birthday.ValueMustBeBirthday")

    def replace_year(self, year):
        if isinstance(year, int):
            return self.__value.replace(year=year)
        else:
            raise ValueError("Birthday.YearMustBeInt")

    def __str__(self):
        return str(self.__value.strftime("%d.%m.%Y"))

class Email():
    def __init__(self, value):
        if value is None or str(value).strip() == '':
            raise ValueError('Email.Required')

        if not re.match("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", value):
            raise ValueError('Email.Invalid')
        
        self.__value = str(value)

    def __str__(self):
        return self.__value
 
class Address():
    def __init__(self, value):
        if value is None or str(value).strip() == '':
            raise ValueError('Address.Required')

        self.__value = str(value)

    def __str__(self):
        return self.__value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.email = None
        self.address = None
        self.phones = []

    def __str__(self):
        result = f"Name: {str(self.name)}"

        if self.email is not None:
            result += f"\r\nEmail: {self.email}"

        if self.birthday is not None:
            result += f"\r\nBirthday: {self.birthday}"

        if self.address is not None:
            result += f"\r\nAddress: {self.address}"

        if len(self.phones) > 0:
            result += f"\r\nPhones: {'; '.join(str(p) for p in self.phones)}"

        return result

class AddressBook(UserDict):
    pass