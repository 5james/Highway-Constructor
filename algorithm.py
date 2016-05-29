

class Point:
    TYPE_TOWN, TYPE_CROSSROAD = range(0, 2)

    def __init__(self, x, y, point_type):
        self.x = x
        self.y = y
        self.type = point_type

    def __str__(self):
        str = ""
        if self.type == self.TYPE_TOWN:
            str += "Town: "
        else:
            str += "Crossroad: "
        str += repr(self.x) + ", " + repr(self.y)
        return str


class State:
    def __init__(self, edges):
        self.edges = edges


class Algorithm:
    def __init__(self, point_tuples):
        pass