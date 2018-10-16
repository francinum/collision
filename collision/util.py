import math


LEFT_VORONOI_REGION = -1
MIDDLE_VORONOI_REGION = 0
RIGHT_VORONOI_REGION  = 1


class vec():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            return vec(self.x+other, self.y+other)

        return vec(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            return vec(self.x*other, self.y*other)

        return vec(self.x*other.x, self.y*other.y)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            return vec(self.x-other,self.y-other)

        return vec(self.x-other.x,self.y-other.y)

    def __neg__(self):
        return vec(-self.x, -self.y)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            return vec(self.x/other,self.y/other)

        return vec(self.x/other.x,self.y/other.y)

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            return vec(self.x//other,self.y//other)

        return vec(self.x//other.x,self.y//other.y)

    def __mod__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            return vec(self.x%other,self.y%other)

        return vec(self.x%other.x,self.y%other.y)

    def __eq__(self, other):
        if type(other) != vec:
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if type(other) != vec:
            return True
        return self.x != other.x or self.y != other.y

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __contains__(self, value):
        return value == self.x or value == self.y

    def __len__(self):
        return 2

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "vec [{x}, {y}]".format(x=self.x, y=self.y)

    def copy(self):
        return vec(self.x,self.y)

    def set(self, other):
        self.x = other.x
        self.y = other.y

    def perp(self):
        return vec(self.y, -self.x)

    def rotate(self,angle):
        return vec(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))

    def reverse(self):
        return vec(-self.x, -self.y)


    def int(self):
        return vec(int(self.x), int(self.y))

    def normalize(self):
        d = self.ln()
        return self/d

    def project(self,other):
        amt = self.dot(other) / other.ln2()

        return vec(amt * other.x,  amt * other.y)

    def project_n(self,other):
        amt = self.dot(other)

        return vec(amt * other.x, amt * other.y)


    def reflect(self,axis):
        v = vec(self.x,self.y)
        v = v.project(axis) * 2
        v = -v

        return v

    def reflect_n(self,axis):
        v = vec(self.x, self.y)
        v = v.project_n(axis) * 2
        v = -v

        return v

    def dot(self,other):
        return self.x * other.x + self.y * other.y

    def ln2(self):
        return self.dot(self)

    def ln(self):
        return math.sqrt(self.ln2())

def flatten_points_on(points, normal, result):
    min = math.inf
    max = -math.inf
    for i in range(len(points)):
        dot = points[i].dot(normal)
        if dot < min: min = dot
        if dot > max: max = dot

    result[0] = min
    result[1] = max


def is_separating_axis(a_pos,b_pos,a_points,b_points,axis,response = None):
    range_a = [0,0]
    range_b = [0,0]

    offset_v = b_pos-a_pos

    projected_offset = offset_v.dot(axis)

    flatten_points_on(a_points, axis, range_a)
    flatten_points_on(b_points, axis, range_b)

    range_b[0] += projected_offset
    range_b[1] += projected_offset

    if range_a[0] > range_b[1] or range_b[0] > range_a[1]:
        return True

    if response:

        overlap = 0

        if range_a[0] < range_b[0]:
            response.a_in_b = False

            if range_a[1] < range_b[1]:
                response.b_in_a = False

            else:
                option_1 = range_a[1] - range_b[1]
                option_2 = range_b[1] - range_a[1]
                operlap = option_1 if option_1 < option_2 else option_2

        else:
            response.b_in_a = False

            if range_a[1] > range_b[1]:
                overlap = range_a[0] - range_b[1]
                response.a_in_b = False

            else:
                option_1 = range_a[1] - range_b[0]
                option_2 = range_b[1] - range_a[0]

                overlap = option_1 if option_1 < option_2 else option_2

        abs_overlap = abs(overlap)
        if abs_overlap < response.overlap:
            response.overlap = abs_overlap
            response.overlap_n.set(axis)
            if overlap < 0:
                response.overlap_n = response.overlap_n.reverse()

    return False

def voronoi_region(line,point):
    dp = point.dot(line)

    if dp < 0:
        return LEFT_VORONOI_REGION
    elif dp > line.ln2():
        return RIGHT_VORONOI_REGION
    return MIDDLE_VORONOI_REGION