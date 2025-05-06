import random 

def make_change(change):
    change = int(change * 100)

    print("Change to be given: ", change, " cents")
    coins = [100, 50, 25, 10, 5, 1]

    if change == 0:
        return 0
    elif change < 0:
        return -1
    else:
        coin_count = 0
        for coin in coins:
            while change >= coin:
                change -= coin
                coin_count += 1
        return coin_count

def main():
    change = float(input("Enter the amount of change to be given: "))
    coin_count = make_change(change)
    print("Number of coins to be given: ", coin_count)

if __name__ == "__main__":
    main()
    