# Define the cars_mpg dictionary
cars_mpg = {
    "Camry": 52.36,
    "2015 Mercedes Benz E400": 20.82,
    "Tesla Model S": 104.44,
    "Chevrolet Silverado 1500": 17.89
}

# Display available car models
print(cars_mpg.keys())

# Get user input for car model
car_model = input("Enter a vehicle to see its mpg: ")

# Retrieve MPG value
mpg = cars_mpg.get(car_model)

# Print the car model and its MPG
print("The", car_model, "gets", mpg, "mpg.")

# Get user input for distance
distance = float(input("How many miles will you drive the " + car_model + "? "))

# Calculate gallons needed
gallons_needed = distance / mpg

# Print the result
print("{:.2f}".format(gallons_needed), "gallon(s) of gas are needed to drive the", car_model, distance, "miles.")