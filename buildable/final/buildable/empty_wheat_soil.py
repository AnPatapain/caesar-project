from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class Empty_wheat_soil(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.EMPTY_WHEAT_SOL, (1, 1),0,0)