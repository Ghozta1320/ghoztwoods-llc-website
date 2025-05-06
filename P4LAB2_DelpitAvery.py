# Avery Delpit
# 03/19/2025
#P4LAB2_DelpitAvery

#Create the variable to control while loop
run_again = 'yes'


#While loop
while run_again != 'no':
    # Get interger from user
    user_num = int(input("Enter an integer: "))
    if user_num < 0:
        print('Negative numbers are not allowed')
    else: # user input is 0 or greater
        for i in range(1, 101):
            print(f'{user_num} x {i} = {user_num * i}') # print
        run_again = input('Do you want to run again? (yes/no): ')
        if run_again == 'no': 
            break  # Exit the for loop if the user decides to choose 'no'
print('Thank you for using the program!')

# While loop ends here
print('The program has ended successfully')
                    