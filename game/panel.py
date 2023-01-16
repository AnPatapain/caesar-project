import pygame as pg

import backup_game
from class_types.buildind_types import BuildingTypes
from class_types.panel_types import SwitchViewButtonTypes
from class_types.road_types import RoadTypes
from components.button import Button
from components.menu_deroulant import Menu_Deroulant
from events.event_manager import EventManager
from game.game_controller import GameController
from game.mini_map import MiniMap
from game.textures import Textures
from game.utils import draw_text
from map_element.tile import Tile
from game.overlay import Overlay

TOPBAR_HEIGHT = 46
PANEL_WIDTH = 162
PANEL_HEIGHT = 1080 - TOPBAR_HEIGHT

class Panel:
    def __init__(self, width, height, screen):
        self.width, self.height, self.screen = width, height, screen

        # Mini_Map
        self.mini_map = MiniMap()
        self.sous_menu = False

        self.ressource_panel_color = (204, 174, 132)
        self.building_panel_color = (230, 162, 64)

        # Ressource panel in the top of screen
        self.ressource_panel = pg.Surface((self.width, TOPBAR_HEIGHT)).convert()
        self.ressource_panel_rect = self.ressource_panel.get_rect(topleft=(0, 0))
        self.ressource_panel.fill(self.ressource_panel_color)
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (0, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.BARRE), (500, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 - 304, 0))
        self.ressource_panel.blit(Textures.get_texture(SwitchViewButtonTypes.DYNAMIC_DISPLAY), (1000 + 304, 0))

    # Building panel in the right screen
        self.building_panel = pg.Surface((PANEL_WIDTH, self.height)).convert()
        self.building_panel_rect = self.building_panel.get_rect(topleft=(self.width - PANEL_WIDTH, TOPBAR_HEIGHT))
        self.building_panel.fill(self.building_panel_color)
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.TOP_PANNEL), (0, 0))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.BOTTOM_PANNEL), (0, 496 - TOPBAR_HEIGHT))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.SCULPTURE), (0, PANEL_HEIGHT - 120))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.MINI_SCULPTURE), (7, 216))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.JULIUS), (7, 200 - TOPBAR_HEIGHT))
        self.building_panel.blit(Textures.get_texture(SwitchViewButtonTypes.EUROPEAN), (84, 200 - TOPBAR_HEIGHT))



        self.file_continue_game = Button((0,46),(200, 46), text="Continue Game", center_text=False, text_size=30)
        self.file_continue_game.on_click(lambda : self.set_sous_menu(False))

        self.file_save_game = Button((0, 92), (200, 46), text="Save Game", center_text=False, text_size=30)
        self.file_save_game.on_click(lambda: backup_game.save_game("save.bin"))

        self.file_load_game = Button((0, 138), (200, 46), text="Load Game", center_text=False, text_size=30)
        self.file_load_game.on_click(lambda: backup_game.load_game("save.bin"),lambda : self.set_sous_menu(False))

        self.file_exit_game = Button((0,184),(200, 46), text="Exit Game", center_text=False, text_size=30)
        self.file_exit_game.on_click(lambda : pg.quit())

        self.file_sous_menu_list = [self.file_continue_game, self.file_save_game, self.file_load_game, self.file_exit_game]

        self.file = Button((0, 0), (100, 46), image=Textures.get_texture(SwitchViewButtonTypes.FILE_BUTTON), selectable=True)
        self.file_menu = Menu_Deroulant(self.file, self.file_sous_menu_list, self.screen)
        EventManager.register_menu_deroulant(self.file_menu)
        self.file.on_click2(lambda : self.set_sous_menu(True))

        # Overlay button
        self.change_overlay = Button((self.width - 158, 49), (117,25), text_fn=Overlay.get_instance().get_name,
                                     center_text=True,text_size=30)
        self.change_overlay.on_click(lambda: Overlay.get_instance().set_overlay_types())

        button_size = (39, 26)
        self.build__road = Button((self.width - 49, 277 + TOPBAR_HEIGHT), button_size,
                                  image=Textures.get_texture(SwitchViewButtonTypes.BUTTON7),
                                  image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON7_HOVER),
                                  image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON7_SELECTED),
                                  disable_unselect=True, selectable=True, text_pop_up="Build road")
        self.build__road.on_click(lambda: self.set_selected_tile(RoadTypes.TL_TO_BR))

        self.destroy_tile = Button((self.width - 99, 277 + TOPBAR_HEIGHT), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON6),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON6_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON6_SELECTED),
                                   disable_unselect=True, selectable=True, text_pop_up="Destroy")
        self.destroy_tile.on_click(lambda: self.set_selected_tile(BuildingTypes.PELLE))  # image qui est sur le curseur

        self.build__house = Button((self.width - 149, 277 + TOPBAR_HEIGHT), button_size,
                                   image=Textures.get_texture(SwitchViewButtonTypes.BUTTON5),
                                   image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON5_HOVER),
                                   image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON5_SELECTED),
                                   disable_unselect=True, selectable=True, text_pop_up="Build house")
        self.build__house.on_click(lambda: self.set_selected_tile(BuildingTypes.VACANT_HOUSE))

        self.build__prefecture = Button((self.width - 99, 385 + TOPBAR_HEIGHT), button_size,
                                        image=Textures.get_texture(SwitchViewButtonTypes.BUTTON15),
                                        image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON15_HOVER),
                                        image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON15_SELECTED),
                                        disable_unselect=True, selectable=True, text_pop_up="Build Prefecture")
        self.build__prefecture.on_click(lambda: self.set_selected_tile(BuildingTypes.PREFECTURE))

        self.build__well = Button((self.width - 149, 312 + TOPBAR_HEIGHT), button_size,
                                  image=Textures.get_texture(SwitchViewButtonTypes.BUTTON8),
                                  image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON8_HOVER),
                                  image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON8_SELECTED),
                                  disable_unselect=True, selectable=True, text_pop_up="Build well")
        self.build__well.on_click(lambda: self.set_selected_tile(BuildingTypes.WELL))

        self.build__engineer_post = Button((self.width - 149, 385 + TOPBAR_HEIGHT), button_size,
                                           image=Textures.get_texture(SwitchViewButtonTypes.BUTTON14),
                                           image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON14_HOVER),
                                           image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON14_SELECTED),
                                           disable_unselect=True, selectable=True, text_pop_up="Build Engineer post")
        self.build__engineer_post.on_click(lambda: self.set_selected_tile(BuildingTypes.ENGINEERS_POST))

        self.increase_speed = Button((self.width - 149, 490 + TOPBAR_HEIGHT), (24,24),
                                     image=Textures.get_texture(SwitchViewButtonTypes.INCREASE_SPEED),
                                     image_hover=Textures.get_texture(SwitchViewButtonTypes.INCREASE_SPEED_HOVER),
                                     image_selected=Textures.get_texture(SwitchViewButtonTypes.INCREASE_SPEED_SELECTED))
        self.increase_speed.on_click(GameController.get_instance().increase_current_speed)

        self.decrease_speed = Button((self.width - 119, 490 + TOPBAR_HEIGHT), (24,24),
                                     image=Textures.get_texture(SwitchViewButtonTypes.DECREASE_SPEED),
                                     image_hover=Textures.get_texture(SwitchViewButtonTypes.DECREASE_SPEED_HOVER),
                                     image_selected=Textures.get_texture(SwitchViewButtonTypes.DECREASE_SPEED_SELECTED))
        self.decrease_speed.on_click(GameController.get_instance().decrease_current_speed)

        self.build__senate = Button((self.width - 49, 349 + 46), button_size,
                                    image=Textures.get_texture(SwitchViewButtonTypes.BUTTON13),
                                    image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON13_HOVER),
                                    image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON13_SELECTED),
                                    disable_unselect=True, selectable=True, text_pop_up="Build Senate")
        self.build__senate.on_click(lambda: self.set_selected_tile(BuildingTypes.SENATE))

        self.build__hospital = Button((self.width - 100, 312 + 46), button_size,
                                      image=Textures.get_texture(SwitchViewButtonTypes.BUTTON9),
                                      image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON9_HOVER),
                                      image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON9_SELECTED),
                                      disable_unselect=True, selectable=True, text_pop_up="Build Hospital")
        self.build__hospital.on_click(lambda: self.set_selected_tile(BuildingTypes.HOSPITAL))

        self.build__temple = Button((self.width - 49, 312 + 46), button_size,
                                    image=Textures.get_texture(SwitchViewButtonTypes.BUTTON10),
                                    image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON10_HOVER),
                                    image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON10_SELECTED),
                                    disable_unselect=True, selectable=True, text_pop_up="Religion")
        self.build__temple.on_click(lambda: self.set_selected_tile(BuildingTypes.TEMPLE))

        self.build__school = Button((self.width - 150, 349 + 46), button_size,
                                    image=Textures.get_texture(SwitchViewButtonTypes.BUTTON11),
                                    image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON11_HOVER),
                                    image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON11_SELECTED),
                                    disable_unselect=True, selectable=True, text_pop_up="Build School")
        self.build__school.on_click(lambda: self.set_selected_tile(BuildingTypes.SCHOOL))

        self.build__theatre = Button((self.width - 100, 349 + 46), button_size,
                                     image=Textures.get_texture(SwitchViewButtonTypes.BUTTON12),
                                     image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON12_HOVER),
                                     image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON12_SELECTED),
                                     disable_unselect=True, selectable=True, text_pop_up="Build Theatre")
        self.build__theatre.on_click(lambda: self.set_selected_tile(BuildingTypes.THEATRE))

        self.build__commerce = Button((self.width - 49, 385 + 46), button_size,
                                    image=Textures.get_texture(SwitchViewButtonTypes.BUTTON16),
                                    image_hover=Textures.get_texture(SwitchViewButtonTypes.BUTTON16_HOVER),
                                    image_selected=Textures.get_texture(SwitchViewButtonTypes.BUTTON16_SELECTED),
                                    disable_unselect=True, selectable=True, text_pop_up="Build Market")
        self.build__commerce.on_click2(lambda : self.set_sous_menu(True))

        self.build__farm = Button((1000, 431), (200, 26), text="Wheat Farm", center_text=False, text_size=26)
        self.build__farm.on_click(lambda: self.set_selected_tile(BuildingTypes.WHEAT_FARM),lambda : self.set_sous_menu(False))

        self.build__market = Button((1000, 459), (200, 26), text="Market", center_text=False, text_size=26)
        self.build__market.on_click(lambda: self.set_selected_tile(BuildingTypes.MARKET), lambda: self.set_sous_menu(False))

        self.build__granary = Button((1000, 487), (200, 26), text="Granary", center_text=False, text_size=26)
        self.build__granary.on_click(lambda: self.set_selected_tile(BuildingTypes.GRANARY), lambda: self.set_sous_menu(False))

        self.commerce_menu = Menu_Deroulant(self.build__commerce, [self.build__farm, self.build__granary, self.build__market], self.screen)
        EventManager.register_menu_deroulant(self.commerce_menu)


        self.button_list = [
            self.destroy_tile, self.build__house, self.build__prefecture, self.build__road, self.build__senate,
            self.build__well, self.build__hospital, self.build__school, self.build__temple, self.build__commerce,
            self.build__theatre, self.build__engineer_post, self.change_overlay, self.increase_speed, self.decrease_speed,
            self.file
        ]

        for button in self.button_list:
            EventManager.register_component(button)

        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None
        self.panel_rects = [self.ressource_panel_rect, self.building_panel_rect]

    def draw(self, screen):
        screen.blit(self.ressource_panel, (0, 0))
        screen.blit(self.building_panel, (self.width - 162, TOPBAR_HEIGHT))


        # Can't draw on the building_panel because we need absolute position to move the camera with the mouse listener
        self.mini_map.draw(screen)

        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON1), (self.width - 155, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON2), (self.width - 116, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON3), (self.width - 78, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON4), (self.width - 39, 230))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON17), (self.width - 150, 420 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON18), (self.width - 100, 420 + 46))
        screen.blit(Textures.get_texture(SwitchViewButtonTypes.BUTTON19), (self.width - 49, 420 + 46))

        draw_text("Options         Help         Advisors", screen, color=pg.Color(50, 30, 0), size=38, pos=(120, 10))

        last_button_to_display = None

        for button in self.get_buttons_list():
            if not button.is_hovered():
                button.display(screen)
            elif button.is_hovered():
                last_button_to_display = button

        if last_button_to_display is not None:
            last_button_to_display.display(screen)

        if self.sous_menu:
            for sous_menu in [self.file_menu, self.commerce_menu]:
                if sous_menu.get_isActive():
                    sous_menu.display()


    def update(self):
        self.mini_map.update()

    def has_selected_tile(self):
        return self.selected_tile is not None

    def get_selected_tile(self) -> Tile:
        return self.selected_tile

    def set_selected_tile(self, value):
        self.selected_tile = value
        print(value)
        if value == BuildingTypes.VACANT_HOUSE:
            self.build__house.set_selected(True)
            for button in self.get_buttons_list():
                if button != self.build__house:
                    button.set_selected(False)
        elif value == BuildingTypes.PELLE:
            self.destroy_tile.set_selected(True)
            for button in self.get_buttons_list():
                if button != self.destroy_tile:
                    button.set_selected(False)
        elif value == BuildingTypes.PREFECTURE:
            self.build__prefecture.set_selected(True)
            for button in self.get_buttons_list():
                if button != self.build__prefecture:
                    button.set_selected(False)
        elif value == 6:
            self.build__road.set_selected(True)
            for button in self.get_buttons_list():
                if button != self.build__road:
                    button.set_selected(False)
        elif value == BuildingTypes.WHEAT_FARM or value == BuildingTypes.MARKET or value == BuildingTypes.GRANARY:
            self.build__commerce.set_selected(True)
            for button in self.get_buttons_list():
                if button != self.build__commerce:
                    button.set_selected(False)
        elif value == BuildingTypes.WELL:
            self.build__well.set_selected(True)
            for button in self.get_buttons_list():
                if button != self.build__well:
                    button.set_selected(False)

    def get_panel_rects(self):
        return self.panel_rects

    def get_mini_map(self): return self.mini_map

    def get_buttons_list(self):
        return self.button_list

    def set_sous_menu(self, status):
        self.sous_menu = status





