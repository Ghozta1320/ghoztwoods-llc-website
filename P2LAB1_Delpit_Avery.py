#   Avery Delpit
#   02/17/2024
#   P2HW1
#   Calculating the area and circumference of a pizza based on the radius and diameter

Radius = float(input("Enter the radius of the pizza in inches: "))
Diameter = float(input("Enter the diameter of the pizza in inches: "))
circrumference = 2 * 3.14 * Diameter
area = 3.14 * (Diameter**2)

print(f'The circumference of the pizza is: {circrumference:2.2f}')
print(f'The area of the pizza is: {area:2.2f}')
print(f'The radius of the pizza is: {Radius:2.2f}')
print(f'The diameter of the pizza is: {Diameter:2.2f}')