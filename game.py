import os
import pygame
from pygame.locals import *

from chess import Chess
from utils import Utils


class Game:
    def __init__(self):

        screen_width = 640
        screen_height = 750

        self.menu_showed = False

        self.running = True

        self.resources = "res"

        pygame.display.init()

        pygame.font.init()

        self.screen = pygame.display.set_mode([screen_width, screen_height])

        window_title = "Chess Game"

        pygame.display.set_caption(window_title)

        icon_src = os.path.join(self.resources, "chess_icon.png")

        icon = pygame.image.load(icon_src)

        pygame.display.set_icon(icon)

        pygame.display.flip()

        self.clock = pygame.time.Clock()

    def start_game(self):

        self.board_offset_x = 0
        self.board_offset_y = 50
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)

        board_src = os.path.join(self.resources, "board.png")

        self.board_img = pygame.image.load(board_src).convert()

        square_length = self.board_img.get_rect().width // 8

        self.board_locations = []

        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append([self.board_offset_x + (x * square_length),
                                                self.board_offset_y + (y * square_length)])

        pieces_src = os.path.join(self.resources, "pieces.png")

        self.chess = Chess(self.screen, pieces_src, self.board_locations, square_length)

        # game loop
        while self.running:
            self.clock.tick(5)

            for event in pygame.event.get():

                key_pressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    self.running = False
                elif key_pressed[K_SPACE]:
                    self.chess.reset()

            winner = self.chess.winner

            if self.menu_showed == False:
                self.menu()
            elif len(winner) > 0:
                self.declare_winner(winner)
            else:
                self.game()

            pygame.display.flip()
            pygame.event.pump()

        pygame.quit()

    def menu(self):
        bg_color = (255, 255, 255)
        self.screen.fill(bg_color)
        black_color = (0, 0, 0)
        start_btn = pygame.Rect(270, 300, 100, 50)
        pygame.draw.rect(self.screen, black_color, start_btn)

        white_color = (255, 255, 255)
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        welcome_text = big_font.render("Chess Game", False, black_color)

        start_btn_label = small_font.render("Play", True, white_color)

        self.screen.blit(welcome_text,
                         ((self.screen.get_width() - welcome_text.get_width()) // 2,
                          150))

        self.screen.blit(start_btn_label,
                         ((start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2,
                           start_btn.y + (start_btn.height - start_btn_label.get_height()) // 2)))

        key_pressed = pygame.key.get_pressed()

        util = Utils()

        if util.left_click_event():
            mouse_coords = util.get_mouse_event()

            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, start_btn, 3)

                self.menu_showed = True
            elif key_pressed[K_RETURN]:
                self.menu_showed = True

    def game(self):
        color = (0, 0, 0)
        self.screen.fill(color)

        self.screen.blit(self.board_img, self.board_dimensions)

        self.chess.play_turn()

        self.chess.draw_pieces()

    def declare_winner(self, winner):

        bg_color = (255, 255, 255)

        self.screen.fill(bg_color)

        black_color = (0, 0, 0)

        reset_btn = pygame.Rect(250, 300, 140, 50)

        pygame.draw.rect(self.screen, black_color, reset_btn)

        white_color = (255, 255, 255)

        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)

        text = winner + " wins!"
        winner_text = big_font.render(text, False, black_color)

        reset_label = "Play Again"
        reset_btn_label = small_font.render(reset_label, True, white_color)

        self.screen.blit(winner_text,
                         ((self.screen.get_width() - winner_text.get_width()) // 2,
                          150))

        self.screen.blit(reset_btn_label,
                         ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2,
                           reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))

        key_pressed = pygame.key.get_pressed()

        util = Utils()

        if util.left_click_event():

            mouse_coords = util.get_mouse_event()

            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):

                pygame.draw.rect(self.screen, white_color, reset_btn, 3)

                self.menu_showed = False

            elif key_pressed[K_RETURN]:
                self.menu_showed = False

            self.chess.reset()

            self.chess.winner = ""
