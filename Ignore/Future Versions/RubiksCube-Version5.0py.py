# RubikCube.py by Phyllip Hall

""""
This program is a simulator and solver for a 6-sided/colored 3x3 Rubik's cube.
It uses cube move conventions defined on ruwix.com (the Twisty Puzzle Wiki), and
the solving algorithm defined on speedcube.com.au. I’ve made some contributions to
the solving algorithm where the "speedcube" algorithm requires human interpretation.

This is my first Python program. I’m learning Python syntax primarily through py4e.com (Python
For Everyone), w3schools.com, and realpython.com. I'm also reading Steve McConnell's "Code Complete:
2nd Addition" (Microsoft Press) as a software architecture style guide.

I saw the Rubik's cube solved by a robot hand created by Open AI (https://youtu.be/x4O8pojMF0w)
and thought creating a software-only simulation would be a fun way to practice Python and to
share my learning progress with friends. (Of course, this program uses the predetermined solving
algorithm stated above rather than the machine learning approach used in the video).

After completing my self-guided learning plan, I hope to find work as a Python developer.
Previously, I programmed almost exclusively in PowerBuilder PowerScript (also an incredibly
efficient and expressive language) and SQL. I developed and marketed a windows based case
management and reporting system that has come to the end of it's usage after more than 20 years.

In the spirit of open-source software sharing, I hope that my skills development process,
including a significant coding challenge, will inspire and serve as a guide to other experienced
developers who are making the transition from legacy languages to Python and other modern tools.

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).

PLATFORMS: The cube is rendered in 2D using the graphics.py library developed by
John Zelle as a companion to his book "Python Programming: An Introduction to Computer
Science" (Franklin, Beedle & Associates).

OVERVIEW: There are 4 primary classes in this program: cube(), render(), play(), and solve()
- cube() provides a 3D coordinate map of the cube and methods that simulate moves upon it:
    * rotate() - generates a list of changes to the cube's colors based on the execution of rotate commands
    * get_render_que() - provides the list of cube face changes generated by rotate() needed to display the cube
    * scramble() - sends a randomized set of rotation commands to the rotate method
    * find() - returns a list of coordinates that locate requested cubes
    * reset() - returns the cube to it's original (solved) state
- render() displays the 6 faces of the cube in an application window
- play() executes command line rotate requests
- solve() executes a multiphase algorithm that solves the cube
"""


# Version 5   11/6/19
#     * significant refactor to classes that isolate the cube object, and allow independent and potentially
#       interchangeable processes for input, output, and solving algorithm
#     * simplified logic for cube rotation, and completed the rotation command library
#     * significantly increased the speed of cube rendering by changing the fill-color of squares rather
#       than moving them to simulate cube rotations
#     * loaded the program to GitHub to learn GitHub, for comment, and to share with other newbie deverlopers

# Version 4   11/2/19
#     * sped up visual processing by only moving effected squares rather than wiping and redrawing all squares
#       after each rotation command
#     * added a dictionary map to track cube positions

# Version 3   11/1/19
#     * added comments to better organize code
#     * added basic (18) 1/4 turn movements and ability to accept and execute a list of moves
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
class cube:

    def __init__(self):
        self.sides_cnt = 3
        self.sides = {
            'f': ['Front', 'green'],
            'r': ['Right', 'red'],
            'b': ['Back', 'blue'],
            'l': ['Left', 'orange'],
            'u': ['Up', 'white'],
            'd': ['Down', 'yellow']}
        self.squares = {}
        self.squares_to_render = {}
        self.squares_reset = {}
        self.squares_buffer = {}

        for side_key, side in self.sides.items():
            side_name = side[0]
            color = side[1]

            for column in range(self.sides_cnt):
                for row in range(self.sides_cnt):
                    key = side_key + str(column) + str(row)
                    self.squares[key] = color

        self.squares_to_render = self.squares.copy()
        self.squares_reset = self.squares.copy()


    def rotate(self, rotation_list):
        # a rotation is a single rotation (1/4 turn) of a row or column on the cube

        # there are 18 rotations implemented...
        #   6 basic - f(front), r(right), u(Up), l(Left), b(back), d(down)
        #   3 middle cube turns - m(middle layer), e(equatorial layer), s(standing layer)
        #   plus each of the 9 default moves has an inverted/reverse move
        #       indicated by an 'i', eg. fi, ri, ui, li, bi, di, mi, ei, si

        # the 18 rations are implemented by plans that indicate either
        # a movement of the colors in a column or row on one face to another face, or
        # a movement of a single colors from one face to another

        # a storage buffer to allow all color changes in a rotation to be specified before
        # they are accepted into the cube map or the que of squares to be changed at render

        ###### x & y axis slice functions
        #   eg. 'fd' indicates replace the colors on 'd' (down) side of cube
        #   with the colors on the 'f' (front) side of the cube
        plan_col = ['uf', 'bu', 'db', 'fd']
        plan_row = ['rf', 'br', 'lb', 'fl']

        def slice_x_inverted(squares, plan, col):
            plan_inverted = invert_plan(plan)
            slice_x(squares, plan_inverted, col)

        def slice_y_inverted(squares, plan, col):
            plan_inverted = invert_plan(plan)
            slice_y(squares, plan_inverted, col)

        def slice_x(squares, plan, col):
            for change in plan:
                for row in range(self.sides_cnt):
                    key_source = change[0] + str(col) + str(row)
                    key_target = change[1] + str(col) + str(row)
                    add_change(squares, key_source, key_target)
            accept_buffer(squares)

        def slice_y(squares, plan, row):
            for change in plan:
                for col in range(self.sides_cnt):
                    key_source = change[0] + str(col) + str(row)
                    key_target = change[1] + str(col) + str(row)
                    add_change(squares, key_source, key_target)
            accept_buffer(squares)

        ###### face functions
        #   eg. ['u20', 'r00'] indicates the color on face 'r' (right) should be
        #   replaced by the color on face 'u' (up)
        plan_front = [
            ['u02', 'r00'], ['u12', 'r01'], ['u22', 'r02'],
            ['r00', 'd20'], ['r01', 'd10'], ['r02', 'd00'],
            ['d20', 'l22'], ['d10', 'l21'], ['d00', 'l20'],
            ['l20', 'u22'], ['l21', 'u12'], ['l22', 'u02']]

        plan_standing = [
            ['u01', 'r10'], ['u11', 'r11'], ['u21', 'r12'],
            ['r10', 'd21'], ['r11', 'd11'], ['r12', 'd01'],
            ['d21', 'l12'], ['d11', 'l11'], ['d01', 'l10'],
            ['l12', 'u01'], ['l11', 'u11'], ['l10', 'u21']]

        plan_back = [
            ['u00', 'l02'], ['u10', 'l01'], ['u20', 'l00'],
            ['l00', 'd02'], ['l01', 'd12'], ['l02', 'd22'],
            ['d02', 'r22'], ['d12', 'r21'], ['d22', 'r20'],
            ['r22', 'u20'], ['r21', 'u10'], ['r20', 'u00']]

        def slice_z_inverted(squares, plan):
            plan_inverted = invert_plan(plan)
            slice_z(squares, plan_inverted)

        def slice_z(squares, plan):
            for change in plan:
                key_source = change[0]
                key_target = change[1]
                add_change(squares, key_source, key_target)
            accept_buffer(squares)

        ###### face rotation functions
        # clockwise
        plan_face = [
            ['00', '20'], ['10', '21'], ['20', '22'],
            ['01', '10'], ['21', '12'],
            ['02', '00'], ['12', '01'], ['22', '02']]

        def rotate_face_inverted(squares, plan, face):
            # counter-clockwise
            plan_inverted = invert_plan(plan)
            rotate_face(squares, plan_inverted, face)

        def rotate_face(squares, plan, face):
            for change in plan:
                key_source = face + change[0]
                key_target = face + change[1]
                add_change(squares, key_source, key_target)
            accept_buffer(squares)

        ###### cube rotation functions
        # X rotate on R
        # y - rotate on U
        # z - rotate on F


        plan_rotate_left = ['fl', 'rf', 'br', 'lb'] # left
        plan_rotate_up = ['fu', 'ub', 'bd', 'df'] # up

        def turn_inverted(squares, plan):
            # right
            plan_inverted = invert_plan(plan)
            turn(squares, plan_inverted)

        def turn(squares, plan):
            for change in plan:
                face_source = change[0]
                face_target = change[1]
                for column in range(self.sides_cnt):
                    for row in range(self.sides_cnt):
                        key_source = face_source + str(column) + str(row)
                        key_target = face_target + str(column) + str(row)
                        add_change(squares, key_source, key_target)
            accept_buffer(squares)

        def invert_plan(plan):
            plan_inverted = []
            for item in plan:
                plan_inverted.append(item[::-1])
            return plan_inverted

        def add_change(squares, key_source, key_target):
            color = squares.get(key_source)
            self.squares_buffer[key_target] = color
            self.squares_to_render[key_target] = color

        def accept_buffer(squares):
            for key, color in self.squares_buffer.items():
                squares[key] = color
            self.squares_buffer.clear()

        # rotate()
        self.squares_to_render.clear()

        rotations = rotation_list.split()
        for rotation in rotations:
            if rotation == 'l':
                slice_x(self.squares, plan_col, 0)
                rotate_face(self.squares, plan_face, 'l')
            elif rotation == 'li':
                slice_x_inverted(self.squares, plan_col, 0)
                rotate_face_inverted(self.squares, plan_face, 'l')
            elif rotation == 'm':
                slice_x(self.squares, plan_col, 1)
            elif rotation == 'mi':
                slice_x_inverted(self.squares, plan_col, 1)
            elif rotation == 'r':
                slice_x_inverted(self.squares, plan_col, 2)
                rotate_face(self.squares, plan_face, 'r')
            elif rotation == 'ri':
                slice_x(self.squares, plan_col, 2)
                rotate_face_inverted(self.squares, plan_face, 'r')

            elif rotation == 'u':
                slice_y(self.squares, plan_row, 0)
                rotate_face(self.squares, plan_face, 'u')
            elif rotation == 'ui':
                slice_y_inverted(self.squares, plan_row, 0)
                rotate_face_inverted(self.squares, plan_face, 'u')
            elif rotation == 'e':
                slice_y_inverted(self.squares, plan_row, 1)
            elif rotation == 'ei':
                slice_y(self.squares, plan_row, 1)
            elif rotation == 'd':
                slice_y_inverted(self.squares, plan_row, 2)
                rotate_face(self.squares, plan_face, 'd')
            elif rotation == 'di':
                slice_y(self.squares, plan_row, 2)
                rotate_face_inverted(self.squares, plan_face, 'd')
            elif rotation == 'f':
                slice_z(self.squares, plan_front)
                rotate_face(self.squares, plan_face, 'f')
            elif rotation == 'fi':
                slice_z_inverted(self.squares, plan_front)
                rotate_face_inverted(self.squares, plan_face, 'f')
            elif rotation == 's':
                slice_z(self.squares, plan_standing)
            elif rotation == 'si':
                slice_z_inverted(self.squares, plan_standing)
            elif rotation == 'b':
                slice_z(self.squares, plan_back)
                rotate_face(self.squares, plan_face, 'b')
            elif rotation == 'bi':
                slice_z_inverted(self.squares, plan_back)
                rotate_face_inverted(self.squares, plan_face, 'b')

            elif rotation == 'tl':
                turn(self.squares, plan_rotate_left)
                rotate_face(self.squares, plan_face, 'u')
                rotate_face(self.squares, plan_face, 'd')
            elif rotation == 'tr':
                turn_inverted(self.squares, plan_rotate_left)
                rotate_face_inverted(self.squares, plan_face, 'u')
                rotate_face_inverted(self.squares, plan_face, 'd')

            elif rotation == 'tu':
                turn(self.squares, plan_rotate_up)
                rotate_face(self.squares, plan_face, 'l')
                rotate_face(self.squares, plan_face, 'r')
            elif rotation == 'td':
                turn_inverted(self.squares, plan_rotate_up)
                rotate_face_inverted(self.squares, plan_face, 'l')
                rotate_face_inverted(self.squares, plan_face, 'r')

            else:
                print('No case defined for rotation: ', rotation)
                print()

    def scramble(self, rotation_count):
        rotation_list = ''
        rotations = ('l', 'li', 'm', 'mi', 'r', 'ri', 'u', 'ui', 'e', 'ei', 'd', 'di', 'f', 'fi', 's', 'si', 'b', 'bi')

        for i in range(rotation_count):
            idx = random.randint(0, len(rotations) - 1)
            if rotation_list != '': rotation_list += ' '
            rotation_list += rotations[idx]

        self.rotate(rotation_list)

    def reset(self):
        self.squares = self.squares_reset.copy()
        self.squares_to_render = self.squares_reset.copy()

    def get_render_que(self):
        return self.squares_to_render


class render :
    def __init__(self, cube):
        # cube of 6 sides/colors
        self.cube_map = {}
        self.win = GraphWin("Rubik's Cube Solver", 450, 675)
        self.init(cube)

    def init(self, cube):
        square_size = 50
        display_map = {}

        def init_map(display_map) :
            # create map of layout of cube sides
            cube_row = 0
            margin_left = square_size
            margin_top = square_size
            space_btw_sides = square_size

            label_h = 18
            col_cnt = 2

            side_w = 3 * square_size + space_btw_sides
            side_h = label_h + 3 * square_size + space_btw_sides

            i = -1
            for side_key, side in cube.sides.items() :
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

                x1 = margin_left + (cube_col * side_w)
                y1 = margin_left + (cube_row * side_h)

                # add label of side
                label = Text(Point((x1 + (3 * square_size / 2)), y1), side_name)
                label.setSize(20)
                label.setStyle('normal')
                label.draw(self.win)
                y1 += label_h

                display_map[side_key] = [x1, y1]

        def init_squares(cube, display_map, cube_map, square_size):
            for key, color in cube.squares.items():
                outer_border = 1  # btw outer box
                inner_border = 2  # btw inner and outer boxes

                side = key[0]
                column = int(key[1])
                row = int(key[2])

                position = display_map[side]
                x1 = position[0]
                y1 = position[1]

                x_start = x1 + (column * square_size)
                y_start = y1 + (row * square_size)

                # outer black square
                px1 = x_start + outer_border
                py1 = y_start + outer_border

                px2 = x_start + square_size - outer_border
                py2 = y_start + square_size - outer_border

                sqr_outer = Rectangle(Point(px1, py1), Point(px2, py2))
                sqr_outer.setFill('black')
                sqr_outer.draw(self.win)

                # inner colored square
                px1 = px1 + inner_border
                py1 = py1 + inner_border

                px2 = px2 - inner_border
                py2 = py2 - inner_border
                sqr_inner = Rectangle(Point(px1, py1), Point(px2, py2))
                sqr_inner.setFill(color)
                sqr_inner.draw(self.win)

                # coordinate label
                # center = Point(x_start + (size / 2), y_start + (size / 2))
                # coordinate = str(column) + ',' + str(row)
                # label = Text(center, coordinate)
                # label.draw(win)

                element = [px1, py1, sqr_outer, sqr_inner]
                cube_map[key] = element

        # init()
        init_map(display_map)
        init_squares(cube, display_map, self.cube_map, square_size)


    def draw(self, cube):
        squares = cube.get_render_que()
        for key, color in squares.items():
            element = self.cube_map[key]

            sqr_inner = element[3]
            sqr_inner.setFill(color)

    def __del__(self):
        self.win.close()


##########################################################################
# RUN PROGRAM

# init
cube = cube()
render = render(cube)

# execute moves
print('Rotations: l, li, m, mi, r, ri, u, ui, e, ei, d, di, f, fi, s, si, b, bi, sc (scramble), re (reset)')

while True :
    inp = input('Enter rotation(s) separated by spaces or "q" to quit: ')

    if inp == 'q' :
        exit()
    elif inp == 'sc' :
        cube.scramble(10000)
        render.draw(cube)
    elif inp == 're':
        cube.reset()
        render.draw(cube)
    else :
        cube.rotate(inp)
        render.draw(cube)