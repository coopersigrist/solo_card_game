import random
import _ctypes
from typing import Tuple, Dict, Any

def di(obj_id):
    """ Inverse of id() function. """
    return _ctypes.PyObj_FromPtr(obj_id)

suits = ['diamonds', 'hearts', 'spades', 'clubs']
ranks = ['7','8','9','10','Jack','Queen','King', 'Ace']
values = [7,8,9,10,11,12,13,14]

QUEEN_OF_CLUBS=30
QUEEN_OF_SPADES=22

class Card:
    def __init__(self, rank, value, suit, num):
        '''
        class for a single card
        :param rank: the name of the card (i.e, "7" or "king")
        :param value: the actual numeric value of the card (7 - 14), Ace is high
        :param suit: the suit of the card, Diamond, Heart, Spade, Club
        '''
        self.rank = rank
        self.value = value
        self.suit = suit
        self.num = num
        
    def __str__( self ):
        return self.rank + " of " + self.suit

    def val(self, suit, lead_suit):
        '''
        Calculation of the value of this specific card given suit and lead
        :param suit: the trump suit of a given calculation
        :param lead_suit: the suit that was led for a given trick
        '''
        if suit == None:
            print(self.value * int(self.suit == lead_suit))
            return self.value * int(self.suit == lead_suit)
        else:
            if self.num == QUEEN_OF_CLUBS:
                return 1000
            elif self.value == 7 and (self.suit == suit):
                return 999
            elif self.num == QUEEN_OF_SPADES:
                return 998
            else:
                return (self.value * int(self.suit == lead_suit)) + (2 * self.value * int(self.suit == suit))

'''
A solo deck, 7 - Ace of all four suits
'''
DECK = [Card(ranks[num-7], values[num-7], suit, (num - 6) + (8 * step)) for num in range(7, 15) for step,suit in enumerate(suits)]

def get_num(card):
    return card.num

class Deck:
    def __init__(self, cards):
        '''
        A deck of Solo cards, 7 - Ace 
        :param cards: the cards used in this deck (a solo deck in this case)
        '''
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
        for step, card in enumerate(self.cards):
            ret += str(card) + " -- " + str(step) + "\n"
        return ret

    def sort(self):
        self.cards = sorted(self.cards, key=get_num)

    def play(self, index):
        return self.cards.pop(index)

    def check(self, index):
        return self.cards[index]

class Player:
    def __init__(self, deck):
        '''
        A solo player, keeps track of score and hand of the player
        '''
        self.hand = Hand(deck)
        self.hand.sort()
        self.points = 0

    def __str__(self):
        return "points: " + str(self.points) + "\n" + str(self.hand)

    def out(self):
        return self.points >= 26

    def play_card(self, index):
        return self.hand.play(index)

    def score(self, points):
        self.points += points

    def check_card(self, index):
        return self.hand.check(index)


BIDS = [("frock", 2),("nolo", 3),("club frock",4),("wedding",4),("club wedding",6),("solo",5),("updibuck",9),("grando",10),("solo-du",26),("grando-du",27)]

class Bid:
    def __init__(self, points, name, suit, partnered):
        '''
        A class for Bids, this will control how many points a trick is worth and how it will be played, there is a specific instance for each possible bid
        :param points: the number of points this bid is worth for the winner
        :param name: the name of this bid
        :param suit: an Optional[string] that is the trump of the bid
        :param partnered: determines whether this trick has a partner, wedding may be different (TODO)
        '''
        self.points = points
        self.name = name
        self.partners = partnered
        self.suit = suit

    def winner(self, lead_suit, played):
        sorted_plays = sorted(played, key=lambda tup: tup[1].val(self.suit, lead_suit), reverse=True)
        return sorted_plays[0]

    def is_partnered(self):
        return self.partners

    def pick_partner(self):
        # TODO ask player to pick partner
        pass

    def pick_suit(self):
        # TODO ask player to pick suit
        pass

    def go_through(self):
        self.points += 2

class Round:
    def __init__(self, turn, bid, players):
        '''
        A single round of cards (4 played in total) this will determine the winner and allow players to play their cards
        :param turn: the first turn of play (a number 0 - 3)
        :param bid: the current bid being played of type Bid
        :param players: a list of Players (only 4 at the moment) 
        '''
        self.played = []
        self.turn = turn
        self.bid = bid
        self.players = players
        self.lead_suit = None

        for ind in range(4):
            self.played.append(self.play_card((self.turn + ind) % 4))

        self.winner = bid.winner(self.lead_suit, self.played)
        print("\nPlayed: \n" + str(self))
        print(str(self.winner[0]) + " wins with " + str(self.winner[1]))
 
    def __str__( self ):
        ret = ''
        for step, card in enumerate(self.played):
            ret += str(card[1]) + " " + str(step) + "\n"
        return ret

    def play_card(self, turn):
        print("Player " + str(turn) + "'s turn\n")
        print("Played: \n" + str(self))
        print("your cards: \n" + str(self.players[turn].hand))

        choice = None
        while choice == None:
            choose = int(input("which card to play?"))
            if not turn == self.turn:
                if any(card.suit == self.lead_suit for card in self.players[turn].hand.cards) and not self.players[turn].check_card(choose).suit == self.lead_suit:
                    print("you have to play on suit -- pulling a Griffin, my god\n")
                else:
                    choice = choose
            else:
                choice = choose
                self.lead_suit = self.players[turn].check_card(choice).suit

        return (self.players[turn], self.players[turn].play_card(choice), turn)

class FullHand:
    def __init__(self,turn,bid,players):
        self.turn = turn
        self.bid = bid
        self.players = players



class Game:
    def __init__(self):
        self.game_deck = Deck(DECK)
        self.game_deck.shuffle()

        self.turn = 1
        self.dealer = 0

        self.player1 = Player(self.game_deck)
        self.player2 = Player(self.game_deck)
        self.player3 = Player(self.game_deck)
        self.player4 = Player(self.game_deck)

        self.players = [self.player1, self.player2, self.player3, self.player4]

    def game_over(self):
        outs = 0
        for player in self.players:
            if player.out():
                outs += 1
        return outs >= 3 

    def loser(self):
        if self.game_over():
            for player in self.players:
                if not player.out():
                    return player
        else:
            return None  

game = Game()
bid = Bid(game.player1, 20, "grando")
print(game.player1)
round = Round(0, bid, game.players)