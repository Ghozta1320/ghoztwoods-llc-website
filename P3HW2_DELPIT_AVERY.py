# DATE: 03/05/2025
# CTI-110 P3HW2 - EMPLOYEE PAY 
# Avery Delpit

# THIS PROGRAM CALCULATES THE GROSS PAY FOR AN EMPLOYEE BASED ON HOURS WORKED

# Get the employee's details.
employee_name = input("Enter the employee's name: ")
hours_worked = float(input("Enter the number of hours worked: "))
pay_rate = float(input("Enter employee's pay rate: "))

# Calculate the gross pay for regular hours worked
if hours_worked <= 40:
    reg_hour_pay = hours_worked * pay_rate
    ot_hours = 0
    ot_pay = 0
else:
    reg_hour_pay = 40 * pay_rate
    ot_hours = hours_worked - 40
    ot_pay = ot_hours * (pay_rate * 1.5)

# Calculate the total gross pay
gross_pay = reg_hour_pay + ot_pay

# Display the employee's details and pay information
print("----------------------------------------")
print("Employee name: ", employee_name)
print()
print("Hours Worked    Pay Rate    OverTime    OverTime Pay    RegHour Pay    Gross Pay")
print("--------------------------------------------------------------------------------")
print(f"{hours_worked:<15}{pay_rate:<12}{ot_hours:<12}{ot_pay:<15.2f}{reg_hour_pay:<15.2f}{gross_pay:<.2f}")
