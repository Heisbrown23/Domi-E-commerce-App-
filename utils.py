"""This module will be used across different parts of the application
for example input validation, clear screen, display messages."""

import os
DATA_DIR = "data"

ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.txt")
def setup_data_storage():

    """here we check if the 'data' directory and 'accounts.txt' file exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:

            pass # Create an empty accounts.txt file

        print(f"Created file: {ACCOUNTS_FILE}")

#we Call this at the start of your main application
# setup_data_storage()