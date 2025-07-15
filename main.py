"""This is our main entry point for the application, where it handles the overall flow,
presenting the login/signup options, and then navigating to the main run section."""

import os #means bring in Python's tools to work with files and folders.

import time #means to bring in Python's clock tools to help with time / delays.

import re # "re" stands for regular expressions. bring in Python tools for finding patterns in text.

import hashlib # it turns words like your password into secret code that no one can read.

import random   #means bring in Python's tools to pick or create things randomly.

import string #means to bring in Python's tools for working with a letter, number, and symbols.

#Utility Functions (in utils.py)
DATA_DIR: str = "data"

ACCOUNTS_FILE: str = os.path.join(DATA_DIR, "accounts.txt") #👈create the full file path for accounts.txt, inside
                                                            #folder named DATA_DIR.
def clear_screen(): #Clears the console screen.
    os.system('cls' if os.name == 'nt' else 'clear') #👈if the computer is Windows, use cls. if not, use clear.
                                                     # Either way, just clean the screen


def setup_data_storage():
    """Ensures the 'data' directory and 'accounts.txt' file exist."""

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

        print(f"Created directory: {DATA_DIR}")

    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:
            pass  # Create an empty accounts.txt file

        print(f"Created file: {ACCOUNTS_FILE}")


#Authentication Functions (auth.py)

def _hash_password(password: str) -> str:
    """Hashes a password using SHA256."""

    return hashlib.sha256(password.encode()).hexdigest()


def _check_password_strength(password: str) -> bool:
    """Checks if a password meets the strength criteria."""

    if len(password) < 16:
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    if not any(c in string.punctuation for c in password):  # Includes common special symbols

        return False

    return True


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

        pass  # Will be handled by setup_data_storage

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

            input("Press Enter to continue after noting your password...")  # Give user time to note it

            break

        else:

            print("Invalid choice. Please enter 'M' or 'A'.")

    hashed_password = _hash_password(password)

    new_account = {

        "username": username,

        "email": email,

        "password_hash": hashed_password,

        "balance": 0.00

    }

    accounts.append(new_account)

    _save_accounts(accounts)

    print("Account created successfully!")

    return new_account  # Return the newly created account for immediate login


def sign_in():
    """Handles existing user login."""

    print("\n--- Sign In ---")

    accounts = _get_all_accounts()

    max_attempts = 3

    attempts = 0

    while attempts < max_attempts:

        user_input = input("Enter username or email: ").strip()

        password = input("Enter password: ").strip()

        hashed_password = _hash_password(password)

        found_account = None

        for account in accounts:

            if (account['username'].lower() == user_input.lower() or

                    account['email'].lower() == user_input.lower()):

                if account['password_hash'] == hashed_password:
                    found_account = account

                    break

        if found_account:

            print("Login successful!")

            return found_account

        else:

            attempts += 1

            print(f"Invalid username/email or password. {max_attempts - attempts} attempts remaining.")

    print("Too many failed attempts. Returning to main menu.")

    return None


# --- Inventory Functions (inventory.py) ---

def load_inventory_from_files() -> dict:
  #loads inventory items from all warehouse*.txt files in the data directory.
  # returns a dictionary where keys are item names and values are dictionaries
  # containing 'price' and 'quantity'.

    inventory: dict = {}

    for filename in os.listdir(DATA_DIR):

        if filename.startswith("warehouse") and filename.endswith(".txt"):

            filepath = os.path.join(DATA_DIR, filename)

            try:

                with open(filepath, 'r') as f:

                    content = f.read().strip()

                    if not content:
                        continue

                    items_str = content.split(';')

                    for item_str in items_str:

                        if ':' in item_str:

                            name, price_str = item_str.strip().split(':', 1)

                            try:

                                price = float(price_str)

                                # Assuming initial quantity for each item is 10 for simplicity

                                inventory[name] = {"price": price, "quantity": 10}

                            except ValueError:

                                print(f"Warning: Invalid price format for item '{name}' in {filename}. Skipping.")

                        else:

                            print(f"Warning: Invalid item format '{item_str}' in {filename}. Skipping.")

            except FileNotFoundError:

                print(f"Error: {filepath} not found.")

            except Exception as e:

                print(f"Error reading {filepath}: {e}")

    return inventory


def search_inventory(query: str, inventory: dict) -> list[tuple[str, float]]:
    """

    Searches the inventory for items matching the query.

    Returns a list of (item_name, item_price) tuples.

    """

    search_terms: list[str] = query.split()

    regex_patterns: list[re.Pattern[str]] = [re.compile(re.escape(term), re.IGNORECASE) for term in search_terms]

    search_output: list[tuple[str, float]] = []

    for item_name, details in inventory.items():

        if all(pattern.search(item_name) for pattern in regex_patterns):
            search_output.append((item_name, details["price"]))

    return search_output


# --- Account Management Functions (account_management.py) ---

def _authenticate_user_password(current_user: dict) -> bool:
    """Prompts for password and verifies it against the current user's password."""

    password = input("Please enter your password to confirm: ").strip()

    if _hash_password(password) == current_user['password_hash']:

        return True

    else:

        print("Incorrect password. Operation cancelled.")

        return False


def fund_wallet(current_user: dict):
    """Allows user to add money to their wallet."""

    print("\n--- Fund Wallet ---")

    options = [10000, 20000, 50000, 100000]

    for i, amount in enumerate(options):
        print(f"{i + 1}. NGN {amount:,.2f}")

    print("5. Custom Amount")

    print("6. Back to Run Menu")

    while True:

        try:

            choice = input("Select an option to fund your wallet: ").strip()

            if choice == '6':
                return

            fund_amount = 0.0

            if choice == '5':

                while True:

                    try:

                        custom_amount = float(input("Enter custom amount to deposit (NGN): "))

                        if custom_amount > 0:

                            fund_amount = custom_amount

                            break

                        else:

                            print("Amount must be positive.")

                    except ValueError:

                        print("Invalid amount. Please enter a number.")

            else:

                choice_index = int(choice) - 1

                if 0 <= choice_index < len(options):

                    fund_amount = options[choice_index]

                else:

                    print("Invalid option. Please try again.")

                    continue

            current_user['balance'] += fund_amount

            accounts = _get_all_accounts()

            for i, acc in enumerate(accounts):

                if acc['username'] == current_user['username']:
                    accounts[i] = current_user

                    break

            _save_accounts(accounts)

            print(f"Wallet funded successfully! Your new balance is NGN {current_user['balance']:,.2f}")

            cont_choice = input("Continue funding (Y/N)? ").strip().upper()

            if cont_choice != 'Y':
                break

        except ValueError:

            print("Invalid input. Please enter a number.")

        except Exception as e:

            print(f"An error occurred: {e}")


def change_username(current_user: dict):
    """Allows user to change their username."""

    print("\n--- Change Username ---")

    if not _authenticate_user_password(current_user):
        return

    accounts = _get_all_accounts()

    while True:

        new_username = input("Enter new username: ").strip()

        if any(acc['username'].lower() == new_username.lower() for acc in accounts if
               acc['username'] != current_user['username']):

            print("Username already taken. Please choose another.")

        else:

            break

    current_user['username'] = new_username

    for i, acc in enumerate(accounts):

        if acc['email'] == current_user['email']:  # Use unique identifier to find

            accounts[i] = current_user

            break

    _save_accounts(accounts)

    print(f"Username changed successfully to: {new_username}")


def change_email(current_user: dict):
    """Allows user to change their email."""

    print("\n--- Change Email ---")

    if not _authenticate_user_password(current_user):
        return

    accounts = _get_all_accounts()

    while True:

        new_email = input("Enter new email: ").strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):

            print("Invalid email format. Please try again.")

        elif any(
                acc['email'].lower() == new_email.lower() for acc in accounts if acc['email'] != current_user['email']):

            print("Email already registered. Please choose another.")

        else:

            break

    current_user['email'] = new_email

    for i, acc in enumerate(accounts):

        if acc['username'] == current_user['username']:  # Use unique identifier to find

            accounts[i] = current_user

            break

    _save_accounts(accounts)

    print(f"Email changed successfully to: {new_email}")


def change_password(current_user: dict):
    """Allows user to change their password."""

    print("\n--- Change Password ---")

    if not _authenticate_user_password(current_user):
        return

    while True:

        password_choice = input("Create new password manually (M) or generate automatically (A)? ").strip().upper()

        if password_choice == 'M':

            while True:

                new_password = input("Enter new password (min 16 chars, 1 lower, 1 upper, 1 num, 1 special): ").strip()

                if _check_password_strength(new_password):

                    break

                else:

                    print("Password does not meet strength requirements. Please try again.")

            break

        elif password_choice == 'A':

            new_password = generate_strong_password()

            print(f"Generated new password: {new_password}")

            input("Press Enter to continue after noting your new password...")

            break

        else:

            print("Invalid choice. Please enter 'M' or 'A'.")

    current_user['password_hash'] = _hash_password(new_password)

    accounts = _get_all_accounts()

    for i, acc in enumerate(accounts):

        if acc['username'] == current_user['username']:
            accounts[i] = current_user

            break

    _save_accounts(accounts)

    print("Password changed successfully!")


def view_account_details(current_user: dict):
    """Displays user account balance and details."""

    print("\n--- Account Details ---")

    if not _authenticate_user_password(current_user):
        return

    print(f"Username: {current_user['username']}")

    print(f"Email: {current_user['email']}")

    print(f"Balance: NGN {current_user['balance']:,.2f}")


def reset_balance(current_user: dict):
    """Resets user's wallet balance to zero."""

    print("\n--- Reset Balance ---")

    if not _authenticate_user_password(current_user):
        return

    confirm = input("Are you sure you want to reset your balance to NGN 0.00? (Y/N): ").strip().upper()

    if confirm == 'Y':

        current_user['balance'] = 0.00

        accounts = _get_all_accounts()

        for i, acc in enumerate(accounts):

            if acc['username'] == current_user['username']:
                accounts[i] = current_user

                break

        _save_accounts(accounts)

        print("Your balance has been reset to NGN 0.00.")

    else:

        print("Balance reset cancelled.")


def delete_account(current_user: dict):
    """Permanently deletes the user's account."""

    print("\n--- Delete Account ---")

    if not _authenticate_user_password(current_user):
        return

    confirm = input(
        "Are you absolutely sure you want to delete your account? This action cannot be undone. (Y/N): ").strip().upper()

    if confirm == 'Y':

        accounts = _get_all_accounts()

        accounts = [acc for acc in accounts if acc['username'] != current_user['username']]

        _save_accounts(accounts)

        print("Your account has been successfully deleted.")

        return True  # Indicate an account was deleted

    else:
        print("Account deletion cancelled.")

        return False  # Indicate an account was not deleted


# --- Cart Functions (cart.py) ---

def display_cart(user_cart: dict, inventory: dict):
    """Displays items currently in the user's cart."""

    print("\n--- Your Shopping Cart ---")

    if not user_cart:
        print("Your cart is empty.")

        return

    total_price = 0.0

    print(f"{'Item Name':<30} {'Quantity':<10} {'Price (each)':<15} {'Subtotal':<15}")

    print("-" * 70)

    for item_name, qty in user_cart.items():

        if item_name in inventory:
            price_each = inventory[item_name]['price']

            subtotal = price_each * qty

            total_price += subtotal

            print(f"{item_name:<30} {qty:<10} NGN {price_each:,.2f}   NGN {subtotal:,.2f}")

    print("-" * 70)

    print(f"{'Total:':<55} NGN {total_price:,.2f}")


def add_item_to_cart(user_cart: dict, inventory: dict, item_name: str, quantity: int = 1):
    """Adds an item to the cart and updates inventory."""

    if item_name not in inventory:
        print(f"Error: '{item_name}' not found in inventory.")

        return False

    if inventory[item_name]['quantity'] < quantity:
        print(f"Error: Not enough stock for '{item_name}'. Available: {inventory[item_name]['quantity']}")

        return False

    user_cart[item_name] = user_cart.get(item_name, 0) + quantity

    inventory[item_name]['quantity'] -= quantity

    print(f"'{item_name}' (x{quantity}) added to cart.")

    return True


def remove_item_from_cart(user_cart: dict, inventory: dict, item_name: str, quantity: int = 1):
    """Removes an item from the cart and updates inventory."""

    if item_name not in user_cart:
        print(f"Error: '{item_name}' not in your cart.")

        return False

    if user_cart[item_name] <= quantity:

        inventory[item_name]['quantity'] += user_cart[item_name]  # Return all quantity to inventory

        del user_cart[item_name]

        print(f"'{item_name}' removed from cart.")

    else:

        user_cart[item_name] -= quantity

        inventory[item_name]['quantity'] += quantity

        print(f"Removed {quantity} of '{item_name}' from cart. Remaining: {user_cart[item_name]}")

    return True


def clear_cart(user_cart: dict, inventory: dict):
    """Clears all items from the cart and restores inventory quantities."""

    if not user_cart:
        print("Your cart is already empty.")

        return

    confirm: str = input("Are you sure you want to clear your entire cart? (Y/N): ").strip().upper()

    if confirm == 'Y':

        for item_name, qty in user_cart.items():

            if item_name in inventory:
                inventory[item_name]['quantity'] += qty

        user_cart.clear() #👈to clear the user_cart

        print("Your cart has been cleared 🤗.")

    else:
        print("Cart clear operation cancelled. ❌")


def checkout(user_cart: dict, current_user: dict, inventory: dict) -> bool: #👈 return True / False
    #Here we process the checkout, updates balance, and clears cart.

    if not user_cart:
        print("Your cart is empty. Nothing to checkout.🤳")

        return False

    display_cart(user_cart, inventory)

    total_fee: float = 0.0

    for item_name, qty in user_cart.items():

        if item_name in inventory:
            total_fee += inventory[item_name]['price'] * qty

    print(f"\nTotal checkout price: NGN {total_fee:,.2f}")

    confirm = input("Proceed to payment? (Y/N): ").strip().upper() #👈clear unnecessary space and all letters to CAPITALS.

    if confirm != 'Y':
        print("Checkout cancelled. Returning to Purchase menu.🤳")
        return False

    if current_user['balance'] < total_fee:

        print(f"Insufficient funds!❌ Your current balance is NGN {current_user['balance']:,.2f}.")
        print("Please fund your wallet before attempting to checkout.💰💰💰")

        #revert inventory changes if checkout fails due to insufficient funds (optional, but good practice)

        for item_name, qty in user_cart.items():

            if item_name in inventory:
                inventory[item_name]['quantity'] += qty  #👈Put items back to stock

        user_cart.clear()  #👈Clear cart as items are effectively not purchased
        return False

    #payment process
    current_user['balance'] -= total_fee

    #Update accounts.txt (important for persistence)
    accounts = _get_all_accounts()  #👈Use the function from auth.py

    for i, acc in enumerate(accounts): #👈Go into the account list, one by one and me both.

        if acc['username'] == current_user['username']: #chech if the both are the same
            accounts[i] = current_user
            break #👈stop the loop immediately and jump out!

    _save_accounts(accounts)  #👈Use the function from auth.py

    print("\n--- TRANSACTION SUCCESSFUL! 💰✅😁---")
    print(f"Amount paid: NGN {total_fee:,.2f}")
    print(f"Your new balance: NGN {current_user['balance']:,.2f}")
    print("Thank you for your purchase!🫂🙏")

    user_cart.clear()  #👈Empty cart after successful purchase

    time.sleep(3)  #👈Pause for user to read the message
    return True


#Global variables for current user and inventory
current_user: None = None
inventory = {}  #👈This will store {item_name: {"price": float, "quantity": int}}
user_cart = {}  #👈This will store {item_name: quantity_in_cart}

def main_menu():
    #This menu displays the main login/signup menu.
    while True:

        clear_screen()

        print("="*40)
        print("--- WELCOME TO GROUP 9 MOCK E-COMMERCE APP ❤️❤️❤️ ---")
        print("Where your basic needs are met 😊🥰🤗")
        print("=" * 40)
        print("\n 1. 🔒 Sign In")

        print(" 2. 🔏 Sign Up")

        print(" 3. 👋 Exit Program")

        option = input("\n Enter your choice: ").strip() #👈 means remove any space from the beginning of the word.

        if option == '1':

#use the variable current_user that was created outside this function, if changed? implement it in the program
            global current_user

            current_user = sign_in()

            if current_user:
                run_section()  #👈Go to the main application
                current_user = None  #👈Log out after run section exits

        elif option == '2':
            sign_up()

        elif option == '3':
            print("Exiting the program. Goodbye!👋👋👋")
            time.sleep(1) #👈 wait for 1 second before disappearing.

            break #👈stop the loop immediately and jump out!

        else:
            print("Wrong option. Please try again.🤗")
            time.sleep(1) #👈 wait for 1 second before disappearing.


def run_section():
    #Here is the main section after the successful login.

    global inventory

    inventory = load_inventory_from_files()  # Load inventory once user logs in

    while True:

        clear_screen()

        print(f"--- Welcome, {current_user['username']}! ---")
        print(f"Current Balance: NGN {current_user['balance']:,.2f}")
        print("="*40)
        print("\n--- Run Section ---")

        print("1. Fund Wallet")

        print("2. Make Purchases")

        print("3. Manage Account")

        print("4. Exit Program (Logout)")

        choice = input("Enter your choice: ").strip()

        if choice == '1':

            fund_wallet(current_user)

        elif choice == '2':

            purchase_menu()

        elif choice == '3':

            manage_account_menu()

            # If deleted or user logged out, current_user will be None, so break

            if current_user is None:
                break

        elif choice == '4':

            print("\nLogging you out securely...")

            print("Thank you for using our e-commerce app dear. We hope to see you again soon! 👋👋")

            time.sleep(2) #👈 means pause the program for 2 seconds.

            break  # 👈 Exit run_section, returning to main_menu

        else:

            print("Wrong option ❌. Please try again 🤗.")

        time.sleep(1)


def purchase_menu():
    """This menu handles product search, cart management, and checkout."""

    while True:
        clear_screen()
        print("-"*50)
        print("\n--- PURCHASE MENU ---")
        print("1. Search Items")
        print("2. Manage Cart")
        print("3. Checkout")
        print("4. Exit Purchase Menu")

        option: str = input("Enter your any option: ").strip() #👈 means remove any space from the beginning of the word.

        if option == '1':

            handle_search_items()

        elif option == '2':

            manage_cart_menu()

        elif option == '3':

            # we check if checkout was successful and the cart is empty before breaking
            if checkout(user_cart, current_user, inventory):

                # Break if checkout was successful (cart empty)
                break

        elif option == '4':

            print("You're leaving the Purchase Menu.")

            time.sleep(1) #👈 means pause the program for 1 second.

            break

        else:

            print("Invalid choice. Please try again.")

        time.sleep(1) #👈 means pause the program for 1 second.


def handle_search_items():
    """Here Manages the search functionality and post-search options."""

    while True:

        clear_screen() #👈 means to clean everything off the screen.

        query: str = input("Enter item name or brand to search (e.g., 'Apple Watch'): ").strip()

        matched_items_tuples: list[tuple[str, float]] = search_inventory(query, inventory)

        #convert tuples to a list of dicts for easier manipulation
        # and filter out items with 0 quantity

        available_matched_items: list = [] #👈 this is the list that will contain all the items.

        for name, price in matched_items_tuples: #👈 Go through the list one by one, give me the name / price.

            if inventory[name]['quantity'] > 0:
                available_matched_items.append({"name": name, "price": price, "quantity": inventory[name]['quantity']})

        if not available_matched_items:

            print(f"sorry {name} items matched your query or are currently out of stock.")

        else:
            print("\n--- Matched Items ---")

            for i, item in enumerate(available_matched_items):
                print(f"{i + 1}. {item['name']} - NGN {item['price']:,.2f} (Stock: {item['quantity']})")

        print("\n--- Search Options ---")

        print("1. Search Again")

        print("2. Add Item(s) to Cart")

        print("3. Exit Search Menu")

        search_choice = input("Enter your choice: ").strip()

        if search_choice == '1':

            continue  # Loop to search again

        elif search_choice == '2':

            if not available_matched_items:
                print("No items to add. Please search again.")

                time.sleep(1)

                continue

            while True:

                try:

                    item_num = int(input("Enter the number of the item to add to cart (or 0 to finish adding): "))

                    if item_num == 0:
                        break

                    if 1 <= item_num <= len(available_matched_items):

                        selected_item = available_matched_items[item_num - 1]

                        # Ask for quantity to add

                        while True:

                            try:

                                qty_to_add = int(input(
                                    f"How many '{selected_item['name']}' do you want to add (max {selected_item['quantity']})? "))

                                if qty_to_add <= 0:

                                    print("Quantity must be positive.")

                                elif qty_to_add > selected_item['quantity']:

                                    print(f"Only {selected_item['quantity']} available. Please enter a lower quantity.")

                                else:

                                    add_item_to_cart(user_cart, inventory, selected_item['name'], qty_to_add)

                                    break

                            except ValueError:

                                print("Invalid quantity. Please enter a number.")



                    else:

                        print("Invalid item number.")

                except ValueError:

                    print("Invalid input. Please enter a number.")

            # After adding, give option to continue adding or go back to main search options

            input("Press Enter to continue...")

        elif search_choice == '3':

            break  # Exit search loop, return to purchase_menu

        else:

            print("Invalid choice. Please try again.")

        time.sleep(1)


def manage_cart_menu():
    """Handles viewing, adding, removing, and clearing items from the cart."""

    while True:

        clear_screen()

        display_cart(user_cart, inventory)  # Always show cart first

        print("\n--- Manage Cart Menu ---")

        print("1. View Items in Cart (already displayed)")

        print("2. Add More Items to Cart (from inventory)")

        print("3. Remove Item(s) from Cart")

        print("4. Clear Cart")

        print("5. Exit Manage Cart Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':

            input("Press Enter to continue...")

        elif choice == '2':

            # This option allows adding by exact name or by selecting from a list of all available

            print("\n--- Add More Items to Cart ---")

            all_available_items = [name for name, details in inventory.items() if details['quantity'] > 0]

            if not all_available_items:
                print("No items currently available to add.")

                time.sleep(1)

                continue

            print("Available Items:")

            for i, item_name in enumerate(all_available_items):
                print(
                    f"{i + 1}. {item_name} - NGN {inventory[item_name]['price']:,.2f} (Stock: {inventory[item_name]['quantity']})")

            while True:

                try:

                    item_num_to_add = int(input("Enter the number of the item to add (0 to cancel): "))

                    if item_num_to_add == 0:
                        break

                    if 1 <= item_num_to_add <= len(all_available_items):

                        selected_item_name = all_available_items[item_num_to_add - 1]

                        available_qty = inventory[selected_item_name]['quantity']

                        while True:

                            try:

                                qty_to_add = int(input(
                                    f"How many '{selected_item_name}' do you want to add (max {available_qty})? "))

                                if qty_to_add <= 0:

                                    print("Quantity must be positive.")

                                elif qty_to_add > available_qty:

                                    print(f"Only {available_qty} available. Please enter a lower quantity.")

                                else:

                                    add_item_to_cart(user_cart, inventory, selected_item_name, qty_to_add)

                                    break  # Break from inner qty loop

                            except ValueError:

                                print("Invalid quantity. Please enter a number.")

                        break  # Break from outer item selection loop

                    else:

                        print("Invalid item number.")

                except ValueError:

                    print("Invalid input. Please enter a number.")

            time.sleep(1)



        elif choice == '3':

            print("\n--- Remove Items ---")

            if not user_cart:
                print("Your cart is empty. Nothing to remove.")

                time.sleep(1)

                continue

            # Re-display cart with numbers for removal

            print(f"{'No.':<5} {'Item Name':<30} {'Quantity':<10}")

            print("-" * 45)

            cart_items_list = list(user_cart.keys())

            for i, item_name in enumerate(cart_items_list):
                print(f"{i + 1:<5} {item_name:<30} {user_cart[item_name]:<10}")

            while True:

                try:

                    item_num_to_remove = int(input("Enter the number of the item to remove (0 to cancel): "))

                    if item_num_to_remove == 0:
                        break

                    if 1 <= item_num_to_remove <= len(cart_items_list):

                        item_name = cart_items_list[item_num_to_remove - 1]

                        qty_in_cart = user_cart[item_name]

                        while True:

                            try:

                                qty_to_remove = int(input(
                                    f"How many '{item_name}' do you want to remove (current in cart: {qty_in_cart})? "))

                                if qty_to_remove <= 0:

                                    print("Quantity must be positive.")

                                elif qty_to_remove > qty_in_cart:

                                    print(f"You only have {qty_in_cart} of this item in your cart.")

                                else:

                                    remove_item_from_cart(user_cart, inventory, item_name, qty_to_remove)

                                    break  # Break from inner qty loop

                            except ValueError:

                                print("Invalid quantity. Please enter a number.")

                        break  # Break from outer item selection loop

                    else:

                        print("Invalid item number.")

                except ValueError:

                    print("Invalid input. Please enter a number.")

            time.sleep(1)



        elif choice == '4':

            clear_cart(user_cart, inventory)

            time.sleep(1)

        elif choice == '5':

            print("Exiting Manage Cart Menu.")

            time.sleep(1)

            break

        else:

            print("Invalid choice. Please try again.")
        time.sleep(1)


def manage_account_menu():
    #This section handles all account management functionalities.

    global current_user

    while True:
        clear_screen()

        print("="*40)
        print("\n--- MANAGE ACCOUNT MENU 👨‍💼🫂 ---")
        print("=" * 40)

        print("1. Change Username 👤")
        print("2. Change Email 📩")
        print("3. Change Password 🔑")
        print("4. View Account Balance/Details🧾")
        print("5. Reset Balance 🧾")
        print("6. Delete Account ❌")
        print("7. Logout ✅")
        print("8. Exit Manage Account Menu ❌")

        option: str = input("Kindly enter your choice 🫴: ").strip() #remove unnecessary space.

        if option == '1':
            change_username(current_user)

        elif option == '2':
            change_email(current_user)

        elif option == '3':
            change_password(current_user)

        elif option == '4':
            view_account_details(current_user)

        elif option == '5':
            reset_balance(current_user)

        elif option == '6':
            if delete_account(current_user):
                current_user = None  #👈Set current_user to None if an account is deleted

                print("You have been logged out.")
                time.sleep(2) #👈Pause for user to read a message

                return  #👈Exit this menu and run_section

        elif option == '7':
            print("\nLogging out 📤...")
            print("You have been securely logged out. ✅✅✅")

            time.sleep(2) #👈Pause for user to read a message
            current_user = None  #👈Clear current user on logout

            return  #👈Exit this menu and run_section

        elif option == '8':
            print("Exiting Manage Account Menu.")

            time.sleep(1) #👈Pause for user to read a message

            break #👈stop the loop immediately and jump out!

        else:
            print("Wrong option,❌ Please try again.🤗")
        time.sleep(1)  #👈Pause for user to read a message


if __name__ == "__main__": #👈only run this part if the file is being run directly, not if it's being imported.
    setup_data_storage()  #👈Ensure data directory and accounts.txt exist
    main_menu()