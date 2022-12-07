import pygame as pg

from class_types.tile_types import TileTypes
from class_types.road_types import RoadTypes
from components.button import Button
from game.textures import Textures
from game.utils import draw_text

class Panel:
    
    def __init__(self, width, height, event_manager):
        self.width, self.height = width, height

        self.event_manager = event_manager

        self.ressource_panel_color = (204, 174, 132)
        self.building_panel_color = (230, 162, 64)

        # Ressource panel in the top of screen
        self.ressource_panel = pg.Surface((self.width, self.height * 0.04))
        self.ressource_panel_rect = self.ressource_panel.get_rect(topleft=(0, 0))
        self.ressource_panel.fill(self.ressource_panel_color)

        # Building panel in the right screen
        self.building_panel = pg.Surface((self.width * 0.2, self.height * 0.96))
        self.building_panel_rect = self.building_panel.get_rect(topleft=(self.width * 0.8, self.height * 0.04))
        self.building_panel.fill(self.building_panel_color)

        self.build__tree = Button((self.building_panel_rect.left + 20, 800), (120, 80), image=Textures.get_texture(TileTypes.TREE))
        self.build__tree.on_click(lambda: self.set_selected_tile(TileTypes.TREE))

        self.build__rock = Button((self.building_panel_rect.left + 20 + 120 + 20, 800), (120, 80), image=Textures.get_texture(TileTypes.ROCK))
        self.build__rock.on_click(lambda: self.set_selected_tile(TileTypes.ROCK))

        self.build__road = Button((self.building_panel_rect.left + 20, 800 + 80 + 20), (120, 80), image=Textures.get_texture(RoadTypes.TL_TO_BR))
        self.build__road.on_click(lambda: self.set_selected_tile(RoadTypes.TL_TO_BR))

        self.event_manager.register_component(self.build__tree)
        self.event_manager.register_component(self.build__rock)
        self.event_manager.register_component(self.build__road)

        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None
        self.panel_rects = [self.ressource_panel_rect, self.building_panel_rect]


    def draw(self, screen):        
        screen.blit(self.ressource_panel, (0, 0))

        screen.blit(self.building_panel, (self.width * 0.8, self.height * 0.04))

        resource_panel_text = ['File', 'Options', 'Help', 'Advisor', 'Dn: 0', 'Population: 0']
        
        resource_panel_text_pos = [20, 20]

        for text in resource_panel_text:
            
            temp_pos = resource_panel_text_pos.copy()

            draw_text(text, screen, temp_pos, size=42)
            
            resource_panel_text_pos[0] += 200

        self.build__tree.display(screen)
        self.build__rock.display(screen)
        self.build__road.display(screen)

    
    def update(self):
        pass
        # self.event_manager.handle_events()


    def scale_image(self, image, width=None, height=None):  # Procedure function which scales up or down the image specified
        # Default case do nothing
        if (width is None) and (height is None):
            pass

        elif height is None:  # scale only width
            scale = width / image.get_width()
            height = scale * image.get_height()
            image = pg.transform.scale(image, ( int(width), int(height) ))

        elif width is None:  # scale only width
            scale = height / image.get_height()
            width = scale * image.get_width()
            image = pg.transform.scale(image, (int(width), int(height)))

        else:
            image = pg.transform.scale(image, (int(width), int(height)))

        return image


    def scale_image_2x(self, image):
        return pg.transform.scale2x(image)

    def has_selected_tile(self): return self.selected_tile is not None

    def get_selected_tile(self): return self.selected_tile

    def set_selected_tile(self, value): self.selected_tile = value

    def get_panel_rects(self): return self.panel_rects
