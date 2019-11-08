# RubikCube.py

# Simple Rubik's Cube solver developed by Phyllip Hall to learn
# and test understanding of Python

# Version 3   11/1/19
#     * added comments to better organize code
#     * added all (18) 1/4 turn movements and ability to accept and execute a list of moves
#     * added cube scrambler
#     * allowed a stream of commands to sent to the mover

# Version 2   10/31/19
#     * made cubes more realistic with simulated black space between cubelets
#     * added mini cubes to show all 6 faces simultaneously
#     * changed cube data structure to use alphanumerics for "side"

# Version 1   10/30/19
# initializes 6-sided cube, draws single side specified by user via command line

from graphics import *
import random

##########################################################################
# global variables and funtions

side_names = (['f', 'Front'], ['b', 'Back'], ['u', 'Up'], ['d', 'Down'], ['l', 'Left'], ['r', 'Right'])

def get_side_name_short(i) :
    side_family = side_names[i]
    return side_family[0]

def get_side_name_long(side_name_short) :
    for i in range(len(side_names)) :
        side_family = side_names[i]
        if side_name_short == side_family[0] :
            return side_family[1]


##########################################################################
# initialize cube
def init_cube () :

    def init_square (color, side, row, column) :
        # cube of 6 sides/colors
        square = [color, side, row, column]
        return square

    # init_cube
    cube = []
    colors = ['green', 'blue', 'white', 'yellow', 'orange', 'red']

    for i in range(len(side_names)) :
        side = get_side_name_short(i)
        color = colors[i]
        for row in [0, 1, 2] :
            for column in [0, 1, 2] :
                cube.append(init_square(color, side, row, column))

    return cube


##########################################################################
# draw cube functions
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

            # coordinate label
            center = Point(x_start + size / 2, y_start + size / 2)
            coordinate = str(row) + ',' + str(column)
            label = Text(center, coordinate)
            label.draw(win)


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

    # display cube in 2 columns
    win.delete('all')

    for i in range(len(side_names)):
        side = get_side_name_short(i)

        if i in [1, 3, 5] :
            x_start_cube += 3 * square_size + space_btw_squares
        elif i in [2, 4] :
            x_start_cube = x_start_drawing
            y_start_cube += 3 * square_size + space_btw_squares

        draw_side(win, cube, side, x_start_cube, y_start_cube, square_size)

##########################################################################
# rotation functions
def move(cube, rotations) :

    # a slice is a single (1/4 turn) rotation of a row or column on the cube

    # there are 18 rotations implemented...
    #   6 basic - f(front), r(right), u(Up), l(Left), b(back), d(down)
    #   3 middle cube turns - m(middle layer), e(equatorial layer), s(standing layer)
    #   plus each of the 9 default moves has an inverted/reverse move
    #       indicated by an 'i', eg. fi, ri, ui, li, bi, di, mi, ei, si

    # 1-dimensional slicing plans
    #   squares in slice on face indicated by 1st letter of the plan
    #   go to the face indicated by the 2nd letter of the plan
    #   eg. 'fd' indicates squares on the 'down' side of the cube
    #   are replaced by squares on the 'front' side of the cube
    plan_slice_left = ['fd', 'db', 'bu', 'uf']
    plan_slice_right = ['fu', 'ub', 'bd', 'df']
    plan_slice_up = ['fl', 'lb', 'br', 'rf']
    plan_slice_down = ['fr', 'rb', 'bl', 'lf']

    # 3-dimensional slicing plans
    #   each plan maps the replacement of individual squares in a slice
    #   from one side to another
    #   eg. ['u', 2, 0, 'r', 0, 0] - square on face up at position row 2, column 0
    #   replaces the square on face right at position row 0, column 0
    plan_slice_front = [
        ['u', 2, 0, 'r', 0, 0], ['u', 2, 1, 'r', 1, 0], ['u', 2, 2, 'r', 2, 0],
        ['r', 0, 0, 'd', 0, 2], ['r', 1, 0, 'd', 0, 1], ['r', 2, 0, 'd', 0, 0],
        ['d', 0, 2, 'l', 2, 2], ['d', 0, 1, 'l', 1, 2], ['d', 0, 0, 'l', 0, 2],
        ['l', 0, 2, 'u', 2, 2], ['l', 1, 2, 'u', 2, 1], ['l', 2, 2, 'u', 2, 0]]

    plan_slice_standing = [
        ['u', 1, 0, 'r', 0, 1], ['u', 1, 1, 'r', 1, 1], ['u', 1, 2, 'r', 2, 1],
        ['r', 0, 1, 'd', 1, 2], ['r', 1, 1, 'd', 1, 1], ['r', 2, 1, 'd', 1, 0],
        ['d', 1, 2, 'l', 2, 1], ['d', 1, 1, 'l', 1, 1], ['d', 1, 0, 'l', 0, 1],
        ['l', 2, 1, 'u', 1, 0], ['l', 1, 1, 'u', 1, 1], ['l', 0, 1, 'u', 1, 2]]

    plan_slice_back = [
        ['u', 0, 0, 'l', 2, 0], ['u', 0, 1, 'l', 1, 0], ['u', 0, 2, 'l', 0, 0],
        ['l', 0, 0, 'd', 2, 0], ['l', 1, 0, 'd', 2, 1], ['l', 2, 0, 'd', 2, 2],
        ['d', 2, 0, 'r', 2, 2], ['d', 2, 1, 'r', 1, 2], ['d', 2, 2, 'r', 0, 2],
        ['r', 2, 2, 'u', 0, 2], ['r', 1, 2, 'u', 0, 1], ['r', 0, 2, 'u', 0, 0]]

    def slice_1d(cube, plan, inverted, idx, val) :
        if inverted :
            # inverted order
            for square in cube:
                for change in plan:
                    if square[1] == change[1] and square[idx] == val:
                        square[1] = change[0]
                        break
        else :
            # default order
            for square in cube :
                for change in plan :
                    if square[1] == change[0] and square[idx] == val :
                        square[1] = change[1]
                        break

    def slice_3d(cube, plan, inverted):
        if inverted:
            # inverted order
            for square in cube:
                for change in plan:
                    if square[1] == change[3] and square[2] == change[4] and square[3] == change[5]:
                        square[1] = change[0]
                        square[2] = change[1]
                        square[3] = change[2]
                        break
        else :
            # default order
            for square in cube:
                for change in plan:
                    if square[1] == change[0] and square[2] == change[1] and square[3] == change[2]:
                        square[1] = change[3]
                        square[2] = change[4]
                        square[3] = change[5]
                        break

    # execute moves
    move_list = rotations.split()
    for rotation in move_list :
        if rotation == 'l' :
            slice_1d(cube, plan_slice_left, False, 3, 0)
        elif rotation == 'li':
            slice_1d(cube, plan_slice_left, True, 3, 0)
        elif rotation == 'm':
            slice_1d(cube, plan_slice_left, False, 3, 1)
        elif rotation == 'mi':
            slice_1d(cube, plan_slice_left, True, 3, 1)
        elif rotation == 'r' :
            slice_1d(cube, plan_slice_right, False, 3, 2)
        elif rotation == 'ri':
            slice_1d(cube, plan_slice_right, True, 3, 2)
        elif rotation == 'u':
            slice_1d(cube, plan_slice_up, False, 2, 0)
        elif rotation == 'ui':
            slice_1d(cube, plan_slice_up, True, 2, 0)
        elif rotation == 'e':
            slice_1d(cube, plan_slice_down, False, 2, 1)
        elif rotation == 'ei':
            slice_1d(cube, plan_slice_down, True, 2, 1)
        elif rotation == 'd':
            slice_1d(cube, plan_slice_down, False, 2, 2)
        elif rotation == 'di':
            slice_1d(cube, plan_slice_down, True, 2, 2)
        elif rotation == 'f':
            slice_3d(cube, plan_slice_front, False)
        elif rotation == 'fi':
            slice_3d(cube, plan_slice_front, True)
        elif rotation == 's':
            slice_3d(cube, plan_slice_standing, False)
        elif rotation == 'si':
            slice_3d(cube, plan_slice_standing, True)
        elif rotation == 'b':
            slice_3d(cube, plan_slice_back, False)
        elif rotation == 'bi':
            slice_3d(cube, plan_slice_back, True)
        else :
            print('No case defined for rotation: ', rotation)
            print()

def scramble_cube(cube, count) :
    moves = ('l', 'li', 'm', 'mi', 'r', 'ri', 'u', 'ui', 'e', 'ei', 'd', 'di', 'f', 'fi', 's', 'si', 'b', 'bi')

    moves_list = ''

    for i in range(count) :
        idx = random.randint(0, len(moves) - 1)
        if moves_list != None : moves_list += ' '
        moves_list += moves[idx]

    move(cube, moves_list)
    print('Scrambled {} random moves...'.format(count))


##########################################################################
# RUN PROGRAM

# init
win = GraphWin("Rubik's Cube Solver", 420, 650)

cube = init_cube()
draw_cube(win, cube)

# scramble cube
scramble_cube(cube, 1000)

# draw initialized cube
draw_cube(win, cube)


# execute moves
print('Moves: l, li, m, mi, r, ri, u, ui, e, ei, d, di, f, fi, s, si, b, bi')

while True :
    inp = input('Enter move(s) separated by spaces or "q" to quit: ')

    if inp == 'q' :
        win.close()
        exit()

    move(cube, inp)
    draw_cube(win, cube)
