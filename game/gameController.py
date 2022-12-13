from buildable.building import Buildings
from class_types.buildind_types import BuildingTypes
from buildable.buildableCost import buildable_cost

class GameController:
    def __init__(self,initial_denier = 10000):
        self.denier = initial_denier
        self.actual_citizen = 0
        self.max_citizen = 0


    def new_building(self,building : Buildings):
        self.denier -= buildable_cost[building.get_building_type()]
        self.max_citizen += building.get_max_citizen()
        self.max_citizen += building.get_max_citizen()

    def has_enough_denier(self,building_type : BuildingTypes):
        return buildable_cost[building_type] <= self.denier

    def get_denier(self):
        return self.denier

