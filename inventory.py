""" This module manages the product inventory which will be responsible for loading items from warehouse*.txt files, parsing them,
and providing functions to search and update item quantities."""
import os
import re
DATA_DIR = "data"



def load_inventory_from_files() -> dict:
    """ this function is just telling it to load items from all warehouse*.txt files in the data directory whereby
    it returns a dictionary where keys are item names and values are dictionaries
    containing 'price' and 'quantity'.
    """
    inventory = {}

    for filename in os.listdir(DATA_DIR):

        if filename.startswith("warehouse") and filename.endswith(".txt"):

            filepath = os.path.join(DATA_DIR, filename)

            try:

                with open(filepath, 'r') as f: """just open the file and read it"""

                    content = f.read().strip()

                    if not content:

                        continue

                    items_str = content.split(';')

                    for item_str in items_str:

                        if ':' in item_str:

                            name, price_str = item_str.strip().split(':', 1)

                            try:

                                price = float(price_str)

                                # Assuming initial quantity for each item is 1 for simplicity

                                # You might need to adjust this based on how stock is defined.

                                # For a mock app, a simple quantity might suffice.

                                inventory[name] = {"price": price, "quantity": 10} # Placeholder quantity

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



# Example Usage (for testing)

# if __name__ == "__main__":

#     setup_data_storage() # Make sure data directory and files exist for testing

#     # Create dummy warehouse files for testing

#     with open(os.path.join(DATA_DIR, "warehouse1.txt"), "w") as f:

#         f.write("Apple iPhone 14:1000000;Samsung Galaxy S23:800000")

#     with open(os.path.join(DATA_DIR, "warehouse2.txt"), "w") as f:

#         f.write("Google Pixel 7:700000;Apple Watch Series 8:400000")



#     all_items = load_inventory_from_files()

#     print("Loaded Inventory:", all_items)



#     matched = search_inventory("Apple Watch", all_items)

#     print("Matched items (Apple Watch):", matched)