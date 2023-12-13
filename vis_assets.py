import pygame
import game

class Button():

    def __init__(self, text, x=0, y=0, width=100, height=50, allowed=True, command=None, returner=None):

        BLACK = (  0,   0,   0)

        self.width = width
        self.height = height


        self.text = text
        self.command = command
        self.allowed = allowed
        self.returner = returner
        
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill((190,190,190))

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill((80,80,80))

        self.image_not_allowed = pygame.Surface((width, height))
        self.image_not_allowed.fill((200,100,100))

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.SysFont('freesansbold.ttf', 40)
        
        text_image = font.render(text, True, BLACK)
        text_rect = text_image.get_rect(center = self.rect.center)
        
        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y

        self.hovered = False
        #self.clicked = False

    def update(self):

        if self.allowed:
            if self.hovered:
                self.image = self.image_hovered
            else:
                self.image = self.image_normal
        else:
            self.image = self.image_not_allowed
        
    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            mousex,mousey = pygame.mouse.get_pos()
            self.hovered = (mousex >= self.x) and (mousex <= self.x + self.width) and (mousey >= self.y) and (mousey <= self.y + self.height)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.allowed:
            if self.hovered:
                return self.returner
        
        return None
    
class Card():

    def __init__(self, img, x=0, y=0, scale=0.5, rotation=0, hoverable=True, returner=0):

        self.image = img
        self.x = x
        self.y = y
        self.HEIGHT = int(726 * scale)
        self.WIDTH = int(500 * scale)

        self.hovered = False
        self.hoverable = hoverable
        self.returner = returner
        self.rotation = rotation

    def update(self):
        return
        
    def draw(self, surface):

        scaled_img = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        scaled_rotated_image = pygame.transform.rotate(scaled_img, self.rotation)
        surface.blit(scaled_rotated_image, (self.x, self.y - (self.hovered * self.hoverable) * 100))

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            mousex,mousey = pygame.mouse.get_pos() 
            self.hovered = (mousex >= self.x) and (mousex <= self.x + self.WIDTH/2) and (mousey >= self.y) and (mousey <= self.y + self.HEIGHT)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                return self.returner
        
        return None

class Hand():
    def __init__(self, cards, x=0, y=0, scale=0.5, rotation=0, hoverable=True, returner=0, spacing=0.5):

        self.cards = []
        self.x = x
        self.y = y

        self.HEIGHT = int(726 * scale)
        self.WIDTH = int(500 * scale)

        self.hovered = False
        self.hoverable = hoverable
        self.returner = returner
        self.rotation = rotation

        # Overlap between cards
        self.spacing = spacing
            

        for i, card in enumerate(cards):
            drawable_card = Card(card.image, x=x+i*(int(self.WIDTH * spacing)), y=y, scale=scale, rotation=0, hoverable=hoverable,returner=i)
            self.cards.append(drawable_card)

    def update(self):

        for card in self.cards:
            card.update()

        
    def draw(self, surface):

        for card in self.cards:
            card.draw(surface)

    def handle_event(self, event):

        for card in self.cards:
            temp = card.handle_event(event)
            if temp is not None:
                return temp
        
        return None
    
class Bids():

    def __init__(self, high_bid, x=0, y=0, n_in_row=4):
        Bid_list = [("pass", 0),("frock", 2),("nolo", 3),("wedding",4),("solo",5),("updibuck",9),("grando",10),("solo-du",26),("grando-du",27)]
        button_length = 150

        self.button_list = []
        self.button_list.append(Button("pass", x, y, button_length, 50, allowed=True, returner=0))

        for i, (bid,points) in enumerate(Bid_list[1:]):
            button_add = Button(bid, x + (1 + (i%n_in_row))*(button_length+20), y + (i > n_in_row-1)*75, width=button_length, allowed=(points>high_bid), returner=points)
            self.button_list.append(button_add)
        
    def update(self):

        for button in self.button_list:
            button.update()

        
    def draw(self, surface):

        for button in self.button_list:
            button.draw(surface)

    def handle_event(self, event):

        for button in self.button_list:
            temp = button.handle_event(event)
            if temp is not None:
                return temp
        
        return None

class Trump_suits():

    def __init__(self, hand, x=50, y=400):

        suits = ["diamonds", "hearts", "spades", "clubs"]
        self.allowed = [True, True, True, True]

        trump_indicator_cards = []

        for i in range(4):
            self.allowed[i] = self.allowable(hand, suits[i])
            trump_indicator_cards.append(game.Card(rank="Ace", value=14, suit=suits[i], num=0))
            if not self.allowed[i]:
                trump_indicator_cards[i].image = pygame.transform.grayscale(trump_indicator_cards[i].image)

        self.hand = Hand(trump_indicator_cards,x=x, y=y, scale=0.5,rotation=0,hoverable=False,spacing=1.25 ) 

    def allowable(self, hand, suit):
        for card in hand:
            if card.suit == suit:
                return True
        
        return False
    
    def update(self):
        self.hand.update()

        
    def draw(self, surface):
        self.hand.draw(surface)

    def handle_event(self, event):
        self.hand.handle_event(event)


