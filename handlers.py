from typing import List

from address_book import AddressBook, Record
from error_decorator import input_error


def check_args_len(args: List[str], quantity: int) -> None:
    if not len(args) == quantity:
        raise IndexError("Not enough arguments")


@input_error
def add_contact(args: List, book: AddressBook) -> str:
    """
    Creates new record in book
    :param args: List of arguments
    :param book: Dictionary of contacts
    :return: text message about operation status
    """
    check_args_len(args=args, quantity=2)
    name, phone = args
    record = book.find(name=name)
    message = "Contact already exists. Use 'change' command to update it."
    if record is None:
        record = Record(name=name)
        book.add_record(record=record)
        message = "Contact created."
        try:
            record.add_phone(number=phone)
        except ValueError as e:
            message = f"{e} Contact created without telephone number."
    return message


@input_error
def update_contact(args: List, book: AddressBook) -> str:
    """
    Takes a list of arguments and creates a new contact.
    :param args: List of arguments
    :param book: Dictionary of contacts
    :return: text message about operation status
    """
    check_args_len(args=args, quantity=2)
    name, phone = args
    record = book.find(name=name)
    message = "There is no such contact in book"
    if record is not None:
        try:
            record.add_phone(number=phone)
            message = "Contact updated."
        except ValueError as e:
            message = e
    return message


@input_error
def print_contact(args: List, book: AddressBook) -> str:
    """
    Print a single contact from the dict of contacts
    :param args: list of arguments
    :param book: dict of contacts
    :return: record to be printed or text message about operation status
    """
    check_args_len(args=args, quantity=1)
    name = args[0]
    record = book.find(name=name)
    if record is not None:
        return record

    message = "Contact not found."
    return message


@input_error
def remove_contact(args: List, book: AddressBook) -> str:
    """
    Remove contact if found
    :param args: list of arguments
    :param book: dict of contacts
    :return: text message about operation status
    """
    check_args_len(args=args, quantity=1)
    name = args[0]
    record = book.find(name=name)
    message = "Contact not found"
    if record is not None:
        book.delete(name=name)
        message = "Contact removed."

    return message


@input_error
def add_birthday(args: List, book: AddressBook) -> str:
    """
    Add a birthday date to the record
    :param args: List of arguments
    :param book: Dictionary of contacts
    :return: text message about operation status
    """
    check_args_len(args=args, quantity=2)
    name, date = args
    record = book.find(name=name)
    message = "Contact not found."
    if record is not None:
        record.add_birthday(date=date)
        message = "Birthday added."
    return message


@input_error
def show_birthday(args: List, book: AddressBook) -> str:
    """
    Show records` birthday date
    :param args: List of arguments
    :param book: Dictionary of contacts
    :return: text message about operation status
    """
    check_args_len(args=args, quantity=1)
    name = args[0]
    record = book.find(name=name)
    message = "Contact not found."

    if record is not None:
        message = record.birthday

    return message


def remove_birthday(args: List, book: AddressBook) -> str:
    """
    Remove birthday date from the record
    :param args: List of arguments
    :param book: Dictionary of contacts
    :return: text message about operation status
    """
    check_args_len(args=args, quantity=1)
    name = args[0]
    record = book.find(name=name)
    message = "Contact not found."
    if record is not None:
        record.remove_birthday()
        message = "Birthday removed."
    return message


@input_error
def show_upcoming_birthdays(book: AddressBook) -> str:
    """
    Shows upcoming birthdays
    :param book: Dictionary of contacts
    :return: Upcoming birthdays list or text message about operation status
    """
    message = "There are no upcoming birthdays."
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        message = ""
        for birthday in upcoming_birthdays:
            message += f"{birthday['name']}: congratulate on {birthday['congratulation_date']}\n"
    return message
