from model import AddressBook
import viewmodel as vm

def main():
    load_result = vm.load_data("addressbook.pkl")
    if isinstance(load_result, str):
        print(load_result)
        address_book = AddressBook()
    elif load_result is None:
        address_book = AddressBook()
    else:
        address_book = load_result

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = vm.parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_result = vm.save_data(address_book, "addressbook.pkl")
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
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()