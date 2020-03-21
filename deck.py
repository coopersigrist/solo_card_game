import random

suits = ['diamonds', 'hearts', 'spades', 'clubs']
ranks = ['7','8','9','10','Jack','Queen','King', 'Ace']

class Card:

    def __init__(self, value, suit, num):
        self.value = value
        self.suit = suit
        self.num = num
        
    def __str__( self ):
        return self.value + " of " + self.suit + " " + str(self.num)


DECK = [Card(ranks[num-7], suit, (num - 6) + (8 * step)) for num in range(7, 15) for step,suit in enumerate(suits)]

def get_num(item):
    return item.num

class Deck:

    def __init__(self, cards):
        self.cards = cards
        self.used = []
        self.size = len(cards)

    def __str__( self ):
        ret = ''
        for card in self.cards:
            ret += str(card) + "\n"
        return ret
    
    def shuffle(self):
        self.cards = self.cards + self.used
        self.used = []
        random.shuffle(self.cards)

    def sort(self):
        self.cards = sorted(self.cards, key=get_num)

    def draw(self, num):
        drawn = []
        for n in range(num):
            next_draw = self.cards.pop(0) 
            drawn.append(next_draw)
            self.used.append(next_draw)
        return drawn

class Hand:

    def __init__(self, deck):
        self.cards = deck.draw(8)

    def __str__( self ):
        ret = ''
        for card in self.cards:
            ret += str(card) + "\n"
        return ret

    def sort(self):
        self.cards = sorted(self.cards, key=get_num)

    def play(self, index):
        return self.cards.pop(index)

   

d1 = Deck(DECK)
print(d1)
d1.shuffle()
print(d1)
d1.sort()
print(d1)