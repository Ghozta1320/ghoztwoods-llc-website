# Avery Delpit
# 02/24/2024  
# P2HW2
# This program will calculate the grade for Modules 1 - 6 to include the total, average, lowest, and highest grades.

# Get student input for grades for Modules 1 - 6
module1 = float(input("Enter grade for Module 1: "))
module2 = float(input("Enter grade for Module 2: "))
module3 = float(input("Enter grade for Module 3: "))
module4 = float(input("Enter grade for Module 4: "))
module5 = float(input("Enter grade for Module 5: "))
module6 = float(input("Enter grade for Module 6: "))

# Calculate the total and average 
total = module1 + module2 + module3 + module4 + module5 + module6
average = total / 6

# Find the lowest and highest grades 
grades = [module1, module2, module3, module4, module5, module6]
lowest_grade = min(grades)
highest_grade = max(grades)

# Print the results to the student 
print("\nGrades Summary")
print("==============")
print(f"Module 1: {module1}")
print(f"Module 2: {module2}")
print(f"Module 3: {module3}")
print(f"Module 4: {module4}")
print(f"Module 5: {module5}")
print(f"Module 6: {module6}")
print("=======Results=======")
print(f"{'Total:':<20} {total}")
print(f"{'Average:':<20} {average:.2f}")
print(f"{'Lowest Grade:':<20} {lowest_grade}")
print(f"{'Highest Grade:':<20} {highest_grade}")
if average >= 70:
    print("=========You passed============")
else:
    print("=========You failed============")
