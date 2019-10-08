import math


def distance_between_objects(obj1, obj2) -> float:
    return math.sqrt((obj2.rect.x - obj1.rect.x) ** 2 + (obj2.rect.y - obj1.rect.y) ** 2)
