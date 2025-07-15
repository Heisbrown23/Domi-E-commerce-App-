"""The module here handles all authentication-related functionalities: signing in, signing up,
password hashing (though not explicitly mentioned, it's good practice for security), and password generation."""

import re  # "re" stands for regular expressions. bring in Python tools for finding patterns in text.

import os   #means bring in Python's tools to work with files and folders.

import random   # means bring in Python's tools to pick or create things randomly.

import string    #means to bring in Python's tools for working with a letter, number, and symbols.

import hashlib    # it turns words like your password into secret code that no one can read.

ACCOUNTS_FILE = os.path.join("data", "accounts.txt")

def _hash_password(password: str) -> str:
     #we hash the password using SHA256.
     #SHA stands for Secure Hash Algorithm.
     #use to turn a piece of text into a secret code.

    return hashlib.sha256(password.encode()).hexdigest()
    #take the password, turn it into a secret SHA256 code and return the result.

def _check_password_strength(password: str) -> bool:
    #Here we check if a password meets the strength criteria.

    if len(password) < 16:
        return False

    if not any(c.islower() for c in password): #if the password does not have any lower letter, show an error.
        return False

    if not any(c.isupper() for c in password): #if the password does not have any capital letter, show an error.
        return False

    if not any(c.isdigit() for c in password): #if the password does not have any digit, show an error.
        return False

    if not any(c in string.punctuation for c in password): #if the password does not have any special symbols. indicate
        return False

    return True #return True as answer in this function



def generate_strong_password() -> str:

    """Generates a strong password meeting the specified criteria."""

    while True:

        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))

        if _check_password_strength(password):

            return password



def _get_all_accounts() -> list[dict]:

    """Reads all accounts from accounts.txt."""

    accounts = []

    try:

        with open(ACCOUNTS_FILE, 'r') as f:

            for line in f:

                parts = line.strip().split(',')

                if len(parts) == 4:

                    accounts.append({

                        "username": parts[0].strip(),

                        "email": parts[1].strip(),

                        "password_hash": parts[2].strip(),

                        "balance": float(parts[3].strip())

                    })

    except FileNotFoundError:

        pass # Will be handled by setup_data_storage

    return accounts

def _save_accounts(accounts: list[dict]):

    """Saves all accounts back to accounts.txt."""

    with open(ACCOUNTS_FILE, 'w') as f:

        for account in accounts:

            f.write(f"{account['username']},{account['email']},{account['password_hash']},{account['balance']:.2f}\n")



def sign_up():

    """Handles new user registration."""

    print("\n--- Sign Up ---")

    accounts = _get_all_accounts()



    while True:

        username = input("Enter desired username: ").strip()

        if any(acc['username'].lower() == username.lower() for acc in accounts):

            print("Username already taken. Please choose another.")

        else:

            break



    while True:

        email = input("Enter email address: ").strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):

            print("Invalid email format. Please try again.")

        elif any(acc['email'].lower() == email.lower() for acc in accounts):

            print("Email already registered. Please choose another or sign in.")

        else:

            break



    while True:

        password_choice = input("Create password manually (M) or generate automatically (A)? ").strip().upper()

        if password_choice == 'M':

            while True:

                password = input("Enter password (min 16 chars, 1 lower, 1 upper, 1 num, 1 special): ").strip()

                if _check_password_strength(password):

                    break

                else:

                    print("Password does not meet strength requirements. Please try again.")

            break

        elif password_choice == 'A':

            password = generate_strong_password()

            print(f"Generated password: {password}")

            input("Press Enter to continue after noting your password...") # Give user time to note it

            break #stop the loop and jump out!

        else:
            print("Wrong option. Please enter 'Manuel'✅✅ or 'Automatic'📩📩.")  # CHOOSE MANUEL OR AUTOMATIC.

    hashed_password: str = _hash_password(password)

    new_account = {
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "balance": 0.00
    }

    accounts.append(new_account)  #add the new account to the end of the account list.
    _save_accounts(accounts)   #Call a function named _save_accounts and give it the account list to save.

    print("Account created successfully! ✅✅✅🫂")

    return new_account # Return the newly created account for immediate login


def sign_in():
    #Here deals with handling existing user login.

    print("="*40)
    print("\n--- SIGN IN ---")
    print("=" * 40)

    accounts: list[dict] = _get_all_accounts()
    max_attempts: int = 4
    attempts: int = 0

    while attempts < max_attempts:
        user_input: str = input("Enter username or email 📩: ").strip()
        password: str = input("Enter password 🔏: ").strip()
        hashed_password: str = _hash_password(password)

        found_account = None        #no account found

        for account in accounts:    #go through each account in the account list, one by one.

            if (account['username'].lower() == user_input.lower() or

                account['email'].lower() == user_input.lower()):

                if account['password_hash'] == hashed_password:

                    found_account = account

                    break  #stop the loop and jump out!

        if found_account:
            print("Login successful!🫂✅")

            return found_account #that means we found your account

        else:
            attempts += 1 #👈add one to the number stored an attempt.

            print(f"Invalid username/email or password ❌. {max_attempts - attempts} attempts remaining 🥱.")



    print("Too many failed attempts❌. Returning to main menu 🤳.")
    return None #return nothing