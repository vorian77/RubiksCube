# RubikCube.py

# Simple Rubik's Cube solver developed by Phyllip Hall to learn
# and test understanding of Python

# Version 4   11/2/19
#     * refactor rendering to move rather than draw cubes after each move
#     * added dictionary to map cube positions and know where each squre should go
#     * to increase rendering speed further, added flag to only move squares that were affected by rotation

# Version 3   11/1/19
#     * added comments to better organize code
#     * added all (18) 1/4 turn movements and ability to accept and execute a list of moves
#     * added cube scrambler

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

square_size = 50
outer_border = 1  # btw outer box
inner_border = 2  # btw inner and outer boxes

cube = []
cube_map = {}

sides = {
    'f' : ['Front', 'green'],
    'r' : ['Right', 'red'],
    'b' : ['Back', 'blue'],
    'l' : ['Left', 'orange'],
    'u' : ['Up', 'white'],
    'd' : ['Down', 'yellow']}


##########################################################################
# initialize cube
def init_cube (square_size) :

    def init_square (color, side, column, row, x_start, y_start, size) :
        # cube of 6 sides/colors
        moved = False

        # outer black square
        px1 = x_start + outer_border
        py1 = y_start + outer_border

        px2 = x_start + size - outer_border
        py2 = y_start + size - outer_border

        sqr_outer = Rectangle(Point(px1, py1), Point(px2, py2))
        sqr_outer.setFill('black')
        sqr_outer.draw(win)

        # inner colored square
        px1 = px1 + inner_border
        py1 = py1 + inner_border

        px2 = px2 - inner_border
        py2 = py2 - inner_border
        sqr_inner = Rectangle(Point(px1, py1), Point(px2, py2))
        sqr_inner.setFill(color)
        sqr_inner.draw(win)

        # coordinate label
        # center = Point(x_start + (size / 2), y_start + (size / 2))
        # coordinate = str(column) + ',' + str(row)
        # label = Text(center, coordinate)
        # label.draw(win)

        square = [color, side, column, row, sqr_outer, sqr_inner, label, moved]

        return square

    # init_cube
    cube_row = 0
    label_h = 18

    margin_left = square_size
    margin_top = square_size
    space_btw_squares = square_size

    x = margin_left
    y = margin_top

    i = -1
    for side_key, side in sides.items() :
        i += 1
        side_name = side[0]
        side_color = side[1]

        # display cube in 2 columns
        # determin cube column
        if i % 2 == 0 :
            cube_col = 0
        else :
            cube_col = 1

        # determine cube row
        if i > 1 and i % 2 == 0 :
            cube_row += 1

        x = margin_left + (cube_col * (3 * square_size + space_btw_squares))
        y = margin_top + (cube_row * (label_h + 3 * square_size + space_btw_squares))

        # add label of side
        label = Text(Point((x + (3 * square_size / 2)), y), side_name)
        label.setSize(20)
        label.setStyle('normal')
        label.draw(win)
        y += label_h

        for column in [0, 1, 2]:
            x_sqr = x + (column * square_size)

            for row in [0, 1, 2] :
                y_sqr = y + (row * square_size)

                map_key = side_key + str(column) + str(row)
                map_point = [x_sqr, y_sqr]
                cube_map[map_key] = map_point

                cube.append(init_square(side_color, side_key, column, row, x_sqr, y_sqr, square_size))

    return cube


##########################################################################
def draw_cube(win, cube) :

    def move_square(win, square, x_target, y_target, border) :
        p = square.getP1()
        x_current, y_current = p.getX(), p.getY()

        x_move = x_target - x_current + border
        y_move = y_target - y_current + border

        square.move(x_move, y_move)

    def move_label(win, label, x_target, y_target) :
        x_current, y_current = label.getX(), label.getY()

        x_move = x_target - x_current
        y_move = y_target - y_current

        label.move(x_move, y_move)

    for square in cube :
        if not square[7] : continue

        side = square[1]
        column = square[2]
        row = square[3]
        sqr_outer = square[4]
        sqr_inner = square[5]
        label = square[6]
        square[7] = False

        map_key = side + str(column) + str(row)
        map_point = cube_map[map_key]

        move_square(win, sqr_outer, map_point[0], map_point[1], outer_border)
        move_square(win, sqr_inner, map_point[0], map_point[1], outer_border + inner_border)
        #move_label(win, label, map_point[0], map_point[1])


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
        ['u', 0, 2, 'r', 0, 0], ['u', 1, 2, 'r', 0, 1], ['u', 2, 2, 'r', 0, 2],
        ['r', 0, 0, 'd', 2, 0], ['r', 0, 1, 'd', 1, 0], ['r', 0, 2, 'd', 0, 0],
        ['d', 2, 0, 'l', 2, 2], ['d', 1, 0, 'l', 2, 1], ['d', 0, 0, 'l', 2, 0],
        ['l', 2, 0, 'u', 2, 2], ['l', 2, 1, 'u', 1, 2], ['l', 2, 2, 'u', 0, 2]]

    plan_slice_standing = [
        ['u', 0, 1, 'r', 1, 0], ['u', 1, 1, 'r', 1, 1], ['u', 2, 1, 'r', 1, 2],
        ['r', 1, 0, 'd', 2, 1], ['r', 1, 1, 'd', 1, 1], ['r', 1, 2, 'd', 0, 1],
        ['d', 2, 1, 'l', 1, 2], ['d', 1, 1, 'l', 1, 1], ['d', 0, 1, 'l', 1, 0],
        ['l', 1, 2, 'u', 0, 1], ['l', 1, 1, 'u', 1, 1], ['l', 1, 0, 'u', 2, 1]]

    plan_slice_back = [
        ['u', 0, 0, 'l', 0, 2], ['u', 1, 0, 'l', 0, 1], ['u', 2, 0, 'l', 0, 0],
        ['l', 0, 0, 'd', 0, 2], ['l', 0, 1, 'd', 1, 2], ['l', 0, 2, 'd', 2, 2],
        ['d', 0, 2, 'r', 2, 2], ['d', 1, 2, 'r', 2, 1], ['d', 2, 2, 'r', 2, 0],
        ['r', 2, 2, 'u', 2, 0], ['r', 2, 1, 'u', 1, 0], ['r', 2, 0, 'u', 0, 0]]

    def slice_1d(cube, plan, inverted, idx, val) :
        if inverted :
            # inverted order
            for square in cube:
                for change in plan:
                    if square[1] == change[1] and square[idx] == val:
                        square[1] = change[0]
                        square[7] = True
                        break
        else :
            # default order
            for square in cube :
                for change in plan :
                    if square[1] == change[0] and square[idx] == val :
                        square[1] = change[1]
                        square[7] = True
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
                        square[7] = True
                        break
        else :
            # default order
            for square in cube:
                for change in plan:
                    if square[1] == change[0] and square[2] == change[1] and square[3] == change[2]:
                        square[1] = change[3]
                        square[2] = change[4]
                        square[3] = change[5]
                        square[7] = True
                        break

    # execute moves
    move_list = rotations.split()
    for rotation in move_list :
        if rotation == 'l' :
            slice_1d(cube, plan_slice_left, False, 2, 0)
        elif rotation == 'li':
            slice_1d(cube, plan_slice_left, True, 2, 0)
        elif rotation == 'm':
            slice_1d(cube, plan_slice_left, False, 2, 1)
        elif rotation == 'mi':
            slice_1d(cube, plan_slice_left, True, 2, 1)
        elif rotation == 'r' :
            slice_1d(cube, plan_slice_right, False, 2, 2)
        elif rotation == 'ri':
            slice_1d(cube, plan_slice_right, True, 2, 2)
        elif rotation == 'u':
            slice_1d(cube, plan_slice_up, False, 3, 0)
        elif rotation == 'ui':
            slice_1d(cube, plan_slice_up, True, 3, 0)
        elif rotation == 'e':
            slice_1d(cube, plan_slice_down, False, 3, 1)
        elif rotation == 'ei':
            slice_1d(cube, plan_slice_down, True, 3, 1)
        elif rotation == 'd':
            slice_1d(cube, plan_slice_down, False, 3, 2)
        elif rotation == 'di':
            slice_1d(cube, plan_slice_down, True, 3, 2)
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



##########################################################################
# RUN PROGRAM

# init
win = GraphWin("Rubik's Cube Solver", 450, 675)

cube = init_cube(square_size)

#win.getMouse()  # Pause to view result
#print(cube_map)

# scramble cube
#scramble_cube(cube, 1000)
#draw_cube(win, cube)

# execute moves
print('Moves: l, li, m, mi, r, ri, u, ui, e, ei, d, di, f, fi, s, si, b, bi')

while True :
    inp = input('Enter move(s) separated by spaces or "q" to quit: ')

    if inp == 'q' :
        win.close()
        exit()
    elif inp == 'sc' :
        scramble_cube(cube, 1000)
        draw_cube(win, cube)
    else :
        move(cube, inp)
        draw_cube(win, cube)
