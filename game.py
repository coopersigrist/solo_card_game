import random
from typing import Tuple, Dict, Any
import numpy as np
import visualization
import pygame

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

        self.image = pygame.image.load('card_pics/' + self.rank + '_of_' + str(self.suit) + '.png')
        
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
    def __init__(self, cards=[Card(ranks[num-7], values[num-7], suit, (num - 6) + (8 * step)) for num in range(7, 15) for step,suit in enumerate(suits)]):
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
    
    def __len__(self):
        return len(self.cards)

    def sort(self):
        self.cards = sorted(self.cards, key=get_num)

    def play(self, index):
        return self.cards.pop(index)

    def check(self, index):
        return self.cards[index]

    def has_card(self, value, suit):
        return any((card.value == value and card.suit == suit) for card in self.cards)
    
    def has_suit(self, suit):
        return any(card.suit == suit for card in self.cards)

class Player:
    def __init__(self, deck, name=None):
        '''
        A solo player, keeps track of score and hand of the player
        '''
        self.deck = deck
        self.hand = Hand(deck)
        self.hand.sort()
        self.points = 0
        self.tricks = 0
        if name == None:
            self.name = input("what's your name?")
        else:
            self.name = str(name)
        print(str(self))

    def __str__(self):
        return "Name: " + self.name + "\n" + "points: " + str(self.points) + "\n" + str(self.hand)

    def out(self):
        return self.points >= 26

    def play_card(self, index):
        return self.hand.play(index)

    def score(self, points):
        self.points += points

    def sort(self):
        self.hand.sort()

    def check_card(self, index):
        return self.hand.check(index)

    def has_card(self, value, suit):
        return self.hand.has_card(value, suit)
    
    def new_hand(self):
        self.hand = Hand(self.deck)
        self.tricks = 0


BIDS = {"pass": 0,"frock": 2,"nolo": 3,"wedding":4,"solo":5,"updibuck":9,"grando":10,"solo-du":26,"grando-du":27}
BID_NAMES = ["pass","frock","nolo","wedding","solo","updibuck","grando","solo-du","grando-du"]


class Bid:
    def __init__(self, points, name, suit):
        '''
        A class for Bids, this will control how many points a trick is worth and how it will be played, there is a specific instance for each possible bid
        :param points: the number of points this bid is worth for the winner
        :param name: the name of this bid
        :param suit: an Optional[string] that is the trump of the bid
        '''
        self.points = points
        self.name = name
        self.suit = suit

    def winner(self, lead_suit, played):
        sorted_plays = sorted(played, key=lambda tup: tup[1].val(self.suit, lead_suit), reverse=True)
        print(sorted_plays[0][0])
        return sorted_plays[0]

    def go_through(self):
        self.points += 2

    def over(self, bidder, partner, tricks_left):
        return self.won(bidder, partner, tricks_left) or self.lost(bidder, partner, tricks_left)

    def won(self, bidder, partner, tricks_left):
        if self.name in ["frock","wedding","solo","grando"]:
            if self.name in ["frock","wedding"]:
                return bidder.tricks + partner.tricks >= 5
            else:
                return bidder.tricks >= 5
        elif self.name in ["grand-du","solo-du"]:
            return bidder.tricks == 8
        else:
            return bidder.tricks == 0 and tricks_left == 0
    
    def lost(self, bidder, partner, tricks_left):
        if self.name in ["frock","wedding","solo","grando"]:
            if self.name in ["frock","wedding"]:
                return bidder.tricks + partner.tricks < 5 - tricks_left
            else:
                return bidder.tricks < 5 - tricks_left
        elif self.name in ["grand-du","solo-du"]:
            return (bidder.tricks < 8 - tricks_left)
        else:
            return bidder.tricks > 0 

class Round:
    def __init__(self, turn, bid, players, gameboard):
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
            gameboard.render_all((self.turn + ind) % 4, bid, players)
            self.played.append(self.play_card((self.turn + ind) % 4))

        self.winner = bid.winner(self.lead_suit, self.played)
        print("\nPlayed: \n" + str(self))
        print(str(self.winner) + " wins with " + str(self.winner[1]))
        
 
    def __str__( self ):
        ret = ''
        for step, card in enumerate(self.played):
            ret += str(card[1]) + " " + str(step) + "\n"
        return ret

    def play_card(self, turn):
        print("Player " + self.players[turn % 4].name + "'s turn\n")
        print("Played: \n" + str(self))
        print("your cards: \n" + str(self.players[turn].hand))

        choice = None
        while choice == None:
            choose = None
            while choose == None:
                choose = int(input("which card to play?"))
                if choose not in np.arange(len(self.players[turn].hand)):
                    print("That's not an option! (Pick the number next to the card)")
                    choose = None

            if not turn == self.turn:
                if any(card.suit == self.lead_suit for card in self.players[turn].hand.cards) and not self.players[turn].check_card(choose).suit == self.lead_suit:
                    print("you have to play on suit (" + self.lead_suit + ") -- pulling a Griffin, my god\n")
                else:
                    choice = choose
            else:
                choice = choose
                self.lead_suit = self.players[turn].check_card(choice).suit

        return (self.players[turn], self.players[turn].play_card(choice), turn)

class FullHand:
    def __init__(self,turn,bid,bidder,partner,other_team,players,gameboard):
        self.turn = turn
        self.bid = bid
        self.players = players
        tricks_left = 8
        while self.bid.over(bidder, partner, tricks_left) == False:
            self.round = Round(self.turn, self.bid, self.players, gameboard=gameboard)
            gameboard.render_all(turn, bid, players)
            self.turn = self.round.winner[2]
            self.round.winner[0].tricks += 1
            tricks_left -= 1
        if bid.won(bidder, partner, tricks_left):
            bidder.score(bid.points)
            if partner is not None:
                partner.score(bid.points)
        else:
            for player in other_team:
                player.score(bid.points)
        

class Game:
    def __init__(self):
        self.game_deck = Deck(DECK)
        self.game_deck.shuffle()
        self.top_bid = "pass"
        self.forced_suit = None

        self.turn = 1
        self.bid_winner = self.turn
        self.dealer = 0

        self.suit = None

        self.player1 = Player(self.game_deck, name="Cooper")
        self.player2 = Player(self.game_deck, name="Helen")
        self.player3 = Player(self.game_deck, name="LBS")
        self.player4 = Player(self.game_deck, name="PooPoo")

        self.players = [self.player1, self.player2, self.player3, self.player4]



    def start(self):

        self.gameboard = visualization.GameBoard(self.players)
        

        while not self.game_over():


            self.gameboard.render_hand(self.players[self.turn].hand)

            self.bidding()

            self.bidder = self.players[self.bid_winner]
            self.other_team = [player for player in self.players if player not in [self.bidder, self.partner]]

            self.full_hand = FullHand(self.turn, self.bid, self.bidder, self.partner, self.other_team, self.players, self.gameboard)

            self.new_hands()

        print("And the loser is: " + str(self.loser()))


    def bidding(self):
        '''
        Does a round of bidding, highest bid will then choose partners/suit as necessary
        Creates the bid self.bid that will be used for a full hand of play
        '''
        self.bid_winner = self.turn
        self.top_bid = "pass"
        
        for ind in range(4):
            self.player_bid((ind+self.turn) % 4)

        if not self.top_bid == "pass":
            self.bid = Bid(BIDS[self.top_bid], self.top_bid, self.suit)
        else:
            self.turn = (self.turn + 1) % 4
            print("ITS A MISS DEAL!\n")
            self.new_hands()
            self.bidding()
            pass

        if self.top_bid == "frock" or self.top_bid == "wedding":
            self.partner = self.pick_partner(self.bid)
        else:
            self.partner = None

        if self.forced_suit == None:
            if self.top_bid in ["frock","wedding","solo","solo-du"]:
                self.suit = self.pick_suit(self.bid)
        else:
            self.suit = self.forced_suit
        
        self.gameboard.render_all(self.bid_winner, self.bid, self.players)
        
        if not self.top_bid == "pass":
            self.bid = Bid(BIDS[self.top_bid], self.top_bid, self.suit)
        else:
            self.turn = self.turn + 1 % 4
            self.bidding()

    def player_bid(self, turn):
        '''
        Prompts the player to choose a bid with some simple catch logic
        '''
        final_bid = None
        print("\ntop bid is: " + self.top_bid)
        print("player " + self.players[turn].name + "'s turn to bid")
        print("pick a bid out of: " + str(BID_NAMES))

        self.gameboard.render_all(turn, final_bid, self.players)

        while final_bid == None:
            new_bid = input("which bid do you want?")
            if not new_bid in BIDS:
                print("that's not a real bid :/ ")
            elif BIDS[new_bid] > BIDS[self.top_bid]:
                self.top_bid = new_bid
                self.bid_winner = turn
                final_bid = new_bid
            elif new_bid == "pass":
                final_bid = "pass"
            elif self.top_bid == "nolo" and new_bid == "frock":
                self.top_bid = new_bid
                self.bid_winner = turn
                self.forced_suit="clubs"
                final_bid = new_bid
            else:
                print("you need to bid HIGHER than the other players")   

    def pick_suit(self,bid):
        '''
        Prompts the player to choose a suit with some simple catch logic
        TODO Remove unallowed options for suits
        '''
        final_choice = None
        hand = self.players[self.bid_winner].hand
        self.gameboard.render_all(self.bid_winner, bid, self.players)
        print("Suits: " + str(suits))
        while final_choice == None:
            chosen = input("which suit do you want to choose as Trump?")
            if not chosen in suits:
                print("you gotta pick one of the ones on the cards")
            elif not hand.has_suit(chosen):
                print("you don't have that suit")
                # TODO implement wedding stuff
            else:
                final_choice = chosen

        self.fix_queens(final_choice)
        
        return final_choice
    
    def fix_queens(self, suit):
        for player in self.players:
            for card in player.hand.cards:
                if card.rank == "Queen" and (card.suit == "clubs" or card.suit == "spades"):
                    card.suit = suit

    def pick_partner(self,bid):
        '''
        Prompts the player to choose a partner with some simple catch logic
        TODO Remove unallowed options for suits
        '''
        # TODO implement wedding stuff
        final_choice = None
        hand = self.players[self.bid_winner].hand
        self.gameboard.render_all(self.bid_winner, bid, self.players)
        print("Suits: " + str(suits))
        while final_choice == None:
            chosen = input("which ace do you want to choose?")
            if not chosen in suits:
                print("you gotta pick one of the ones on the cards")
            elif hand.has_card(14,chosen):
                print("you have that ace, no good")
                # TODO implement call for kings 
                # TODO implement asking other out players
            elif not hand.has_suit(chosen):
                print("you don't have that suit")
                # TODO implement unknown aces
            else:
                final_choice = chosen
        partner = self.who_has_card(value=14, suit=final_choice, player_list=self.players)
        return partner
    
    def who_has_card(self, value, suit, player_list):
        for player in player_list:
            if player.has_card(value, suit):
                return player
            
        print("This case should never be reached, no player has a given card")
        return 


    def game_over(self):
        outs = 0
        for player in self.players:
            if player.out():
                outs += 1
        return outs >= 3 

    def new_hands(self):
        self.game_deck.shuffle()
        for player in self.players:
            player.new_hand()
            player.sort()
            print(str(player))

    def loser(self):
        if self.game_over():
            for player in self.players:
                if not player.out():
                    return player
        else:
            return None  

game = Game()
game.start()
print(game.player1)
# round = Round(0, bid, game.players)