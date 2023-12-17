from collections import UserDict
from datetime import datetime
from utils.error_utils import input_error, validation_error, error_messages, validation_messages, ValidationError
from utils.prompt_utils import is_yes_prompt
from utils.validators import is_valid_phone, is_valid_date, date_format_default
from utils.birthdays_per_week import get_birthdays_per_week

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        self.value = Field(name)

class Phone(Field):
    def __init__(self, phone):
        self.value = None
        self.set_value(phone)

    @validation_error
    def set_value(self, phone):
        if not is_valid_phone(phone):
            raise ValidationError(validation_messages["invalid_phone"])
        else:
            self.value = Field(phone)

class Birthday(Field):
    def __init__(self, date):
        self.value = None
        self.set_value(date)

    @validation_error
    def set_value(self, date):
        if not is_valid_date(date):
            raise ValidationError(validation_messages["invalid_date"])
        else:
            self.value = Field(date)

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []
    
    def get_str_name(self):
        return str(self.name)

    def get_str_phones(self):
        return list(map(str, self.phones))
        
    def add_phone(self, phone):
        phone = Phone(phone)
        if phone.value:
            self.phones.append(phone)
            return True
        return False

    @input_error()
    def edit_phone(self, old_phone, new_phone):
        is_updated = False
        idx = self.find_phone_index(old_phone)
        if idx:
            phone = Phone(new_phone)
            if phone.value:
                self.phones[idx] = phone
                is_updated = True
        elif is_yes_prompt(f"Do you want to add new phone to this contact?: "):
            is_updated = self.add_phone(new_phone)
        return is_updated

    @input_error()
    def find_phone_index(self, phone):
        str_phones = self.get_str_phones()
        idx = None
        if not phone in str_phones:
            raise IndexError(f"{self.name}'s contact hasn't such phone")
        else:
            idx = str_phones.index(phone)
        return idx

    @input_error()
    def find_phone(self, phone):
        idx = self.find_phone_index(phone)
        return self.phones[idx] if idx else None
    
    @input_error()
    def remove_phone(self, phone):  
        str_phones = self.get_str_phones()      
        if not phone in self.get_str_phones():
            raise IndexError(f"{self.name}'s contact hasn't such phone")
        idx = str_phones.index(phone)
        self.phones.pop(idx)
        print(f"{self.name}'s phone was removed successfully")
    
    def add_birthday(self, date):
        birthday = Birthday(date)
        if birthday.value:
            self.birthday = birthday
            return True
        return False

    def __str__(self):
        return f"Contact Name: {self.name.value}, Phone(s): {'; '.join(str(p.value) for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, name, phone):
        is_updated = False
        if name in self.data:
            contact = self.find(name)
            # if is_yes_prompt(f"Contact with name {name} already exists. Do you want to update contact?: "):
            is_updated = contact.add_phone(phone)
        else:
            contact = Record(name)
            is_updated = contact.add_phone(phone)
            if is_updated:
                self.data[name] = contact
        return is_updated

    def update_record_phone(self, name, old_phone, new_phone):
        is_updated = False
        if name in self.data:
            contact = self.find(name)
            is_updated = contact.edit_phone(old_phone, new_phone)
        else:
            if is_yes_prompt(f"There is no such contact in your Address Book. Do you want to create it?: "):
                is_updated = self.add_record(name, new_phone)
        return is_updated

    @input_error(error_messages["no_contact"])
    def find(self, name):
        return self.data[name]

    @input_error(error_messages["no_contact"])
    def delete(self, name):
        is_updated = name in self.data
        del self.data[name]
        return is_updated

    def add_birthday(self, name, birthday):
        is_updated = False
        if name in self.data:
            contact = self.data[name]
            if contact.birthday:
                if is_yes_prompt("Existing birthday will be updated, continue?: "):
                    is_updated = contact.add_birthday(birthday)
            else:
                is_updated = contact.add_birthday(birthday)
        else:
            contact = Record(name)
            is_updated = contact.add_birthday(birthday)
            if is_updated:
                self.data[name] = contact
        return is_updated
    
    def show_birthday(self, name):
        contact = self.find(name)
        if contact and contact.birthday:
            return f"{name}'s birthday: {contact.birthday}"
        elif contact:
            return f"There is no birthday set for {name}"

    def get_contact_list_simplified(self):
        record_list = list(self.data.values())
        contact_list = []
        for record in record_list:
            contact_list.append({
                "name": str(record.name),
                "birthday": str(record.birthday),
                "phones": list(map(str, record.phones))
            })
        return contact_list

    def get_birthdays_per_week(self):
        contact_list = self.get_contact_list_simplified()
        contacts_with_bd = [contact for contact in contact_list 
            if bool(contact["birthday"]) and contact["birthday"] != 'None'
        ]
        birthdays = get_birthdays_per_week(contacts_with_bd)
        return birthdays

    def set_data_from_store(self, stored_contacts):
        for row in stored_contacts:
            record = Record(row["name"])
            if row["birthday"] and row["birthday"] != 'None':
                record.add_birthday(row["birthday"])
            for phone in row["phones"]:
                record.add_phone(phone)
            self.data[row["name"]] = record

    def __str__(self):
        record_list = list(self.data.values())
        if not len(record_list):
            return error_messages["no_contacts"]
        contacts_str_list = map(str, record_list)
        contacts_to_display = '\n'.join(contacts_str_list)
        return contacts_to_display.strip()
