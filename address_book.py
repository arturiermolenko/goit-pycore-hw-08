import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import Optional


class Field:
    """Base class for fields."""

    def __init__(self, value: str) -> None:
        self.value = value

    @staticmethod
    def _validate_data(pattern: str, value: str) -> bool:
        match = re.match(pattern=pattern, string=value)
        return match is not None

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Name field."""

    def __init__(self, value: str) -> None:
        pattern = r"^[A-Za-z]+$"
        if not self._validate_data(pattern=pattern, value=value):
            raise ValueError(f"'{value}' is not a valid name. Use letters only")

        super().__init__(value)


class Phone(Field):
    """Phone field with validation of number."""

    def __init__(self, value: str) -> None:
        pattern = r"^\d{10}$"
        if not self._validate_data(pattern=pattern, value=value):
            raise ValueError("Invalid phone format. Phone was not added.")

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str) -> None:
        pattern = r"^\d{2}.\d{2}.\d{4}$"
        if not self._validate_data(pattern=pattern, value=value):
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")

        value = datetime.strptime(str(value), "%d.%m.%Y").date()
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value)


class Record:
    """Class for records."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date: str) -> None:
        self.birthday = Birthday(date)

    def remove_birthday(self) -> None:
        self.birthday = None

    def add_phone(self, number: str) -> None:
        """Add a phone to the record"""
        phone = Phone(number)
        self.phones.append(phone)

    def remove_phone(self, number: str) -> None:
        """Remove a phone from the record"""
        phone = self.find_phone_object(number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_number: str, new_number) -> None:
        """Edit a phone number in the record"""
        phone = self.find_phone_object(old_number)
        if phone:
            index = self.phones.index(phone)
            self.phones[index] = Phone(new_number)

    def find_phone(self, number: str) -> str | None:
        """Find a phone number from the record"""
        phone = self.find_phone_object(number)
        if phone:
            return str(phone)
        return None

    def find_phone_object(self, number: str):
        """Helper method to find a phone number from the record"""
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def __str__(self):
        for phone in self.phones:
            if phone.value:
                return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        return f"Contact name: {self.name.value} with no phone numbers in book"


class AddressBook(UserDict):
    """Address book class."""

    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Find a record in the address book."""
        if name in self.data:
            return self.data[name]

    def delete(self, name: str) -> None:
        """Delete a record from the address book."""
        self.data.pop(name)

    def get_upcoming_birthdays(self) -> list[dict]:
        congratulation_list = []
        date_today = datetime.today().date()

        for user_name, users_record in self.data.items():
            birthday = users_record.birthday.value

            if date_today <= birthday <= date_today + timedelta(days=7):
                if birthday.weekday() == 5:
                    congratulation_date = birthday + timedelta(days=2)
                elif birthday.weekday() == 6:
                    congratulation_date = birthday + timedelta(days=1)
                else:
                    congratulation_date = birthday

                congratulation_date = congratulation_date.strftime("%d.%m.%Y")
                users_info = {
                    "name": user_name,
                    "congratulation_date": congratulation_date,
                }
                congratulation_list.append(users_info)

        return congratulation_list
