import random
from typing import Optional, TYPE_CHECKING
import pygame as pg


from class_types.tile_types import TileTypes
from game.game_controller import GameController
from game.textures import Textures
from game.setting import TILE_SIZE

if TYPE_CHECKING:
    from buildable.buildable import Buildable
    from walkers.walker import Walker


class Tile:



    def __init__(self, col: int, row: int):
        self.type = TileTypes.GRASS
        self.id_number = 0
        self.building: Optional[Buildable] = None
        self.show_tile = True
        self.road = None
        self.x = row
        self.y = col

        self.water_access = False

        self.walkers: list['Walker'] = []

        cartesian_coord = [
            (col * TILE_SIZE, row * TILE_SIZE),
            (col * TILE_SIZE + TILE_SIZE, row * TILE_SIZE),
            (col * TILE_SIZE + TILE_SIZE, row * TILE_SIZE + TILE_SIZE),
            (col * TILE_SIZE, row * TILE_SIZE + TILE_SIZE)
        ]

        def convert_cartesian_to_isometric(x, y):
            return x - y, (x + y) / 2

        self.isometric_coord = [convert_cartesian_to_isometric(x, y) for x, y in cartesian_coord]
        self.render_coord = (
            min([x for x, y in self.isometric_coord]),
            min([y for x, y in self.isometric_coord])
        )

    def get_id_number(self):
        return self.id_number

    def set_id_number(self, new_id):
        self.id_number = new_id

    def find_key(self,v, dictio : dict):
        for k, val in dictio.items():
            if v == val:
                return k

    def get_render_coord(self):
        return self.render_coord

    def get_isometric_coord(self):
        return self.isometric_coord

    def get_type(self):
        return self.type

    def set_type(self, new_type):
        self.type = new_type

    def get_water_access(self):
        return self.water_access

    def set_water_access(self, water_access: bool):
        self.water_access = water_access

    def get_building(self):
        return self.building

    def set_building(self, new_building, show_building: bool = True):
        self.building = new_building
        self.show_tile = show_building

    def get_road(self):
        return self.road

    def set_road(self, new_road):
        self.road = new_road

    def set_show_tile(self,show_tile:bool):
        self.show_tile = show_tile

    def get_show_tile(self):
        return self.show_tile

    def get_texture(self) -> pg.Surface:
        dic = Textures.get_texture(self.get_type())
        if not self.show_tile:
            return dic[self.get_id_number()]
        if self.building:
            return self.building.get_texture()
        if self.road:
            return Textures.get_texture(self.road.get_road_type())
        if self.id_number:
            return dic[self.get_id_number()]
        else:
            return dic
    def get_delete_texture(self):
        if not self.show_tile:
            return Textures.get_texture(TileTypes.GRASS)
        if self.road:
            return Textures.get_delete_texture(self.road.get_road_type())
        if self.building:
            return self.building.get_delete_texture()
        return Textures.get_delete_texture(self.type)

    def is_buildable(self):
        return self.building is None \
               and self.road is None \
               and self.type in (TileTypes.WHEAT, TileTypes.GRASS)

    def is_destroyable(self):
        return (self.building and self.building.is_destroyable()) or self.road

    def destroy(self):
        if self.building:
            self.building.destroy()
            self.building = None
        self.road = None
        for walker in self.walkers:
            walker.associated_building.associated_walker.delete()

    def add_walker(self, walker: 'Walker'):
        self.walkers.append(walker)

    def remove_walker(self, walker: 'Walker'):
        self.walkers.remove(walker)

    def get_adjacente_tiles(self, radius: int = 0):
        adjacentes_tiles = []

        grid = GameController.get_instance().get_map()

        if radius == 0:
            coords = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        else:
            coords = [(x, y) for y in range(-radius, radius+1) for x in range(-radius, radius+1)]

        for coord in coords:
            try:
                adjacentes_tiles.append(grid[self.x + coord[0]][self.y + coord[1]])
            except IndexError:
                continue

        return adjacentes_tiles
