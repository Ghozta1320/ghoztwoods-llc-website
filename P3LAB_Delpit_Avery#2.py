# Avery Delpit
# 02/24/2024
# P3LAB
# This program allows the user to enter a money (float) value with two places after the decimal.
# The program will then display the value of the money entered in a sentence and calculate the most efficient number of dollars, quarters, dimes, nickels, and pennies needed to make the given amount of money.

# Get user input
money = float(input("Enter a value in dollars and cents as a float: "))

# Convert the amount to cents
cents = int(money * 100)

# Calculate the number of dollars, quarters, dimes, nickels, and pennies
dollars = cents // 100
cents %= 100
quarters = cents // 25
cents %= 25
dimes = cents // 10
cents %= 10
nickels = cents // 5
pennies = cents % 5

# Display the value of the money entered
print(f"The value of {money} is ${money:.2f}")

# Display the breakdown of the amount
if dollars > 0:
    print(f"{dollars} dollar{'s' if dollars > 1 else ''}")
if quarters > 0:
    print(f"{quarters} quarter{'s' if quarters > 1 else ''}")
if dimes > 0:
    print(f"{dimes} dime{'s' if dimes > 1 else ''}")
if nickels > 0:
    print(f"{nickels} nickel{'s' if nickels > 1 else ''}")
if pennies > 0:
    print(f"{pennies} penn{'ies' if pennies > 1 else 'y'}")

elif quarters == 0 and dimes == 0 and nickels == 0 and pennies == 0:
    print("No coins needed")
if dollars == 0 and quarters == 0 and dimes == 0 and nickels == 0 and pennies == 0:
    print("No coins needed")

# Display the total number of coins
total_coins = quarters + dimes + nickels + pennies
print(f"Total coins: {total_coins}")
