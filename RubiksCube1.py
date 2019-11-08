def init_cube () :

    def init_square (color, side, row, column) :
        # cube of 6 sides/colors
        cube = [color, side, row, column]
        return cube

    squares = []
    color = None
    side = -1
    row = None
    column = None

    for color in ['white', 'green', 'red', 'blue', 'orange', 'yellow'] :
        side = side + 1
        for row in [0, 1, 2] :
            for column in [0, 1, 2] :
                squares.append(init_square(color, side, row, column))
    return squares


def draw_side(cube, side) :

    def draw_square(s) :
        x_start = 50
        y_start = 50
        size = 200
        space = 10

        color = s[0]
        row = s[2]
        column = s[3]

        x1 = x_start + (column * (space + size))
        y1 = y_start + (row * (space + size))

        x2 = x1 + size
        y2 = y1 + size

        sqr = Rectangle(Point(x1, y1), Point(x2,y2))
        sqr.setFill(color)
        sqr.draw(win)


    for square in cube :
        if square[1] == side :
            draw_square(square)


import graphics
from graphics import *

# init
cube = []
cube = init_cube()

# draw white side of cube
win = GraphWin("Rubik's Cube Solver", 720, 720)

# show side
err_msg = 'Please enter a number between 0 and 5'

while True :
    inp = input('Enter side (0-6):')

    if inp == 'done' :
        win.close()
        exit()
    try :
        side = int(inp)
    except :
        print(err_msg)

    if side >= 0 and side <= 5 :
        draw_side(cube, side)
    else :
        print(err_msg)

