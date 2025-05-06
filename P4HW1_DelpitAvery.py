# Avery Delpit
# 03/24/2025
# P4HW1 - User Score Input Validation for Grades
# This program takes a number grade and outputs a letter grade to the student from inputted scores within this program.

# Ask user for the number of scores they want to enter
num_scores = int(input("How many scores would you like to enter?"))

# Validate the number of scores
while num_scores <= 0:
    print("Invalid number of scores entered!!!. Please enter a number greater than 0.")
    num_scores = int(input("How many scores would you like to enter? "))

# Initialize an empty list to store valid scores
scores = []

# Loop to collect scores
score_number = 1  # Counter to track the score number
for score in range(num_scores):
    score = -1  # Initialize score with an invalid value
    while score < 0 or score > 100:  # Continue until a valid score is entered
        score = int(input(f"Enter score #{score_number}: "))  # Use the counter for score number
        if score < 0 or score > 100:
            print("Invalid score entered!!!. Please enter a score between 0 and 100.")
    scores.append(score)  # Add the valid score to the list
    score_number += 1  # Increase by 1 to track the next score number

# Calculate results of the scores
lowest_score = min(scores)
scores.remove(lowest_score)  # Remove the lowest score from the list 
average_score = sum(scores) / len(scores)  # Calculate average of modified list of scores entered 

# Determine letter grade based on average score
if average_score >= 90:
    letter_grade = "A"
elif average_score >= 80:
    letter_grade = "B"
elif average_score >= 70:
    letter_grade = "C"
elif average_score >= 60:
    letter_grade = "D"
else:
    letter_grade = "F"

# Display results
print(".-.-.-.-.-.-.Results.-.-.-.-..-.-.-.-:")
print(f"Lowest Score  : {lowest_score}")
print(f"Modified List : {scores}")
print(f"Scores Average: {average_score:.2f}")
print(f"Grade         : {letter_grade}")
print(".-What a great job! Remember Perfection is not attainable, but the striving for perfection is honorable-.")
print(".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")

