# RubikCube.py

# Simple Rubik's Cube solver developed by Phyllip Hall to learn
# and test understanding of Python

# Version 2   10/31/19
#     * made cubes more realistic with simulated black space between cubelets
#     * added mini cubes to show all 6 faces simultaneously
#     * changed cube data structure to use alphanumerics for "side"

# Version 1   10/30/19
# initializes 6-sided cube, draws single side specified by user via command line

from graphics import *

def get_side_name_short(i) :
    side_family = side_names[i]
    return side_family[0]

def get_side_name_long(side_name_short) :
    for i in range(len(side_names)) :
        side_family = side_names[i]
        if side_name_short == side_family[0] :
            return side_family[1]


def init_cube () :

    def init_square (color, side, row, column) :
        # cube of 6 sides/colors
        cube = [color, side, row, column]
        return cube

    # init_cube
    squares = []
    colors = ['green', 'blue', 'white', 'yellow', 'orange', 'red']

    for i in range(len(side_names)) :
        side = get_side_name_short(i)
        color = colors[i]
        for row in [0, 1, 2] :
            for column in [0, 1, 2] :
                squares.append(init_square(color, side, row, column))

    return squares


def draw_cube(win, cube) :

    def draw_side(win, cube, side, x_start, y_start, size) :

        def draw_square(win, square, x_start, y_start, size) :
            outer_border = 1  # btw outer box
            inner_border = 2 # btw inner and outer boxes

            color = square[0]
            side = get_side_name_long(square[1])
            row = square[2]
            column = square[3]

            # label
            label = Text(Point((x_start + (3 * size / 2)), y_start), side)
            label.setSize(20)
            label.setStyle('normal')
            label.draw(win)
            y_start += 15

            # actual start
            x_start += (column * size)
            y_start += (row * size)

            # outer black square
            px1 = x_start + outer_border
            py1 = y_start + outer_border

            px2 = x_start + size - outer_border
            py2 = y_start + size - outer_border

            sqr = Rectangle(Point(px1, py1), Point(px2, py2))
            sqr.setFill('black')
            sqr.draw(win)

            # inner colored square
            px1 = px1 + inner_border
            py1 = py1 + inner_border

            px2 = px2 - inner_border
            py2 = py2 - inner_border
            sqr = Rectangle(Point(px1, py1), Point(px2, py2))
            sqr.setFill(color)
            sqr.draw(win)

        # draw_side
        for square in cube :
            if square[1] == side:
                draw_square(win, square, x_start, y_start, size)


    # draw_cube
    square_size = 50
    space_btw_squares = 50

    x_start_drawing = 25
    y_start_drawing = 25

    x_start_cube = x_start_drawing
    y_start_cube = y_start_drawing

    for i in range(len(side_names)):
        if i in [1, 3, 5] :
            x_start_cube += 3 * square_size + space_btw_squares
        elif i in [2, 4] :
            x_start_cube = x_start_drawing
            y_start_cube += 3 * square_size + space_btw_squares

        side_name_short = get_side_name_short(i)
        draw_side(win, cube, side_name_short, x_start_cube, y_start_cube, square_size)




# RUN PROGRAM
side_names = (['f', 'Front'], ['b', 'Back'], ['u', 'Up'], ['d', 'Down'], ['l', 'Left'], ['r', 'Right'])

# init
cube = init_cube()

win = GraphWin("Rubik's Cube Solver", 420, 650)

# draw initialized cube
draw_cube(win, cube)

# pause before closing window
win.getMouse()  # Pause to view result

