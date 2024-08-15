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
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()