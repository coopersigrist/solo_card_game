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

    def render_all(self, turn, bid, players, played_cards=None):
        pygame.event.get()
        self.screen.fill((255, 255, 255))
        self.render_player_names()
        self.render_player_scores()
        self.render_player_tricks()
        self.render_hand(players[turn].hand)
        self.render_played_cards(played_cards)

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

    def render_played_card(self, card, turn):

            spacing = 20
            width = 150
            height = 218
            origin = ((self.size[0] + width)/2 - 250, (self.size[1]+height)/2 - 100)
            spots = [origin, (origin[0]-height-spacing, origin[1]-width-spacing), (origin[0], origin[1]-width-height-2*spacing), (origin[0]+width+spacing, origin[1]-width-spacing)]

            scaled_img = pygame.transform.scale(card.image, (width, height))
            scaled_rotated_image = pygame.transform.rotate(scaled_img, 90*turn)
            self.screen.blit(scaled_rotated_image, spots[turn])
            pygame.display.flip()
    
    def render_played_cards(self, cards):

        if cards == None:
            return

        for card in cards:
            self.render_played_card(card[1], card[2])

    





