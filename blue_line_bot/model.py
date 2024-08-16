from collections import UserDict
from datetime import datetime, timedelta
import re


class Name():
    def __init__(self, value):
        if value is None or str(value).strip() == '':
            raise ValueError('Name.Required')

        self.__value = str(value).strip()

    def __str__(self):
        return self.__value


class Phone():
    def __init__(self, value):
        value = str(value).strip()

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
            self.__value = datetime.strptime(
                str(value).strip(), "%d.%m.%Y"
            ).date()
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
    # RFC 5322 compliant regex, which allows
    # both domain-based and IP-address based emails
    EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    
    def __init__(self, value):
        if value is None or str(value).strip() == '':
            raise ValueError('Email.Required')

        if not re.match(self.EMAIL_REGEX, value):
            raise ValueError('Email.Invalid')

        self.__value = str(value).strip()

    def __str__(self):
        return self.__value


class Address():
    def __init__(self, value):
        if value is None or str(value).strip() == '':
            raise ValueError('Address.Required')

        self.__value = str(value).strip()

    def __str__(self):
        return self.__value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.email = None
        self.address = None
        self.phones = []

    # region Phone
    
    # Create
    def add_phone(self, phone):
        if self.find_phone(phone) is not None:
            raise ValueError("Record.PhoneDuplicate")

        self.phones.append(Phone(phone))

    # Read
    def get_phones(self):
        return ', '.join(str(p) for p in self.phones)

    # Update
    def edit_phone(self, old_phone, new_phone):
        _ = Phone(old_phone)  # just to validate
        new_phone = Phone(new_phone)

        if self.find_phone(old_phone) is None:
            raise ValueError("Record.PhoneNotFound")

        if self.find_phone(new_phone) is not None:
            raise ValueError("Record.PhoneDuplicate")

        # Look for matching phone number and edit it
        i = 0
        while i < len(self.phones):
            if str(self.phones[i]) == old_phone:
                self.phones[i] = new_phone
                break
            i += 1

    # Delete
    def remove_phone(self, phone):
        phone = self.find_phone(phone)

        if phone is None:
            raise ValueError("Record.PhoneNotFound")
        else:
            self.phones.remove(phone)

    # Internal helper method
    def find_phone(self, lookup_phone):
        for phone in self.phones:
            if str(phone) == lookup_phone:
                return phone

        return None
    # endregion

    # region Birthday
    # Create/update
    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # Read
    def get_birthday(self):
        return str(self.birthday)

    # Delete
    def remove_birthday(self):
        self.birthday = None
    # endregion

    # region Email
    # Create/update
    def set_email(self, email):
        self.email = Email(email)

    # Read
    def get_email(self):
        return str(self.email)

    # Delete
    def remove_email(self):
        self.email = None
    # endregion

    # region Address
    # Create/update
    def set_address(self, address):
        self.address = Address(address)

    # Read
    def get_address(self):
        return str(self.address)

    # Delete
    def remove_address(self):
        self.address = None
    # endregion

    # Simple formatting of the whole record for pretty output
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
    # Create
    def add_record(self, record):
        if record.name in self.data:
            raise ValueError('AddressBook.DuplicateName')

        if isinstance(record, Record):
            self.data[str(record.name)] = record
        else:
            raise ValueError("AddressBook.ValueMustBeRecord")

    # Read
    def find(self, field, value):
        result = None
        if field == "name":
            if value in self.data:
                result = self.data[value]
        elif field == "email":
            for record in self.values():
                if str(record.email) == value:
                    result = value
        elif field == "phone":
            for record in self.values():
                if str(record.find_phone(value)) != None:
                    result = value
        elif field == "birthday":
            for record in self.values():
                if str(record.birthday) == value:
                    result = value
        elif field == "address":
            for record in self.values():
                if str(record.address) == value:
                    result = value
        else:
            raise ValueError('AddressBook.WrongSearchField')

        if result is None:
            raise ValueError('AddressBook.NotFound')

        return result

    def find_many(self, field, value):
        result = []
        value = value.lower()
        if field == "name":
            for record in self.values():
                if value in str(record.name).lower():
                    result.append(record)
        elif field == "email":
            for record in self.values():
                if value in str(record.email).lower():
                    result.append(record)
        elif field == "phone":
            for record in self.values():
                if record.find_phone(value) != None:
                    result.append(record)
        elif field == "birthday":
            for record in self.values():
                if value in str(record.birthday):
                    result.append(record)
        elif field == "address":
            for record in self.values():
                if value in str(record.address).lower():
                    result.append(record)
        else:
            raise ValueError("AddressBook.WrongSearchField")

        return result

    # Delete
    def remove(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            raise ValueError('AddressBook.NotFound')

    def get_upcoming_birthdays(self, days=7):
        if not isinstance(days, int):
            raise ValueError("AddressBook.DaysMustBeInt")

        today = datetime.today().date()
        upcoming_birthdays = []

        # For simplicity, replace year of birthday with current year and
        # then see if it is within the given days
        for name in self.data:
            birthday = self.data[name].birthday
            if birthday is None:
                continue
            birthday_this_year = birthday.replace_year(today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace_year(today.year + 1)

            delta_days = (birthday_this_year - today).days

            if 0 <= delta_days <= days:
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year += timedelta(
                        days=(7 - birthday_this_year.weekday()))

                upcoming_birthdays.append({
                    'name': name,
                    'congratulation_date': birthday_this_year.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays


class Note:
    def __init__(self, title, note, tags=[]):
        self.title = title
        self.note = note
        self.tags = tags

    def add_tag(self, tag):
        self.tags.append(tag)
        self.tags = sorted(self.tags)

    def __str__(self):
        return f"Title: {self.title}\r\nTags: {self.tags}\r\nNote: {self.note}"


class NoteBook(UserDict):
    # Create
    def add_note(self, note):
        if note.title in self.data:
            raise ValueError('NoteBook.DuplicateTitle')

        if isinstance(note, Note):
            self.data[str(note.title)] = note
        else:
            raise ValueError("NoteBook.ValueMustBeNote")

    # Read
    def find(self, field, value):
        # Search notes by either title, contents or tags
        # Use exact match for title,
        # but partial match for content and tags
        # (search query is part of note content, or tag is one of the tags)
        result = None
        if field == "title":
            if value in self.data:
                result = self.data[value]
        elif field == "note":
            for note in self.values():
                if value in str(note.note):
                    result = note
        elif field == "tags":
            for note in self.values():
                if value in note.tags:
                    result = note
        else:
            raise ValueError()

        if result is None:
            raise ValueError('NoteBook.NotFound')
        return result

    # Delete
    def remove(self, title):
        if title in self.data:
            self.data.pop(title)
        else:
            raise ValueError('NoteBook.NotFound')
