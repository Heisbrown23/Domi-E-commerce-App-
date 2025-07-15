import os

import time


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

    confirm = input("Are you sure you want to clear your entire cart? (Y/N): ").strip().upper()

    if confirm == 'Y':

        for item_name, qty in user_cart.items():

            if item_name in inventory:
                inventory[item_name]['quantity'] += qty

        user_cart.clear()

        print("Your cart has been cleared.")

    else:

        print("Cart clear operation cancelled.")


def checkout(user_cart: dict, current_user: dict, inventory: dict) -> bool:
    """Processes the checkout, updates balance, and clears cart."""

    if not user_cart:
        print("Your cart is empty. Nothing to checkout.")

        return False

    display_cart(user_cart, inventory)

    total_fee = 0.0

    for item_name, qty in user_cart.items():

        if item_name in inventory:
            total_fee += inventory[item_name]['price'] * qty

    print(f"\nTotal checkout price: NGN {total_fee:,.2f}")

    confirm = input("Proceed to payment? (Y/N): ").strip().upper()

    if confirm != 'Y':
        print("Checkout cancelled. Returning to Purchase menu.")

        return False

    if current_user['balance'] < total_fee:

        print(f"Insufficient funds! Your current balance is NGN {current_user['balance']:,.2f}.")

        print("Please fund your wallet before attempting to checkout.")

        # Revert inventory changes if checkout fails due to insufficient funds (optional, but good practice)

        for item_name, qty in user_cart.items():

            if item_name in inventory:
                inventory[item_name]['quantity'] += qty  # Put items back to stock

        user_cart.clear()  # Clear cart as items are effectively not purchased

        return False

    # Process payment

    current_user['balance'] -= total_fee

    # Update accounts.txt (important for persistence)

    from auth import _get_all_accounts, _save_accounts

    accounts = _get_all_accounts()

    for i, acc in enumerate(accounts):

        if acc['username'] == current_user['username']:
            accounts[i] = current_user

            break

    _save_accounts(accounts)

    print("\n--- Transaction Successful! ---")

    print(f"Amount paid: NGN {total_fee:,.2f}")

    print(f"Your new balance: NGN {current_user['balance']:,.2f}")

    print("Thank you for your purchase!")

    user_cart.clear()  # Empty cart after successful purchase

    time.sleep(2)  # Pause for user to read message

    return True