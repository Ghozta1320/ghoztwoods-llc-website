# Avery Delpit
# 02/24/2024
# P3LAB
# This program allows the user to enter a money (float) value with two places after the decimal. The program will then display the value of the money entered in a sentence.

# Get user input
money = float(input("Enter a value in dollars and cents as a float: "))

# Display the value of the money entered
cents = int(money * 100)
print("The value of", money, "is", cents, "cents.")

# Calculate the number of dollars, quarters, dimes, nickels, and pennies
dollars = int(money)
cents = int((money - dollars) * 100)
quarters = cents // 25
dimes = (cents % 25) // 10
nickels = (cents % 10) // 5
pennies = cents % 5

# Display the number of dollars, quarters, dimes, nickels, and pennies
print(f'Dollars:, {dollars:2.2f}')
print(f'Quarters:, {quarters:2.2f}')
print(f'Dimes:, {dimes:2.2f}')
print(f'Nickels:, {nickels:2.2f}')
print(f'Pennies:, {pennies:2.2f}')

# Display the total number of coins
total_coins = quarters + dimes + nickels + pennies
print(f'Total coins:, {total_coins:2.2f}')

if total_coins == 1:
    print(f'Total coins:, {total_coins:2.2f}')
else:
    print(f'Total coins:, {total_coins:2.2f}')

# Display the total value of the coins
total_value = quarters * 0.25 + dimes * 0.10 + nickels * 0.05 + pennies * 0.01
print(f'Total value:, {total_value:2.2f}')

if total_value == 1:
    print(f'Total value:, {total_value:2.2f}')
else:
    print(f'Total value:, {total_value:2.2f}')