from blue_line_bot.model import AddressBook, NoteBook
import blue_line_bot.viewmodel as vm
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

commands = [
        "add",
        "add-note",
        "add-phone",
        "add-tag",
        "all",
        "birthdays",
        "change-phone",
        "close",
        "exit",
        "get",
        "get-address",
        "get-birthday",
        "get-email",
        "get-note",
        "get-notes",
        "get-phone",
        "hello",
        "remove",
        "remove-address",
        "remove-birthday",
        "remove-email",
        "remove-note",
        "remove-phone",
        "set-address",
        "set-birthday",
        "set-email",
        "update-note"
        ]

completer = WordCompleter(commands, ignore_case=True)

style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
        "prompt": "ansiblue"
    }
)

session = PromptSession(completer=completer, style=style)

def main():
    load_result = vm.load_data("addressbook.pkl")
    if isinstance(load_result, str):
        print(load_result)
        address_book = AddressBook()
    elif load_result is None:
        address_book = AddressBook()
    else:
        address_book = load_result

    load_result = vm.load_data("notebook.pkl")
    if isinstance(load_result, str):
        print(load_result)
        note_book = NoteBook()
    elif load_result is None:
        note_book = NoteBook()
    else:
        note_book = load_result

    print("Welcome to the assistant bot!")
    while True:
        user_input = session.prompt("Enter a command: ")
        command, *args = vm.parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_result = vm.save_data(address_book, "addressbook.pkl")
            if save_result is not None:
                print(save_result)
            
            save_result = vm.save_data(note_book, "notebook.pkl")
            if save_result is not None:
                print(save_result)

            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(vm.add_contact(args, address_book))
        elif command == "get":
            print(vm.get_records(args, address_book))
        elif command == "all":
            print(vm.show_all(address_book))
        elif command == "remove":
            print(vm.remove_record(args, address_book))
        elif command == "add-phone":
            print(vm.add_phone(args, address_book))
        elif command == "get-phone":
            print(vm.get_phones(args, address_book))
        elif command == "change-phone":
            print(vm.change_phone(args, address_book))
        elif command == "remove-phone":
            print(vm.remove_phone(args, address_book))
        elif command == "set-birthday":
            print(vm.set_birthday(args, address_book))
        elif command == "get-birthday":
            print(vm.show_birthday(args, address_book))
        elif command == "remove-birthday":
            print(vm.remove_birthday(args, address_book))
        elif command == "birthdays":
            print(vm.birthdays(args, address_book))
        elif command == "set-email":
            print(vm.set_email(args, address_book))
        elif command == "get-email":
            print(vm.show_email(args, address_book))
        elif command == "remove-email":
            print(vm.remove_email(args, address_book))
        elif command == "set-address":
            print(vm.set_address(args, address_book))
        elif command == "get-address":
            print(vm.show_address(args, address_book))
        elif command == "remove-address":
            print(vm.remove_address(args, address_book))
        elif command == "add-note":
            print(vm.add_note(args, note_book))
        elif command == "get-note":
            print(vm.get_note(args, note_book))
        elif command == "get-notes":
            print(vm.get_notes(args, note_book))
        elif command == "add-tag":
            print(vm.add_tag(args, note_book))
        elif command == "update-note":
            print(vm.add_note(args, note_book))
        elif command == "remove-note":
            print(vm.remove_note(args, note_book))
        elif command == "help":
            print(vm.help())
        else:
            print(vm.error_output("Invalid command."))

if __name__ == "__main__":
    main()