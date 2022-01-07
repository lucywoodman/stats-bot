# Third party imports
import os
import getpass
import hashlib
from xkcdpass import xkcd_password as xp
from pymongo import MongoClient

# Local application imports
if os.path.exists('settings.py'):
    from settings import mongodb_string

# Connect to MongoDB and set the database variables
client = MongoClient(mongodb_string)
db = client.supportStats
users = db.users
stats = db.stats


def welcome():
    while True:
        print('doodledy doo doo')
        break


def create_password():
    """
    * Creates a randomly generated password using the xkcdpass library.
    * @return(str) gen_password -- the password.
    """
    word_file = xp.locate_wordfile()
    words = xp.generate_wordlist(
        wordfile=word_file, min_length=5, max_length=10)

    gen_password = xp.generate_xkcdpassword(words, numwords=3, delimiter="-")
    return gen_password


def register():
    """
    * Allows new users to register using a chosen username and
    * generated password from create_password().
    * Hashes the password and saves to the connected database.
    """
    username = input('Enter a username: ')
    pwd = create_password()
    print('Please save the password somewhere safe.')
    print(f'Your password is: {pwd}')

    enc_pwd = pwd.encode()
    hash_pwd = hashlib.md5(enc_pwd).hexdigest()

    newUser = {
        "username": username,
        "password": hash_pwd
    }

    db.users.insert_one(newUser)
    print('You have successfully registered!')
    print('Go ahead and login:')
    login()


def login():
    """
    * Captures the user's input username and password, and checks if they exist in the database. 
    * If they're already registered, and the input details match, allows login.
    """
    while True:
        # Capture the user input for username and password.
        user = input('Username: ')
        pwd = getpass.getpass()

        # Encode and hash the password to match how the database stores passwords.
        enc_pwd = pwd.encode()
        hash_pwd = hashlib.md5(enc_pwd).hexdigest()

        if db.users.count_documents({"username": user}, limit=1):
            result = db.users.find_one({"username": user})

            if result["password"] == hash_pwd:
                print('Successfully logged in!')
                welcome()
                break
            else:
                print('The password is incorrect. Try again.')
        else:
            print('That username isn\'t registered.')


class Menu:
    """
    * A class to power the menu.
    * @staticmethods:
    * opt_1() through to opt_9() -- options for the menu.
    * process() -- matches the user input with the menu option.
    * run() -- ensures user input is int, runs process().
    * generate_menu() -- creates a str from the menu options and prints it.
    """
    @staticmethod
    def opt_1():
        """Login"""
        print('Enter your username and password:')
        login()

    @staticmethod
    def opt_2():
        """Register"""
        register()

    @staticmethod
    def opt_9():
        """Exit"""
        print('Exiting...')

    @staticmethod
    def process(user_input):
        option_name = f'opt_{user_input}'
        try:
            option = getattr(Menu, option_name)
        except AttributeError:
            print('Option not found.')
        else:
            option()

    @staticmethod
    def run():
        user_input = 0
        while(user_input != 9):
            try:
                user_input = int(input())
                Menu.process(user_input)
            except ValueError:
                print('Please insert a number:')
        print('Goodbye!')

    @staticmethod
    def generate_menu():
        print('=' * 80)
        options = [i for i in dir(Menu) if i.startswith('opt_')]
        menu_str = '\n'.join(
            f'{option[-1]}. {getattr(Menu, option).__doc__}' for option in options)
        print(menu_str)
        print('=' * 80)
        print('Insert a number: ')


def main():
    Menu.generate_menu()
    Menu.run()


if __name__ == '__main__':
    main()
