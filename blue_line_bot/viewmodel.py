from blue_line_bot.model import AddressBook, Record, NoteBook, Note
from colorama import Fore
from prettytable import PrettyTable
import pickle

def error_output(line):
    return Fore.LIGHTRED_EX + "! " + line

def info_output(line):
    return Fore.LIGHTYELLOW_EX + "! " + line

def error_decorator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            message = str(ex)
            if message == "Name.Required":
                return error_output("Name can not be empty")
            elif message == "Phone.NotNumeric":
                return error_output("Phone must be numeric")
            elif message == "Phone.LengthMustBe10":
                return error_output("Phone lenght must be 10 digits")
            elif message == "Birthday.Invalid":
                return error_output("Birthday should be in format d.m.Y (e.g. 27.1.2000)")
            elif message == "Email.Required":
                return error_output("Email can not be empty")
            elif message == "Email.Invalid":
                return error_output("Input a valid email")
            elif message == "Address.Required":
                return error_output("Address can not be empty")
            elif message == "Record.PhoneDuplicate":
                return error_output("This phone already exists in the record")
            elif message == "Record.PhoneNotFound":
                return error_output("This phone does not exist in the record")
            elif message == "AddressBook.DuplicateName":
                return error_output("This name is already exists in the address book")
            elif message == "AddressBook.NotFound":
                return error_output("This value does not exist in the address book")
            elif message == "AddressBook.DaysMustBeInt":
                return error_output("Days value should be integer")
            elif message == "NoteBook.NotFound":
                return error_output("This value does not exist in the note book")
            elif message == "Birthdays.DaysMustBeNumeric":
                return error_output("Days for birthdays must be numeric value")
            else:
                return error_output("Input a valid command.")
        except KeyError:
            return info_output("Contact was not found")
        except IndexError:
            return info_output("Give me contact name to return phone for, please.")
        except IOError as ex:
            message = str(ex)
            if message == "IO.SaveFailed":
                return error_output("Failed to save address book")
            elif message == "IO.LoadFailed":
                return error_output("Failed to save address book")
            else:
                return error_output("Oops... Something went wrong")
        except Exception as ex:
            print(ex)
            return error_output("Oops... Something went wrong")

    return inner

@error_decorator
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

#region Record
#Updates are split into separate functions
#Create
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

#Read
@error_decorator
def get_records(args, book):
    field, value = args
    records = book.find_many(field, value)

    if len(records) == 0:
        return "No contacts match the filter."

    return records_table(records)

@error_decorator
def show_all(book):
    if len(book) == 0:
        return "Address book is empty."

    return records_table(book.values())

def records_table(records: list):
    table = PrettyTable()
    table.field_names = ["Name", "Email", "Birthday", "Phones", "Address"]

    for record in sorted(records, key=lambda record: str(record.name)):
        name = Fore.CYAN + str(record.name) + Fore.RESET
        email = ((Fore.GREEN + str(record.email)) if record.email is not None else "---") + Fore.RESET
        birthday = ((Fore.GREEN + str(record.birthday)) if record.birthday is not None else "---") + Fore.RESET
        phones = ((Fore.YELLOW + record.get_phones()) if record.get_phones() else "---") + Fore.RESET
        address = ((Fore.GREEN + str(record.address)) if record.address is not None else "---") + Fore.RESET
        table.add_row([name, email, birthday, phones, address])
    return table

#Delete
@error_decorator
def remove_record(args, book):
    name, *_ = args
    book.remove(name)
    return "Contact removed"

#endregion

#region Phone  
#Create
@error_decorator
def add_phone(args, book):
    name, phone = args
    book.find("name", name).add_phone(phone)

    return "Contact updated."

#Read
@error_decorator
def get_phones(args, book):
    name = args[0]
    record = book.find("name", name)
    
    if len(record.phones) == 0:
        return "This contact does not have phones."
    else:
        return record.get_phones()

#Update
@error_decorator
def change_phone(args, book):
    name, old_phone, new_phone = args
    book.find("name", name).edit_phone(old_phone, new_phone)

    return "Contact updated."

#Delete
@error_decorator
def remove_phone(args, book):
    name, phone = args
    book.find("name", name).remove_phone(phone)

    return "Phone removed."
#endregion

#region Birthday
#Create/Update
@error_decorator
def set_birthday(args, book):
    name, birthday = args
    book.find("name", name).set_birthday(birthday)
    return 'Birthday is set.'

#Read
@error_decorator
def show_birthday(args, book):
    name, *_ = args
    return str(book.find("name", name).birthday)

#Delete
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
#endregion

#region Email
#Create/Update
@error_decorator
def set_email(args, book):
    name, email = args
    book.find("name", name).set_email(email)
    return 'Email is set.'

#Read
@error_decorator
def show_email(args, book):
    name, *_ = args
    return str(book.find("name", name).email)

#Delete
@error_decorator
def remove_email(args, book):
    name, *_ = args
    book.find("name", name).remove_email()
    return "Email removed."
#endregion

#region Address
#Create/Update
@error_decorator
def set_address(args, book):
    name, *address_array = args
    address = " ".join(i for i in address_array if i is not None).strip()
    book.find("name", name).set_address(address)
    return 'Address is set.'

#Read
@error_decorator
def show_address(args, book):
    name, *_ = args
    return book.find("name", name).address

#Delete
@error_decorator
def remove_address(args, book):
    name, *_ = args
    book.find("name", name).remove_address()
    return "Address removed."
#endregion

#region Notes
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
    return notes_table([book.find(field, value)])

@error_decorator
def get_all_notes(book):
    if len(book) == 0:
        return "Note book is empty."

    return notes_table(book.values())

@error_decorator
def get_notes(args, book: NoteBook):
    if len(args) == 0:
        return get_all_notes(book)

    tag, *_ = args  
    result = []

    for note in book.values():
        if tag in note.tags:
            result.append(note)

    if len(result) == 0:
        return "Zero notes with this tag"
    return notes_table(result)

def notes_table(notes: list):
    table = PrettyTable()
    table.field_names = ["Title", "Tags", "Note"]

    for note in sorted(notes, key=lambda note: note.tags):
        title = Fore.CYAN + note.title + Fore.RESET
        tags = ((Fore.MAGENTA + ', '.join(note.tags)) if note.tags else "---") + Fore.RESET
        text = ((Fore.GREEN + note.note) if note.note else "---") + Fore.RESET
        table.add_row([title, tags, text])
    
    return table

@error_decorator
def remove_note(args, book: NoteBook):
    title, *_ = args
    book.remove(title)
    return "Note removed"

@error_decorator
def add_tag(args, book: NoteBook):
    title, tag, *_ = args
    book.find("title", title).add_tag(tag)
    return "Tag added"
#endregion

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

def help():
    return """Here is the list of commands:

hello - print greeting

add <name> <phone> <email> <birthday> <address> - add new contact with optional info
get <field name> <field value> - get contact's info (e.g. get name Vadym)
all - show all contacts
remove <name> - remove contact by name

add-phone <name> <phone> - add phone number to contact
get-phone <name> - get contact's phone numbers
change-phone <name><old_phone> <new_phone> - change contact's phone number
remove-phone <name> <phone> - remove contact's phone number

set-birthday <name> <birthday> - set birthday to contact in format d.m.Y (e.g. 27.1.2000) 
get-birthday <name> - get contact's birthday in format d.m.Y (e.g. 27.1.2000) 
remove-birthday <name> <birthday> - remove contact's birthday
birthdays <days> - get birthdays upcoming in <days> number of days (optional, default value = 7)

set-email <name> <email> - set email to contact
get-email <name> - get contact's email
remove-email <name> <email> - remove contact's email

set-address <name> <address> - set address to contact
get-address <name> - get contact's address
remove-address <name> <address> - remove contact's address

add-note <title> <note> - add note with given title (title is 1 word)
get-note <field name> <field value> - get note by field (e.g. get title Todo)
get-notes <tag>  - show notes with optional tag filter
add-tag <title> <tag> - add tag to note
update-note <title> <note> - update note with given title (title is 1 word)
remove-note <title> - remove note by title

close - save address book and exit
exit - save address book and exit""" 
