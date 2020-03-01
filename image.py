#SPECIAL THANKS TO IAN WILLIAMS FOR HELPING ME WITH SOME DEBUGGING, PRAISE PROGRAMMER JESUS, PEACE BE UPON HIM
#<3 IW
import math

#multiply m1 by m2, modifying m2 to be the product
#m1 * m2 -> m2
def matrix_mult( m1, m2 ):

    point = 0
    for row in m2:
        #get a copy of the next point
        tmp = row[:]

        for r in range(4):
            m2[point][r] = (m1[0][r] * tmp[0] +
                            m1[1][r] * tmp[1] +
                            m1[2][r] * tmp[2] +
                            m1[3][r] * tmp[3])
        point+= 1

def ident( matrix ):
    for r in range( len( matrix[0] ) ):
        for c in range( len(matrix) ):
            if r == c:
                matrix[c][r] = 1
            else:
                matrix[c][r] = 0

def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m

class picture:
    def __init__(self, n, w, h):
        self.name = n
        self.width, self.height = (w, h)
        self.pixels = [[[0, 0, 0] for i in range(self.width)] for j in range(self.height)]
        self.four_identity = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.edge_matrix = [[], [], [], []]
        self.transformation_matrix = ident(new_matrix())

    def plot(self, x, y, color):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:#out of bounds
            return
        self.pixels[self.height - y - 1][x] = color #Flip for humans

    def draw_line(self, x0, y0, x1, y1, color ):
        #swap points if going right -> left
        if x0 > x1:
            xt = x0
            yt = y0
            x0 = x1
            y0 = y1
            x1 = xt
            y1 = yt

        x = x0
        y = y0
        A = 2 * (y1 - y0)
        B = -2 * (x1 - x0)

        #octants 1 and 8
        if ( abs(x1-x0) >= abs(y1 - y0) ):

            #octant 1
            if A > 0:
                d = A + B/2

                while x < x1:
                    self.plot(x, y, color)

                    if d > 0:
                        y+= 1
                        d+= B
                    x+= 1
                    d+= A
                #end octant 1 while
                self.plot(x1, y1, color)
            #end octant 1

            #octant 8
            else:
                d = A - B/2

                while x < x1:
                    self.plot(x, y, color)
                    if d < 0:
                        y-= 1
                        d-= B
                    x+= 1
                    d+= A
                #end octant 8 while
                self.plot(x1, y1, color)
            #end octant 8
        #end octants 1 and 8

        #octants 2 and 7
        else:
            #octant 2
            if A > 0:
                d = A/2 + B

                while y < y1:
                    self.plot(x, y, color)
                    if d < 0:
                        x+= 1
                        d+= A
                    y+= 1
                    d+= B
                #end octant 2 while
                self.plot(x1, y1, color)
            #end octant 2

            #octant 7
            else:
                d = A/2 - B;

                while y > y1:
                    self.plot(x, y, color)
                    if d > 0:
                        x+= 1
                        d+= A
                    y-= 1
                    d-= B
                #end octant 7 while
                self.plot(x1, y1, color)

    def display_edge_matrix(self):
        for i in self.edge_matrix:
            print(i)

    def add_3d_point(self, x, y, z):
        self.edge_matrix[0].append(x)
        self.edge_matrix[1].append(y)
        self.edge_matrix[2].append(z)
        self.edge_matrix[3].append(1)

    def add_edge(self, x0, y0, z0, x1, y1, z1):
        self.add_3d_point(x0,y0,z0)
        self.add_3d_point(x1,y1,z1)

    def draw_edges(self, color):
        iterator = 0
        self.display_edge_matrix()
        while (iterator < (len(self.edge_matrix[0]) - 1)): # I was wrong, the original error was just you needed < instead of != to account for the overshoot. IW
            self.draw_line(self.edge_matrix[0][iterator], self.edge_matrix[1][iterator], self.edge_matrix[0][iterator + 1], self.edge_matrix[1][iterator + 1], color)
            iterator = iterator + 2
#NEW METHODS NOT INCLUDING SCALING CAN BE FOUND HERE
    def make_translate(self, x, y, z):
        translation_factor = [[1, 0,  0, a], [0, 1, 0, b], [0, 0, 1, c], [0, 0, 0, 1]]
        matrix_mult(translation_factor, self.transformation_matrix)

    def make_scale(self, x, y, z):
        scaling_factor = [[a, 0,  0, 0], [0, b, 0, 0], [0, 0, c, 0], [0, 0, 0, 1]]
        matrix_mult(scaling_factor, self.transformation_matrix)

    def make_rotX(self, deg_theta):
        theta = deg_theta * (math.pi/180)
        rotation_factor = [[1, 0, 0, 0], [0, math.cos(theta), (math.sin(theta) * -1), 0], [0, math.sin(theta), math.cos(theta), 0], [0, 0, 0, 1]]
        matrix_mult(rotation_factor, self.transformation_matrix)

    def make_rotY(self, deg_theta):
        theta = deg_theta * (math.pi/180)
        rotation_factor = [[math.cos(theta), 0, math.sin(theta), 0], [0, 0, 0, 0], [(math.sin(theta) * -1), 0, math.cos(theta), 0], [0, 0, 0, 1]]
        matrix_mult(rotation_factor, self.transformation_matrix)

    def make_rotZ(self, deg_theta):
        theta = deg_theta * (math.pi/180)
        rotation_factor = [[math.cos(theta), (math.sin(theta) * -1), 0, 0], [math.sin(theta), math.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        matrix_mult(rotation_factor, self.transformation_matrix)

# def coolify_pic_ascii(g):
#     a = 1
#     b = 1
#     for x in range(g.width):
#         for y in range(g.height):
#             n = g.pixels[x][y]
#             n[0] = a % 256
#             n[1] = b % 256
#         a = a + 1
#         b = b + 2

def print_pic_ascii(g):
    s = ""
    for x in range(g.width):
        for y in range(g.height):
            n = g.pixels[x][y]
            s += str(n[0]) + " " + str(n[1]) + " " + str(n[2]) + "  "
        s += "\n"
    #print(s)
    return s

def ppm_save_ascii(g):
    n = str(g.name)
    f = open(n + ".ppm", "w")
    f.write("P3\n" + str(g.width) + " " + str(g.height) + "\n255\n")
    f.write(print_pic_ascii(g))
    f.close()
    print(n + '.ppm')

# def test(x, y, deltx, delty, y_int):
#     return (delty *  x) - (deltx *  y) + (deltx * y_int)

def add_line(g, startx, starty, endx, endy):
    g.pixels[startx][starty] = [0, 0, 0]
    g.pixels[endx][endy] = [0, 0, 0]
    if endx - startx == 0:
        drawline_straight(g, startx, starty, endy)
    else:
        slope = (endy - starty)/(endx - startx)
        if (0 <= abs(slope) and abs(slope) < 1):
            drawline_octant_1(g, startx, starty, endx, endy)
        elif (1 <= abs(slope)):
            drawline_octant_2(g, startx, starty, endx, endy)

#NEW MATRIX CODE BELOW
# example_matrix = [[25, 25, 0, 1], [50, 50, 0, 1], [25, 50, 0, 1], [50, 25, 0, 1]]

def display_matrix(x):
    for i in x:
        print(i)

def multiply_matrices(x,y):
#this function is meant to take in rectangular matrices and multiply them in order given
    #Python doesn't generate matrices like this: result = [len(y)][len(y[0])] IW
    result_matrix = [([0] * len(y[0])) for i in range(len(y))]#[len(y)][len(y[0])]
    print(result_matrix)
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                result_matrix[i][j] += x[i][k] * y[k][j]
    display_matrix(result_matrix)
    y = result_matrix #Alters the second matrix IW
    return result_matrix

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         move: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
    pass

#TEST CODE BELOW

#draw_line(self, x0, y0, x1, y1, color )
#add_edge(self, x0, y0, z0, x1, y1, z1)
#draw_edges(self, color)

n = picture('image', 500, 500)

n.draw_edges([255, 255, 255])

ppm_save_ascii(n)
