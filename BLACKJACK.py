# Mini-project #6 - Blackjack
import math
import simplegui
import random


# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
messages = "Game in progress"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self,player_name):
        self.card_set=[]
        self.value=0
        self.aces_no=0
        self.player_name=player_name
        pass	# replace with your code

    def __str__(self):
        return self.player_name + ":"  + " value=" + str(self.value);
            # replace with your code

    def add_card(self, card):
        self.card_set.append(card);	# replace with your code
        self.value += VALUES[card.get_rank()];
        if(card.get_rank()=="A"):
            self.aces_no+=1;
        if(self.value+10 <= 21 and self.aces_no >0):
            self.value=self.value+10;
        if(self.value>21):
            in_play=False
            decide_winner()
        
    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        return self.value;	# replace with your code

    def busted(self):
        print self.player_name+ " You lose!! Busted";	# replace with your code
    def draw(self, canvas, p):
        sp=list(p);
        padding = CARD_SIZE[0] + 25;
        for cd in self.card_set:
            if(self.player_name=="Dealer" and in_play and sp[0]==p[0]):
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [p[0] + CARD_BACK_CENTER[0], p[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE);
            else:
                cd.draw(canvas,sp)
            sp[0]+=padding
        pass	# replace with your code
 
        
# define deck class
class Deck:
    def __init__(self):
        self.deck=range(0,52)
        # replace with your code

    # add cards back to deck and shuffle
    def shuffle(self):
        self.deck=range(0,52)
        random.shuffle(self.deck)
        pass	# replace with your code

    def deal_card(self):
        num=self.deck.pop(0)
        c=Card(SUITS[math.floor(num/13)],RANKS[num%13])	# replace with your code
        return c

#define event handlers for buttons
def decide_winner():
    
    global score,in_play,messages
    in_play=False
    if(dealer.get_value()>21):
        dealer.busted()
        messages = "Player wins! Well done"
        score+=1
    elif player.get_value()>21:
        messages = "Dealer wins"
        player.busted()
        score-=1
    elif(dealer.get_value()<player.get_value()):
        score+=1
        print "Player wins"
        messages = "Player wins! Well done"
    else:
        score-=1
        print "Dealer wins"
        messages = "Dealer wins"
    print str(player);
    print str(dealer);
    print "\n"
        
        
def deal():
    global outcome, in_play, score,player,dealer,messages
    messages = "Game in progress"
    deck.shuffle();
    player=Hand("Player")
    dealer=Hand("Dealer")
    dealer.add_card(deck.deal_card())
    hit()
    dealer.add_card(deck.deal_card())
    hit()
    if(in_play):
        score=-1
    in_play = True

def hit():
    # replace with your code below
    player.add_card(deck.deal_card());
    # if the hand is in play, hit the player
   
    # if busted, assign an message to outcome, update in_play and score
       
def stand():
    
    while(dealer.get_value() < 17):
        dealer.add_card(deck.deal_card());  
    if(in_play):
        decide_winner()
   
# if hand is in play, repeatedly hit dealer until his hand has value 17 or more

# assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global messages
    canvas.draw_text("Blackjack",[50,100],50,"Black");
    canvas.draw_text("Score "+str(score),[400,100],40,"Blue");
    dealer.draw(canvas,[30,200]);
    if in_play:
        message="Do you want to Hit or Stand?"
    else:
        message="Want to make New Deal?"
    canvas.draw_text(message,[30,350],30,"Orange")
    player.draw(canvas,[30,400])    
    canvas.draw_text("Player",[30,550],30,"Yellow")
    canvas.draw_text("Dealer",[30,180],30,"Yellow")
    canvas.draw_text(messages,[400,200],40,"Brown")

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()

deck=Deck()
player=Hand("Player")
dealer=Hand("Dealer")
deal()

