# Avery Delpit
# 03/26/2025
# P4HW2 - This program will calculate the gross pay for multiple employees to build onto the previous program.

# Initialize totals and employee counter
total_ot_pay = 0
total_reg_hour_pay = 0
total_gross_pay = 0
employee_count = 0

while True:
    # Ask for employee name
    employee_name = input("Enter the employee's name or 'Done' to terminate: ")
    if employee_name.lower() == "done":
        break

    # Get hours worked and pay rate
    hours_worked = float(input("Enter the number of hours worked: "))
    pay_rate = float(input("Enter employee's pay rate: "))

    # Calculate regular and overtime pay
    if hours_worked <= 40:
        reg_hour_pay = hours_worked * pay_rate
        ot_hours = 0
        ot_pay = 0
    else:
        reg_hour_pay = 40 * pay_rate
        ot_hours = hours_worked - 40
        ot_pay = ot_hours * (pay_rate * 1.5)

    # Calculate gross pay
    gross_pay = reg_hour_pay + ot_pay

    # Update totals
    total_ot_pay += ot_pay
    total_reg_hour_pay += reg_hour_pay
    total_gross_pay += gross_pay
    employee_count += 1

    # Display individual employee's details
    print("--------------------------------------------------")
    print(f"Employee name: {employee_name}")
    print()
    print("Hours Worked    Pay Rate    OverTime    OverTime Pay    RegHour Pay    Gross Pay")
    print("--------------------------------------------------------------------------------")
    print(f"{hours_worked:6.2f}        {pay_rate:6.2f}        {ot_hours:6.2f}        {ot_pay:6.2f}        {reg_hour_pay:6.2f}        {gross_pay:6.2f}")

# Display totals after all employees are entered
print("--------------------------------------------------")
print("Summary of all employees:")
print(f"Total number of employees entered: {employee_count}")
print(f"Total Overtime Pay: ${total_ot_pay:.2f}")
print(f"Total Regular Hour Pay: ${total_reg_hour_pay:.2f}")
print(f"Total Gross Pay: ${total_gross_pay:.2f}")
print("--------------------------------------------------")

# Display totals after federal and state taxes are taken out
state_tax = float(input("Enter the state tax rate (as a decimal, e.g., 0.05 for 5%): "))
federal_tax = float(input("Enter the federal tax rate (as a decimal, e.g., 0.10 for 10%): "))
federal_tax_total = total_gross_pay * federal_tax
state_tax_total = total_gross_pay * state_tax
net_pay = total_gross_pay - (federal_tax_total + state_tax_total)

# Calculate and display tax summary
print("--------------------------------------------------")
print("Summary of all employees after taxes:")
print(f"Total number of employees entered: {employee_count}")
print(f"Total Overtime Pay: ${total_ot_pay:.2f}")
print(f"Total Regular Hour Pay: ${total_reg_hour_pay:.2f}")
print(f"Total Gross Pay: ${total_gross_pay:.2f}")
print(f"Federal Tax Total: ${federal_tax_total:.2f}")
print(f"State Tax Total: ${state_tax_total:.2f}")
print(f"Net Pay After Taxes: ${net_pay:.2f}")
print("--------------------------------------------------")