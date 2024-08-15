from model import AddressBook, Record, NoteBook, Note
import pickle

def error_decorator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            message = str(ex)
            if message == "Name.Required":
                return "Name can not be empty"
            elif message == "Phone.NotNumeric":
                return "Phone must be numeric"
            elif message == "Phone.LengthMustBe10":
                return "Phone lenght must be 10 digits"
            elif message == "Birthday.Invalid":
                return "Birthday should be in format d.m.Y (e.g. 27.1.2000)"
            elif message == "Email.Required":
                return "Email can not be empty"
            elif message == "Email.Invalid":
                return "Input a valid email"
            elif message == "Address.Required":
                return "Address can not be empty"
            elif message == "Record.PhoneDuplicate":
                return "This phone already exists in the record"
            elif message == "Record.PhoneNotFound":
                return "This phone does not exist in the record"
            elif message == "AddressBook.DuplicateName":
                return "This name is already exists in the address book"
            elif message == "AddressBook.NotFound":
                return "This value does not exist in the address book"
            elif message == "AddressBook.DaysMustBeInt":
                return "Days value should be integer"
            elif message == "NoteBook.NotFound":
                return "This value does not exist in the note book"
            elif message == "Birthdays.DaysMustBeNumeric":
                return "Days for birthdays must be numeric value"
            else:
                return "Input a valid command."
        except KeyError:
            return "Contact was not found"
        except IndexError:
            return "Give me contact name to return phone for, please."
        except IOError as ex:
            message = str(ex)
            if message == "IO.SaveFailed":
                return "Failed to save address book"
            elif message == "IO.LoadFailed":
                return "Failed to save address book"
            else:
                return "Oops... Something went wrong"
        except Exception as ex:
            print(ex)
            return "Oops... Something went wrong"

    return inner

@error_decorator
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@error_decorator
def add_contact(args, book: AddressBook):
    name, phone, email, birthday, *address_array = args + [None, None, None]
    address = " ".join(i for i in address_array if i is not None).strip()

    message = "Contact updated."
    record = None

    if name not in book:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
        
    if record is None:
        record = book.find("name", name)

    if phone:
        record.add_phone(phone)

    if email:
        record.set_email(email)

    if birthday:
        record.set_birthday(birthday)

    if address != '':
        record.set_address(address)

    return message

@error_decorator
def get_records(args, book):
    field, value = args
    records = book.find_many(field, value)

    if len(records) == 0:
        return "No contacts match the filter."

    result = ""
    for record in records:
        result += str(record) + "\r\n\r\n"

    return result.strip()

@error_decorator
def show_all(book):
    if len(book) == 0:
        return "Address book is empty."

    result = ""
    for record in book.values():
        result += f"{record}\r\n\r\n"
    return result.strip()

@error_decorator
def remove_record(args, book):
    name, *_ = args
    book.remove(name)
    return "Contact removed"

@error_decorator
def add_phone(args, book):
    name, phone = args
    book.find("name", name).add_phone(phone)

    return "Contact updated."

@error_decorator
def get_phones(args, book):
    name = args[0]
    record = book.find("name", name)
    
    if len(record.phones) == 0:
        return "This contact does not have phones."
    else:
        return record.get_phones()

@error_decorator
def change_phone(args, book):
    name, old_phone, new_phone = args
    book.find("name", name).edit_phone(old_phone, new_phone)

    return "Contact updated."

@error_decorator
def remove_phone(args, book):
    name, phone = args
    book.find("name", name).remove_phone(phone)

    return "Phone removed."

@error_decorator
def set_birthday(args, book):
    name, birthday = args
    book.find("name", name).set_birthday(birthday)
    return 'Birthday is set.'

@error_decorator
def show_birthday(args, book):
    name, *_ = args
    return str(book.find("name", name).birthday)

@error_decorator
def remove_birthday(args, book):
    name, *_ = args
    book.find("name", name).remove_birthday()
    return "Birthday removed."

@error_decorator
def birthdays(args, book):
    days, *_ = args + [None]
    upcoming_birthdays = None
    if days is None:
        upcoming_birthdays = book.get_upcoming_birthdays()
    elif days.isnumeric():
        upcoming_birthdays = book.get_upcoming_birthdays(int(days))
    else: 
        raise ValueError("Birthdays.DaysMustBeNumeric")
    
    if len(upcoming_birthdays) == 0:
        return "There is no upcoming birthdays."

    result = f"Here are birthdays that will come in {days} days:\r\n"
    for item in upcoming_birthdays:
        result += f"{item['name']} - {item['congratulation_date']}\r\n"

    return result.strip()

@error_decorator
def set_email(args, book):
    name, email = args
    book.find("name", name).set_email(email)
    return 'Email is set.'

@error_decorator
def show_email(args, book):
    name, *_ = args
    return str(book.find("name", name).email)

@error_decorator
def remove_email(args, book):
    name, *_ = args
    book.find("name", name).remove_email()
    return "Email removed."

@error_decorator
def set_address(args, book):
    name, *address_array = args
    address = " ".join(i for i in address_array if i is not None).strip()
    book.find("name", name).set_address(address)
    return 'Address is set.'

@error_decorator
def show_address(args, book):
    name, *_ = args
    return book.find("name", name).address

@error_decorator
def remove_address(args, book):
    name, *_ = args
    book.find("name", name).remove_address()
    return "Address removed."

@error_decorator
def add_note(args, book: NoteBook):
    title, *note_array = args
    note_text = " ".join(i for i in note_array if i is not None).strip()
    
    message = "Note updated."
    note = None

    if title not in book:
        note = Note(title, note_text)
        book.add_note(note)
        message = "Note added."
    else:
        book[title].note = note

    return message

@error_decorator
def get_note(args, book: NoteBook):
    field, value = args
    return str(book.find(field, value))

@error_decorator
def get_all_notes(book):
    if len(book) == 0:
        return "Note book is empty."

    result = ""
    for note in book.values():
        result += f"{note}\r\n"
    return result.strip()

@error_decorator
def remove_note(args, book: NoteBook):
    title, *_ = args
    book.remove(title)
    return "Note removed"

@error_decorator
def save_data(book, filename):
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
        return None
    except Exception:
        raise IOError("IO.SaveFailed")
    
@error_decorator
def load_data(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
    except Exception:
        raise IOError("IO.LoadFailed")
