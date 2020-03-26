#!/usr/bin/env python
# coding: utf-8

# ## Playing Cards
# A standard deck of playing cards has four suits (Hearts, Diamonds, Spades and Clubs) and thirteen ranks (2 through 10, then the face cards Jack, Queen, King and Ace) for a total of 52 cards per deck. Jacks, Queens and Kings all have a rank of 10. Aces have a rank of either 11 or 1 as needed to reach 21 without busting. As a starting point in your program, you may want to assign variables to store a list of suits, ranks, and then use a dictionary to map ranks to values.

# In[8]:


#final
import random
suits=('hearts','dice','spade','clubs')
ranks=('two','three','four','five','six','seven','eight','nine','jack','queen','king','ace')
points={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'jack':10,'queen':10,'king':10,'ace':11}
playing=True


# **Step 2: Create a Card Class**<br>
# A Card object really only needs two attributes: suit and rank. You might add an attribute for "value" - we chose to handle value later when developing our Hand class.<br>In addition to the Card's \_\_init\_\_ method, consider adding a \_\_str\_\_ method that, when asked to print a Card, returns a string in the form "Two of Hearts"

# In[9]:


#final
class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    def __str__(self):
        return (f"{self.rank} of {self.suit}")


# In[10]:


d=[]
for suit in suits:
    for rank in ranks:
        d.append(Card(suit,rank))  #as we are appending a object  it is just savinf themselves in the memory.
    print(d)


# **Step 3: Create a Deck Class**<br>
# Here we might store 52 card objects in a list that can later be shuffled. First, though, we need to *instantiate* all 52 unique card objects and add them to our list. So long as the Card class definition appears in our code, we can build Card objects inside our Deck \_\_init\_\_ method. Consider iterating over sequences of suits and ranks to build out each card. This might appear inside a Deck class \_\_init\_\_ method:
# 
#     for suit in suits:
#         for rank in ranks:
# 
# In addition to an \_\_init\_\_ method we'll want to add methods to shuffle our deck, and to deal out cards during gameplay.<br><br>
# OPTIONAL: We may never need to print the contents of the deck during gameplay, but having the ability to see the cards inside it may help troubleshoot any problems that occur during development. With this in mind, consider adding a \_\_str\_\_ method to the class definition.

# In[11]:


import random
class Deck:
    def __init__(self):
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    def __str__(self):
        string=''
        for item in self.deck:
            string=string + '**' + '\n' + item.__str__()
        return string
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        last_card=self.deck.pop()
        return last_card


# In[12]:


print(Deck())


# **Step 4: Create a Hand Class**<br>
# In addition to holding Card objects dealt from the Deck, the Hand class may be used to calculate the value of those cards using the values dictionary defined above. It may also need to adjust for the value of Aces when appropriate.

# In[13]:


class Hand:
    def __init__(self):
        self.cards=[]
        self.points=0
        self.aces=0
    def add_card(self,card):
        self.cards.append(card)
        self.points = self.points + points[card.rank]
        if card.rank=='ace':
            self.aces=self.aces+1
    def adjust_for_ace(self):
        while self.points>21 and self.aces:
            self.points=self.points-10
            self.aces=self.aces-1


# **Step 5: Create a Chips Class**<br>
# In addition to decks of cards and hands, we need to keep track of a Player's starting chips, bets, and ongoing winnings. This could be done using global variables, but in the spirit of object oriented programming, let's make a Chips class instead!

# In[14]:


class Chips:
    def __init__(self):
        self.total=110
        self.bet=0
    def win_bet(self):
        self.total=self.total+self.bet
    def losing_bet(self):
        self.total=self.total-self.bet


# **Step 6: Write a function for taking bets**<br>
# Since we're asking the user for an integer value, this would be a good place to use <code>try</code>/<code>except</code>. Remember to check that a Player's bet can be covered by their available chips.

# In[15]:


def take_bet(chips):
    while True:
        try:
            chips.bet=int(input(f'you got {chips.total}. How many chips you would like to bet now? '))
        except:
            print('type only integer value.')
        else:
            if chips.bet>chips.total:
                print('the bet cannot exceed the total chips')
                continue
            else:
                break


# **Step 7: Write a function for taking hits**<br>
# Either player can take hits until they bust. This function will be called during gameplay anytime a Player requests a hit, or a Dealer's hand is less than 17. It should take in Deck and Hand objects as arguments, and deal one card off the deck and add it to the Hand. You may want it to check for aces in the event that a player's hand exceeds 21.

# In[16]:


def taking_hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


# **Step 8: Write a function prompting the Player to Hit or Stand**<br>
# This function should accept the deck and the player's hand as arguments, and assign playing as a global variable.<br>
# If the Player Hits, employ the hit() function above. If the Player Stands, set the playing variable to False - this will control the behavior of a <code>while</code> loop later on in our code.

# In[17]:


def hit_stand(deck,hand):
    global playing
    while True:
        a=input("type 'h' or 's' depending on you want to hit or stand")
        if a[0].lower()=='h':
            taking_hit(deck,hand)
        elif a[0].lower()=='s':
            print('wait for some time! dealer is playing now')
            playing= False
        else:
            print('try again')
            continue
        break


# **Step 9: Write functions to display cards**<br>
# When the game starts, and after each time Player takes a card, the dealer's first card is hidden and all of Player's cards are visible. At the end of the hand all cards are shown, and you may want to show each hand's total value. Write a function for each of these scenarios.

# In[18]:


def show_some(dealer,player):
    print("\n dealer's card")
    print("<card hidden>")
    print('',dealer.cards[1])
    print("\n player's card",*player.cards, sep='\n')
def show_all(dealer,player):
    print("\ndealer's card",*dealer.cards,sep='\n')
    print(" ",dealer.points)
    print("\nplayer's card",*player.cards,sep='\n')
def show_dealer(dealer):
    print("\ndealer's card",*dealer.cards,sep='\n')


# **Step 10: Write functions to handle end of game scenarios**<br>
# Remember to pass player's hand, dealer's hand and chips as needed.

# In[19]:


def player_busts(player,dealer,chips):
    print('\nplayer busts')
    chips.losing_bet()

def player_wins(player,dealer,chips):
    print('\nplayers win')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('\ndealer busts')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('\ndealer wins')
    chips.win_bet()
    
def push(player,dealer):
    print('the game is a tie, it is a push')


# ### And now on to the game!!

# In[20]:


while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    deck=Deck()
    deck.shuffle()
    
    player=Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    
    dealer=Hand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())
    
    chips=Chips()
    take_bet(chips)
    
    show_some(dealer,player)
    
    while playing:
        hit_stand(deck,player)
        show_some(dealer,player)
        if player.points>21:
            player_busts(player,dealer,chips)
            break
    if player.points<=21:
        
        while dealer.points<17:
            taking_hit(deck,dealer)
        if dealer.points>21:
            dealer_busts(player,dealer,chips)
        elif player.points<dealer.points:
            dealer_wins(player,dealer,chips)
        elif player.points>dealer.points:
            player_wins(player,dealer,chips)
        else:
            push(player,dealer)
    print('\n')
    print(f'\n the players total points are: {player.points}')
    print(f'\n the dealers total points are: {dealer.points}')
    show_dealer(dealer)
    print('\n')
    new_game=input("\n type 'yes' or 'no depending on if you would like to play or not?'")
    
    if new_game[0].lower()=='y':
        playing = True
        continue
    else:
        print('\n thanks for palying')
        break


# In[ ]:




