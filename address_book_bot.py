import json
import re
from utils.error_utils import input_error, error_messages
from utils.prompt_utils import is_yes_prompt
from address_book import AddressBook

phone_pattern = re.compile(r'^\+?\d{1,4}?[-. ]?\(?\d{1,}\)?[-. ]?\d{1,}[-. ]?\d{1,}$')

address_book_filename = "address_book.json"

def is_valid_phone_number(phone_number):
    return bool(phone_pattern.match(phone_number))

@input_error(error_messages["no_command"])
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error(error_messages["no_name_and_phone"])
def add_contact(args, contacts: AddressBook):
    name, phone = args
    is_updated = contacts.add_record(name, phone)
    if is_updated:
        return f"{name} was added to your contacts"

@input_error(error_messages["no_name_and_phones"])
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    is_updated = contacts.update_record_phone(name, old_phone, new_phone)
    if is_updated:
        return f"{name}'s phone was updated"

@input_error(error_messages["no_name"])
def show_phones_by_user(args, contacts: AddressBook):
    name = args[0]
    contacts_by_name = contacts.find(name)
    return contacts_by_name

@input_error(error_messages["no_name"])
def remove_contact(args, contacts: AddressBook):
    name = args[0]
    is_updated = contacts.delete(name)
    if is_updated:
        return f"{name}'s phone was deleted"

@input_error(error_messages["no_contacts"])
def show_all(contacts):
    return str(contacts)

@input_error(error_messages["no_name_or_birthday"])
def add_birthday(args, contacts: AddressBook):
    name, birthday = args
    is_updated = contacts.add_birthday(name, birthday)
    if is_updated:
        return f"{name}'s birsday was added"

@input_error(error_messages["no_name"])
def show_birthday(args, contacts: AddressBook):
    name = args[0]
    birthday = contacts.show_birthday(name)
    return birthday

def show_birthdays(contacts: AddressBook):
    birthdays = contacts.get_birthdays_per_week()
    return birthdays

def save_address_book(contacts: AddressBook):
    with open(address_book_filename, 'w') as file:
        json.dump(contacts.get_contact_list_simplified(), file)

def load_address_book(contacts: AddressBook):
    try:
        with open(address_book_filename, 'r') as file:
            stored_contacts = json.load(file)
            contacts.set_data_from_store(stored_contacts)
            return True
    except:
        return False

def main():
    contacts = AddressBook()
    load_address_book(contacts)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        message = None

        if command in ["close", "exit"]:
            if is_yes_prompt("Do you want to save this Address Book?: "):
                save_address_book(contacts)
            print("Good bye!")
            break
        elif command == "hello":
            message = "How can I help you?"
        elif command == "add":
            message = add_contact(args, contacts)
        elif command == "change":
            message = change_contact(args, contacts)
        elif command == "phone":
            message = show_phones_by_user(args, contacts)
        elif command == "remove":
            message = remove_contact(args, contacts)
        elif command in ["add-birthday","add-bd"]:
            message = add_birthday(args, contacts)
        elif command in ["show-birthday", "show-bd"]:
            message = show_birthday(args, contacts)
        elif command in ["birthdays", "bds"]:
            message = show_birthdays(contacts)
        elif command == "all":
            message = show_all(contacts)
        else:
            message = "Invalid command."
        
        if bool(message):
            print(message)

if __name__ == "__main__":
    main()