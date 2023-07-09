import copy
import sys


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_object(Class, *args, **kwargs):
    return Class(*args, **kwargs)


point1 = Point(1, 2)  # init 사용
point2 = eval("{}({}, {})".format("Point", 2, 4))  # eval(): risky
point3 = getattr(sys.modules[__name__], "Point")(3, 6) # getattr()
point4 = globals()["Point"](4, 8)  # globals()
point5 = make_object(Point, 5, 10) # 클래스 객체 반환하는 함수
point6 = copy.deepcopy(point5)  # 프로토타입 접근
point6.x = 6
point6.y = 12
point7 = point1.__class__(7, 14)  # 클래스 객체에 새 인자 적용: 프로토타입보다 더 나은 대안이 있징
