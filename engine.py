import pygame
import vis_assets
import game
import visualization
# Your game setup would go here
gameScreen = pygame.display.set_mode((1500,1000))
pygame.display.set_caption('SOLO')
pygame.init()
running = True
started = False
Begin_button = vis_assets.Button('Begin!', 1500/2, 1000/2, 200, 100, returner=True)
card_ex_img = pygame.image.load('card_pics/' + "Jack" + '_of_' + "spades" + '.png')
Card_ex = vis_assets.Card(card_ex_img, 400, 500)
Game = game.Game()
bid_ex = vis_assets.Bids(high_bid=4, x=50, y=100, n_in_row=4)


playing = False
round_ended = False
bidding = False

have_bid = 0

# hand_draw = vis_assets.Hand(cards_ex, 200, 900)


while running:

    gameScreen.fill((255, 255, 255))

    # DRAWING #
    if Game.state == "Menu":
        Begin_button.draw(gameScreen)
    else:
        Hand.draw(gameScreen)

    if Game.state == "Bidding":
        bid_ex.draw(gameScreen)
        bid_ex.update()
    
    if Game.state == "Pick Trump":
        trump_pick.draw(gameScreen)
        trump_pick.update()

    # FUNCTIONALITY #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if Begin_button.handle_event(event) is not None or round_ended:
            Game.state = "Bidding"
            Hand = vis_assets.Hand(Game.players[Game.turn].hand.cards, 200, 900)
        # if Game.state is not "Menu":
        #     Hand = vis_assets.Hand(Game.players[Game.turn].hand.cards, 200, 900)
        if Game.state == "Bidding":
            bid = bid_ex.handle_event(event)
    
    # BIDDING LOGIC #
        if Game.state == "Bidding" and bid is not None:
            if bid != 0:
                Game.top_bid = bid
                Game.bid_winner = ((Game.turn + have_bid) % 4)
            have_bid += 1
            Hand = vis_assets.Hand(Game.players[(Game.bid_winner + have_bid) % 4].hand.cards, 200, 900)

            if have_bid >= 4:
                bidding = False          
                if Game.top_bid in [2,4,5,26]:
                    Hand = vis_assets.Hand(Game.players[Game.bid_winner].hand.cards, 200, 900)
                    Game.state = "Pick Trump"
                else:
                    Game.state = "Playing"

    # TRUMP PICKING LOGIC #
        if Game.state is "Pick Trump":
            trump_pick = vis_assets.Trump_suits(Game.players[Game.bid_winner].hand.cards)
            trump_pick.handle_event(event)







    pygame.display.flip()

pygame.quit()