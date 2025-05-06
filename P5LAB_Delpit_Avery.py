# Avery Delpit
# 03/31/2025
# P5LAB - This program builds on P3LAB with the addition of a function that will disperse change to the customer

import random

# Function to disperse change
def disperse_change(change):
    # Convert change to cents
    cents = int(change * 100)

    # Calculate the number of dollars, quarters, dimes, nickels, and pennies
    dollars = cents // 100
    cents %= 100
    quarters = cents // 25
    cents %= 25
    dimes = cents // 10
    cents %= 10
    nickels = cents // 5
    pennies = cents % 5

    # Display the number of dollars, quarters, dimes, nickels, and pennies
    print(f"Dollars: {dollars}")
    print(f"Quarters: {quarters}")
    print(f"Dimes: {dimes}")
    print(f"Nickels: {nickels}")
    print(f"Pennies: {pennies}")

# Main function
def main():
    # Generate a random float value for the total owed
    total_owed = round(random.uniform(0.01, 100.00), 2)
    print(f"Total owed: ${total_owed}")

    # Prompt the user to enter the amount of cash they will put into the self-checkout
    amount_paid = float(input("Enter the amount of cash you will put into the self-checkout: $"))

    # Calculate the amount of change owed to the customer
    if amount_paid < total_owed:
        print("Insufficient payment. Please enter an amount greater than or equal to the total owed.")
        return
    change = round(amount_paid - total_owed, 2)
    print(f"Change owed: ${change}")

    # Call the disperse_change function
    disperse_change(change)

# Call the main function
if __name__ == "__main__":
    main()