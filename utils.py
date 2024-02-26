import pygame

class Utils:
    def get_mouse_event(self):
        position = pygame.mouse.get_pos()
        return position

    def left_click_event(self):
        mouse_btn = pygame.mouse.get_pressed()
        left_click = False
        if mouse_btn[0]:
            left_click = True
        return left_click
