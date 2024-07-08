import pickle
from typing import Tuple

from address_book import AddressBook
from error_decorator import input_error
from handlers import (
    print_contact,
    show_upcoming_birthdays,
    show_birthday,
    add_birthday,
    add_contact,
    update_contact,
    remove_contact,
    remove_birthday
)

FILENAME = "addressbook.pkl"


def save_data(book, filename=FILENAME):
    """
    Function to save the data in a pickle file.
    :param book: AddressBook object to save.
    :param filename: Filename to save the data in.
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=FILENAME):
    """
    Function to load the data from a pickle file or to create a new one.
    :param filename: Filename to load the data from.
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def parse_input(user_input: str) -> Tuple[str, list] | None:
    """
    Take users input as a string and split into separate command and list of args
    :param user_input: string to be parsed
    :return: tuple of command and list of args
    """
    if not user_input:
        return
    elif len(user_input.split()) > 3:
        print("Too many arguments")
        return

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def print_hint() -> str:
    return """
        How can I help you?
        
            Type 'add name number' to add a new contact.
            Type 'change name number' to change contact.
            Type 'phone name' to print contacts phone number/numbers.
            Type 'delete name' to delete record. 
            Type 'add-birthday name date(in format DD.MM.YYYY)' to add a birthday to record.
            Type 'show-birthday name' to print users' birthday.
            Type 'delete-birthday' to remove birthday date from record.
            Type 'birthdays' to print all upcoming(next 7 days) birthdays.
            Type 'all' to print all contacts in phone book.
            Type 'close' or 'exit' to exit the assistant. 
            """


@input_error
def main() -> None:
    book = load_data()
    hint = print_hint()
    print(hint)

    while True:
        user_input = input("Enter a command: ")

        parsed_input = parse_input(user_input)
        if parsed_input:
            command, *args = parsed_input
        else:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            response = "Hello, my friend!"
        elif command == "help":
            response = print_hint()
        elif command == "add":
            response = add_contact(args, book)
        elif command == "change":
            response = update_contact(args, book)
        elif command == "delete":
            response = remove_contact(args, book)
        elif command == "phone":
            response = print_contact(args, book)
        elif command == "add-birthday":
            response = add_birthday(args, book)
        elif command == "show-birthday":
            response = show_birthday(args, book)
        elif command == "delete-birthday":
            response = remove_birthday(args, book)
        elif command == "birthdays":
            response = show_upcoming_birthdays(book)
        elif command == "all":
            response = ""
            for record in book.data.values():
                response += f"{str(record)}\n"
            if not response:
                response = "The phone book is empty."
        else:
            response = "Invalid command."

        print(response)


if __name__ == "__main__":
    main()
