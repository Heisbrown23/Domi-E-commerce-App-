import os
from auth import _get_all_accounts, _save_accounts, _hash_password, _check_password_strength, generate_strong_password

ACCOUNTS_FILE = os.path.join("data", "accounts.txt")

def _authenticate_user_password(current_user: dict) -> bool:
    """check password and verifies it against the current user's password."""

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

        return True  # Indicate account was deleted

    else:

        print("Account deletion cancelled.")

        return False  # Indicate account was not deleted