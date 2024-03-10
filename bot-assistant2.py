from collections import UserDict

### Errors block

class BotPhoneLenghtException(Exception):
    pass
class BotRecordNotFoundException(Exception):
    pass


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BotPhoneLenghtException:
            return None
    return inner
###

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        Field.__init__(self, name)

class Phone(Field):
    def __init__(self, value):
        if len(value) < 10:
            raise BotPhoneLenghtException
        Field.__init__(self, value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def add_phone(self, phone):
        try: 
            self.phones.append(
                Phone(phone)
            )
        except BotPhoneLenghtException:
            print('  Wrong phone number.')

    def edit_phone(self, pold, pnew):
        for p in range(len(self.phones)):
            if self.phones[p].value == pold:
                try:
                    self.phones[p] = Phone(pnew)
                except BotPhoneLenghtException:
                    print(' Wrong phone number.')
    
    def find_phone(self, value):
        for p in self.phones:
            if p.value == value:
                return p
        return None # Empty Phone object expected

    def remove_phone(self, value):
        p = self.find_phone(value)
        if p is not None:
            self.phones.remove(p)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def __call__(self):
        return self.name.value

class AddressBook(UserDict):
    def add_record(self, value):
        self.data[value()] = value
    
    def __find(self, value):
        try:
            return self.data[value]
        except:
            raise BotRecordNotFoundException
    
    def find(self, value):
        try:
            return self.__find(value)
        except BotRecordNotFoundException:
            print("  Record not found.")
        return None # Empty Record object Expected

    def delete(self, value):
        try:
            self.__find(value)
            del self.data[value]
        except BotRecordNotFoundException:
            print("  Record not found.")


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    #john_record.add_phone("0987654321")
    #john_record.add_phone("0987654")
    john_record.add_phone("5555555555")

    #print(john_record)

    book.add_record(john_record)
    #print(book.data)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    #print(jane_record)
    #print(book.data)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")
    #john.remove_phone("5555555555")
    #print(john)
    book.delete("Jane")

    #lev = book.find('Lev')
    #book.delete("Lev")

    #print(book.data)
