from abc import ABC, abstractmethod
from enum import Enum
from typing import List, TYPE_CHECKING, Union, Set
import math

from PyQt5.QtCore import QPointF, QPoint
from PyQt5.QtGui import QColor

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Enums import Nudge, AxialDirection, OddOffsetDirection, EvenOffsetDirection, \
        HexDirection


class Point(QPointF):
    def __init__(self, x, y):
        super().__init__(x, y)


    @property
    def x(self):
        return super().x()


    @property
    def y(self):
        return super().y()


    @property
    def QPointF(self):
        return QPointF(super().x(), super().y())


    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)


    def __mul__(self, other: [float, int, 'Point']) -> 'Point':
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)


    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Position(ABC):
    """
    Parent class for all positions. In framework are used 3 types of positions

       * Offset
       * Cubic
       * Axial

    You can anytime convert between them, but for speed optimization is good practise to use one position type.
    """
    # Correction for aligning along X axis
    CORRECTION_X = 1e-6

    # Correction for aligning along Y axis
    CORRECTION_Y = 2e-6

    # Correction for aligning along Z axis
    CORRECTION_Z = -3e-6


    @property
    @abstractmethod
    def cubic(self) -> 'CubicPosition':
        """ Convert position to Cubic format """
        pass


    @property
    @abstractmethod
    def axial(self) -> 'AxialPosition':
        """ Convert position to Axial format """
        pass


    @property
    @abstractmethod
    def offset(self) -> 'OffsetPosition':
        """ Convert position to Offset format """
        pass


    @property
    @abstractmethod
    def int_coord(self) -> 'Position':
        """ Convert positions values to int values """
        pass


    @abstractmethod
    def __sub__(self, other: 'Position') -> 'Position':
        pass


    @abstractmethod
    def __add__(self, other: 'Position') -> 'Position':
        pass


    def length(self) -> int:
        """ Returns the distance of this position from center one """
        return (abs(self.cubic.x) + abs(self.cubic.y) + abs(self.cubic.z)) // 2


    def interpolate_to(self, start: list, finish: list, progress: float) -> 'Position':
        """"
        Computes interpolated value

        :param start: The starting point
        :param finish: The ending point
        :param progress:  Ration of the progress in between the ends
        :return: Interpolated Position
        """

        x = start[0] + (finish[0] - start[0]) * progress
        y = start[1] + (finish[1] - start[1]) * progress
        z = start[2] + (finish[2] - start[2]) * progress

        return CubicPosition(x, y, z)


    def distance_from(self, position: 'Position') -> int:
        """ Return distance between two positions """
        return (self.cubic - position.cubic).length()


    def distance_to_nearest(self, positions: List['Position']) -> int:
        """
        Computes the distance to nearest of given positions

        :param positions: Set of positions to consider in computation
        :return: Distance to nearest position
        """
        return min([self.distance_from(x) for x in positions])


    Direction = Union["HexDirection", "OddOffsetDirection", "EvenOffsetDirection", "AxialDirection"]


    @abstractmethod
    def neighbour(self, direction: Direction) -> 'Position':
        """
        Computes position of neighbour of this position in specified hex direction

        :param direction: Direction of neighbour to be computed
        :return: Position of neighbour of this position in specified hex direction
        """
        pass


    @abstractmethod
    def get_all_neighbours(self) -> List['Position']:
        """ Return list of all neighbours positions """
        pass


    def plot_line(self, position: 'Position', nudge: 'Nudge') -> List['Position']:
        """
        Computes all positions between this and specified position

        :param position: Final position to plot line to
        :param nudge: Correct line to get result not on exact edge
        :return: All positions between this and specified position
        """
        distance = self.distance_from(position)

        step = 1.0 / max(distance, 1)
        line = list()

        start_x = self.cubic.x + nudge.nudge(Position.CORRECTION_X)
        finish_x = position.cubic.x + nudge.nudge(Position.CORRECTION_X)
        start_y = self.cubic.y + nudge.nudge(Position.CORRECTION_Y)
        finish_y = position.cubic.y + nudge.nudge(Position.CORRECTION_Y)
        start_z = self.cubic.z + nudge.nudge(Position.CORRECTION_Z)
        finish_z = position.cubic.z + nudge.nudge(Position.CORRECTION_Z)

        for i in range(distance + 1):
            line.append(self.interpolate_to([start_x, start_y, start_z], [finish_x, finish_y, finish_z], step * i))

        return line


    @staticmethod
    def from_pixel(point: Union[QPoint, Point, QPointF], transformation: float) -> "AxialPosition":
        """ Compute position from the pixels on the map screen """
        from OrodaelTurrim.Presenter.Widgets.MapWidget import HEXAGON_SIZE

        x_size = (HEXAGON_SIZE.x * transformation / 2)
        y_size = (HEXAGON_SIZE.y * transformation / math.sqrt(3))

        q = (2 / 3 * point.x()) / x_size
        r = ((-1 / 3 * point.x()) / x_size) + ((math.sqrt(3) / 3 * point.y()) / y_size)

        return AxialPosition(q, r).int_coord


class CubicPosition(Position):
    """ Cubic position representation """
    __slots__ = ['__x_position', '__y_position', '__z_position']


    def __init__(self, x_position, y_position, z_position):

        self.__x_position = int(x_position) if type(x_position) is str else x_position
        self.__y_position = int(y_position) if type(y_position) is str else y_position
        self.__z_position = int(z_position) if type(z_position) is str else z_position


    @property
    def cubic(self) -> 'CubicPosition':
        return self


    @property
    def axial(self) -> 'AxialPosition':
        return AxialPosition(self.__x_position, self.__z_position)


    @property
    def offset(self) -> 'OffsetPosition':
        col = self.__x_position
        row = self.__z_position + (self.__x_position - (self.__x_position & 1)) // 2
        return OffsetPosition(col, row)


    @property
    def x(self):
        return self.__x_position


    @property
    def y(self):
        return self.__y_position


    @property
    def z(self):
        return self.__z_position


    def neighbour(self, direction: 'HexDirection') -> 'CubicPosition':
        return self + direction.value


    def get_all_neighbours(self) -> List['CubicPosition']:
        return [
            CubicPosition(self.x + 0, self.y - 1, self.z + 1),  # UPPER
            CubicPosition(self.x + 1, self.y - 1, self.z + 0),  # RIGHT_UPPER
            CubicPosition(self.x + 1, self.y + 0, self.z - 1),  # RIGHT_LOWER
            CubicPosition(self.x + 0, self.y + 1, self.z - 1),  # LOWER
            CubicPosition(self.x - 1, self.y + 1, self.z - 0),  # LEFT_LOWER
            CubicPosition(self.x - 1, self.y + 0, self.z + 1),  # LEFT_UPPER
        ]


    def __eq__(self, other: 'CubicPosition'):
        return self.x == other.cubic.x and self.y == other.cubic.y and self.z == other.cubic.z


    def __lt__(self, other):
        return self.x < other.cubic.x if self.x != other.cubic.x else self.y < other.cubic.y if self.y != other.cubic.y else self.z < other.z


    def __hash__(self):
        return hash((self.offset.q, self.offset.r))


    def __add__(self, other: Position):
        return CubicPosition(self.cubic.x + other.cubic.x, self.cubic.y + other.cubic.y, self.cubic.z + other.cubic.z)


    def __sub__(self, other: Position):
        return CubicPosition(self.x - other.cubic.x, self.y - other.cubic.y, self.z - other.cubic.z)


    @property
    def int_coord(self):
        rx = round(self.__x_position)
        ry = round(self.__y_position)
        rz = round(self.__z_position)

        x_diff = abs(rx - self.__x_position)
        y_diff = abs(ry - self.__y_position)
        z_diff = abs(rz - self.__z_position)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        self.__x_position = rx
        self.__y_position = ry
        self.__z_position = rz
        return CubicPosition(rx, ry, rz)


    def __repr__(self):
        return '<Cubic> {}, {}, {}'.format(self.x, self.y, self.z)


    def xml_string(self):
        return 'Cubic {} {} {}'.format(self.x, self.y, self.z)


    @property
    def string(self):
        return '{} {} {}'.format(self.x, self.y, self.z)


class AxialPosition(Position):
    """ Axial position representation """
    __slots__ = ['__q', '__r']


    def __init__(self, q: Union[int, float], r: Union[int, float]):
        self.__q = int(q) if type(q) is str else q
        self.__r = int(r) if type(r) is str else r


    @property
    def cubic(self) -> 'CubicPosition':
        return CubicPosition(self.__q, -self.__q - self.__r, self.__r)


    @property
    def axial(self) -> 'AxialPosition':
        return self


    @property
    def offset(self) -> 'OffsetPosition':
        return self.cubic.offset


    @property
    def q(self):
        return self.__q


    @property
    def r(self):
        return self.__r


    @property
    def int_coord(self) -> "AxialPosition":
        p = self.cubic.int_coord.axial
        return AxialPosition(p.q, p.r)


    def neighbour(self, direction: 'AxialDirection') -> 'AxialPosition':
        return self + direction.value


    def get_all_neighbours(self) -> List['AxialPosition']:
        return [
            AxialPosition(self.q + 0, self.r - 1),  # UPPER
            AxialPosition(self.q + 1, self.r - 1),  # RIGHT_UPPER
            AxialPosition(self.q + 1, self.r + 0),  # RIGHT_LOWER
            AxialPosition(self.q + 0, self.r + 1),  # RIGHT_LOWER
            AxialPosition(self.q - 1, self.r + 1),  # LEFT_LOWER
            AxialPosition(self.q - 1, self.r + 0),  # LEFT_UPPER
        ]


    def __eq__(self, other: 'AxialPosition') -> bool:
        return self.q == other.axial.q and self.r == other.axial.r


    def __hash__(self):
        return hash((self.offset.q, self.offset.r))


    def __repr__(self):
        return '<Axial> {}, {}'.format(self.q, self.r)


    def __add__(self, other: Position):
        return AxialPosition(self.q + other.axial.q, self.r + other.axial.r)


    def __sub__(self, other: Position):
        return AxialPosition(self.q - other.axial.q, self.r - other.axial.r)


    def xml_string(self):
        return 'Axial {} {}'.format(self.q, self.r)


    @property
    def string(self):
        return '{} {}'.format(self.q, self.r)


class OffsetPosition(Position):
    """ Offset position representation """
    __slots__ = ['__q', '__r']


    def __init__(self, q: int, r: int):
        self.__q = int(q) if type(q) is str else q
        self.__r = int(r) if type(r) is str else r


    @property
    def cubic(self) -> 'CubicPosition':
        x = self.__q
        z = self.__r - (self.__q - (self.__q & 1)) // 2
        y = -x - z
        return CubicPosition(x, y, z)


    @property
    def axial(self) -> 'AxialPosition':
        return self.cubic.axial


    @property
    def offset(self) -> 'OffsetPosition':
        return self


    @property
    def q(self):
        return self.__q


    @property
    def r(self):
        return self.__r


    def neighbour(self, direction: Union['OddOffsetDirection', 'EvenOffsetDirection']) -> 'OffsetPosition':
        return self + direction.value


    def get_all_neighbours(self) -> List['OffsetPosition']:
        if self.q & 1 == 1:
            return [
                OffsetPosition(self.q + 0, self.r - 1),  # UPPER
                OffsetPosition(self.q + 1, self.r + 0),  # RIGHT_UPPER
                OffsetPosition(self.q + 1, self.r + 1),  # RIGHT_LOWER
                OffsetPosition(self.q + 0, self.r + 1),  # LOWER
                OffsetPosition(self.q - 1, self.r + 1),  # LEFT_LOWER
                OffsetPosition(self.q - 1, self.r + 0),  # LEFT_UPPER
            ]
        else:
            return [
                OffsetPosition(self.q + 0, self.r - 1),  # UPPER
                OffsetPosition(self.q + 1, self.r - 1),  # RIGHT_UPPER
                OffsetPosition(self.q + 1, self.r + 0),  # RIGHT_LOWER
                OffsetPosition(self.q + 0, self.r + 1),  # LOWER
                OffsetPosition(self.q - 1, self.r + 0),  # LEFT_LOWER
                OffsetPosition(self.q - 1, self.r - 1),  # LEFT_UPPER
            ]


    def __eq__(self, other: 'OffsetPosition'):
        return self.q == other.offset.q and self.r == other.offset.r


    def __hash__(self):
        return hash((self.offset.q, self.offset.r))


    def __lt__(self, other):
        if self.q == other.q:
            return self.r < other.q

        return self.q < other.q


    def __add__(self, other: Position):
        return OffsetPosition(self.q + other.offset.q, self.r + other.offset.r)


    def __sub__(self, other: Position):
        return OffsetPosition(self.q - other.offset.q, self.r - other.offset.r)


    @property
    def int_coord(self):
        p = self.cubic.int_coord.offset
        return OffsetPosition(p.q, p.r)


    def __repr__(self):
        return '<Offset> {}, {}'.format(self.q, self.r)


    def xml_string(self):
        return 'Offset {} {}'.format(self.q, self.r)


    @property
    def string(self):
        return '{} {}'.format(self.q, self.r)
