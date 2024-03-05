DB = {}

class BotContactExistsException(Exception):
    pass

class BotContactNotExistsException(Exception):
    pass

class BotContactAddException(Exception):
    pass

class BotContactChangeException(Exception):
    pass

class BotContactPhoneException(Exception):
    pass


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "  Error: Wrong syntax!"
        except BotContactExistsException:
            return "  Contact is present in DB. Use change command instead"
        except BotContactNotExistsException:
            return "  Contact is not present in DB."
        except BotContactAddException:
            return "  Error: Wrong syntax!\n  Example: add UserName 12345678890"
        except BotContactChangeException:
            return "  Error: Wrong syntax!\n  Example: change UserName 12345678890"
        except BotContactPhoneException:
            return "  Error: Wrong syntax!\n  Example: phone UserName"
        except:
            return "  Something happen!"
    return inner

def parce_input(input):
    cmd, *args = input.split()
    return cmd.lower(), *args

@error_handler
def add_contact_handler(args):
    if len(args) < 2:
        raise BotContactAddException
    name, phone = args
    if name in DB.keys():
        raise BotContactExistsException
    DB[name] = phone
    return " Contact added."

@error_handler
def change_contact_handler(args):
    if len(args) != 2:
        raise BotContactChangeException    
    name, phone = args
    if name not in DB.keys():
        raise BotContactNotExistsException 
    DB[name] = phone
    return " Contact updated."

@error_handler
def phone_contact_handler(args):
    if len(args) != 1:
        raise BotContactPhoneException   
    name = args[0]
    if name not in DB.keys():
       raise BotContactNotExistsException 
    return " {}".format(DB[name])

@error_handler
def show_all():
    for c in DB:
        print(" {}: {}".format(c, DB[c]))
    

if __name__ == "__main__":
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, *args = parce_input(user_input)

        if command in ["close", "exit"]:
            print(" Good bye!")
            break
        elif command == "hello":
            print(" How can I help you?")
        elif command == "add":
            print(add_contact_handler(args))
        elif command == "change":
            print(change_contact_handler(args))
        elif command == "phone":
            print(phone_contact_handler(args))
        elif command == "all":
            show_all()
        else:
            print(" Invalid command.")
