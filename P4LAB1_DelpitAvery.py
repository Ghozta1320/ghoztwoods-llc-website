# Avery Delpit
# 03/19/2025
# P4LAB1_DelpitAvery 


import turtle

# Create the screen
win = turtle.Screen()
win.title("Avery's Pentagon")
win.setup(width=800, height=600)
win.bgcolor("black")


# Create the turtle
t = turtle.Turtle()
t.pensize(5)
t.color("gold")
t.speed(1)
t.penup()
t.goto(-50, 0)
t.pendown() 

# For loop that runs x amount of times to create the pentagon
for i in range(5):
    t.forward(100)
    t.right(72)

# While Loop that creates the Star
while True:
    t.forward(100)
    t.right(144)
    if abs(t.pos()) < 1:
        break



win.mainloop(10)


