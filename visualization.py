import numpy as np
import pygame

class GameBoard:

    def __init__(self, players):
        pygame.init()
        self.size = (1500, 1000)
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((255, 255, 255))
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.players = players
        self.render_player_names()
        self.render_player_scores()
        self.render_player_tricks()
        pygame.event.get()

    def render_all(self, turn, bid, players):
        pygame.event.get()
        self.screen.fill((255, 255, 255))
        self.render_player_names()
        self.render_player_scores()
        self.render_player_tricks()
        self.render_hand(players[turn].hand)

    def render_player_names(self):
        for i, player in enumerate(self.players):
            text_surface = self.my_font.render((player.name + ": ").encode('utf-8'), False, (0, 0, 0))
            self.screen.blit(text_surface, (0,40*i))
        pygame.display.flip() 

    def render_player_scores(self):
        for i, player in enumerate(self.players):
            text_surface = self.my_font.render(str(player.points).encode('utf-8'), False, (0, 0, 0))
            self.screen.blit(text_surface, (120,40*i))
        pygame.display.flip()  

    def render_player_tricks(self):
        for i, player in enumerate(self.players):
            text_surface = self.my_font.render( ("Tricks:" + str(player.tricks)).encode('utf-8'), False, (0, 0, 0))
            self.screen.blit(text_surface, (150,40*i))
        pygame.display.flip()

    def render_hand(self, hand):

        for i, card in enumerate(hand.cards):
            self.screen.blit(card.image, (200 + 100*i, self.size[1]-200))
            pygame.display.flip()





