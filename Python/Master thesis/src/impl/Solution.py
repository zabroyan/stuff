from collections import defaultdict
from enum import Enum
from gurobipy import *


class Conflict(Enum):
    """
    Enum for conflict types
    """
    VERTEX = 1
    EDGE = 2
    OVERLAP = 3


class Point:
    def __init__(self, x, y):
        """
        Structure for point of vertex
        :param x: x coordinate
        :param y:  y coordinate
        """
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if type(other) is Point:
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        """
        Euclidean distance
        :param other: other point
        :return: Euclidean distance between this and other point
        """
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def intersect(self, other, dist):
        """
        Finds point of intersection between two points
        :param other: other point
        :param dist: distance of the intersection
        :return: point of the intersection between two point at given distance
        """
        d = self.distance(other)
        if d == 0:
            return self
        d_left = d - dist
        return (self * d_left + other * dist) / d

    def inCircle(self, center, radius):
        return (self.x - center.x) ** 2 + (self.y - center.y) ** 2 <= radius ** 2

    def angle(self, other):
        """
        Calculates an angle between two points
        :param other: other point
        :return: an angle between two points
        """
        angle = math.atan2(other.y - self.y, other.x - self.x) * 180 / math.pi
        return angle if angle > 0 else 360 + angle


class Map:
    def __init__(self):
        """
        Map structure
        """
        self.links = tuplelist()
        self.nodes = {}
        self.points = {}

    def add_link(self, node, nb):
        """
        Adds an edge between two nodes
        :param node: first node
        :param nb: second node
        :return: self
        """
        if (node, nb) not in self.links:
            self.links.extend([(node, nb), (nb, node)])
        return self

    def add_node(self, node, x, y):
        """
        Adds a node to nodes list
        :param node: node to add
        :param x: x coordinate
        :param y: y coordinate
        :return: self
        """
        if node not in self.nodes:
            self.nodes[node] = Point(x, y)
            self.points[(x, y)] = node
        return self

    def print(self):
        """
        Print map
        """
        for n in self.nodes:
            print(f"{n} at {self.nodes[n]}: {self.links.select(n, '*')}")


class Constraint:
    def __init__(self, ai, aj, v, t, type, overlap_t=0, v_next = -1, v_prev=-1):
        """
        Structure for a constraint
        :param ai: agent i
        :param aj: agent j
        :param v: vertex of conflict
        :param t: time of conflict
        :param type: conflict type
        :param overlap_t: time to wait for overlap conflict, default is 0
        :param v_next: vertex after the conflict, default is -1
        :param v_prev: vertex before the conflict, default is -1
        """
        self.ai = ai
        self.aj = aj
        self.vertex = v
        self.vertex_next = v_next
        self.vertex_prev = v_prev
        self.time = t
        self.type = type
        self.overlap_time = overlap_t

    def __eq__(self, other):
        return self.ai == other.ai and self.aj == other.aj and self.vertex == other.vertex and self.time == other.time

    def print(self):
        if self.type == Conflict.VERTEX:
            print(f'ai {self.ai}, aj {self.aj}: v: {self.vertex}, v_prev: {self.vertex_prev}, t: {self.time} (VERTEX)')
        elif self.type == Conflict.EDGE:
            print(f'ai {self.ai}, aj {self.aj}: e: {self.vertex}->{self.vertex_next}, t: {self.time} (EDGE)')
        else:
            print(
                f'ai {self.ai}, aj {self.aj}: v: {self.vertex}, v_prev: {self.vertex_prev} t: {self.time}, overlap_t: {self.overlap_time} (OVERLAP)')


class Agent:
    def __init__(self, id, start, end, speed, radius):
        """
        Structure for an agent
        :param id: agent's id
        :param start: agent's start node
        :param end: agent's end node
        :param speed: agent's speed
        :param radius: agent's radius
        """
        self.id = id
        self.start = start
        self.end = end
        self.speed = speed
        self.radius = radius

    def __str__(self):
        return f'agent {self.id}: from {self.start} to {self.end} with speed {self.speed} and radius {self.radius}'

    def get_center_at_time(self, path, t, nodes):
        """
        Calculates a center of agent at time t
        :param path: agent's path
        :param t: time
        :param nodes: modes from map
        :return: a center of agent at time t
        """
        prev_node = get_prev_node(path, t)
        if prev_node[1][0] <= t <= prev_node[1][1]:  # at vertex
            return nodes[prev_node[0]]
        next_node = get_next_node(path, prev_node)
        if next_node == path[-1]:
            return nodes[self.end]
        return nodes[prev_node[0]].intersect(nodes[next_node[0]], (t - prev_node[1][1]) * self.speed)


def is_in_path(path, n):
    for p in path:
        if p[0] == n:
            return True
    return False


def get_prev_node(path, t, before_vertex=False):
    """
    Finds a node before time t
    :param path: path
    :param t: time
    :param before_vertex: True if agent at time t at node and previous node is needed, False otherwise, default is False
    :return: a node before time t
    """
    prev_node = path[0]
    for n in path:
        if n[1][0] <= t <= n[1][1]:
            if not before_vertex:  # at vertex
                return n
            else:
                return prev_node
        if t > n[1][1]:
            prev_node = n
    return prev_node


def get_next_node(path, prev_node):
    """
    Finds a node after a given node
    :param path: path
    :param prev_node: previous node
    :return: next node
    """
    next_node = path.index(prev_node)
    if next_node != len(path) - 1:
        return path[next_node + 1]
    return path[-1]


def print_path(path, start, end, last_arrive=False):
    """
    Prints path
    :param path: path to print
    :param start: start node
    :param end: end node
    :param last_arrive: True is only last arrival is needed, default is False
    """
    if last_arrive:
        print(path[-1])
        return
    for n in path:
        arrive, depart = n[1]
        print(f"{n[0]}: ", end='')
        if start != n[0] and end != n[0]:
            print(f"arrive at {round(arrive, 4)}, ", end='')
        if arrive != depart:
            print(f"wait for {round(depart, 4) - round(arrive, 4)}, ", end='')
        if end != n[0]:
            print(f"depart at {round(depart, 4)}")
        else:
            print(f"arrive at {round(arrive, 4)}")


def round_path(paths):
    """
    Rounds paths to 3 decimal digits and concats it to one list.
    :param paths: paths to round
    :return: single list of all paths
    """
    rounded_path = []
    for path in paths:
        for i in range(len(path)):
            rounded_path.append((path[i][0], (round(path[i][1][0], 3), round(path[i][1][1], 3))))
    return rounded_path


class Solution:
    def __init__(self):
        """
        Solution structure
        """
        self.agents = []
        self.paths = []
        self.constraints = defaultdict(list)
        self.cost = 0

    def __eq__(self, other):
        rounded_path = round_path(self.paths)
        rounded_path_other = round_path(other.paths)
        for i in range(0, len(rounded_path)):
            if rounded_path[i] != rounded_path_other[i]:
                return False
        return True

    def time_to_wait(self, i, j, t, nodes):
        """
        Calculates time to wait for overlap conflict
        :param i: agent i id
        :param j: agent j id
        :param t: time of conflict
        :param nodes: nodes from map
        :return: time to wait without j's speed or -1 if no conflict
        """
        ai_center = self.agents[i].get_center_at_time(self.paths[i], t, nodes)
        aj_center = self.agents[j].get_center_at_time(self.paths[j], t, nodes)
        d = ai_center.distance(aj_center)
        if d <= self.agents[i].radius + self.agents[j].radius:
            prev_node = get_prev_node(self.paths[i], t)
            next_node = get_next_node(self.paths[i], prev_node)
            angle = nodes[prev_node[0]].angle(nodes[next_node[0]])

            b = -2 * math.cos(angle * math.pi / 180) * (ai_center.x - aj_center.x) \
                - 2 * math.sin(angle * math.pi / 180) * (ai_center.y - aj_center.y)
            c = (ai_center.x - aj_center.x) ** 2 + (ai_center.y - aj_center.y) ** 2 \
                - (self.agents[i].radius + self.agents[j].radius) ** 2
            t = (-b + math.sqrt(b ** 2 - 4 * c)) / 2
            if t < 0:
                return (-b - math.sqrt(b ** 2 - 4 * c)) / 2
            return t
        return -1

    def print(self, last_arrive=False):
        print('solution cost:', self.cost, '\n')
        for i in range(len(self.paths)):
            print(f"agent id: {i}, path:")
            print_path(self.paths[i], self.agents[i].start, self.agents[i].end, last_arrive)
            self.constraints[i].sort(key=lambda x: x.time)
            for c in self.constraints[i]:
                c.print()
            if i != len(self.paths) - 1:
                print()

    def calculate_cost(self):
        for p in self.paths:
            self.cost += p[-1][1][1]
