# ===============Imports=====================

from ShuffleCards import *

# ===============Player Classes==============


class Player:  # define a players variables and functions
    def __init__(self):
        self.__cards = {}
        self.points = 0
        self.notLoss = True
        self.stayFlag = False

    def update_points(self):
        self.points = sum(self.__cards.values())
        if self.points > 21:
            self.notLoss = False

    def add_cards(self, deck):
        self.__cards[list(deck.keys())[0]] = list(deck.values())[0]
        # syntax to add new value into dictionary is myDict[key] = value since the items in the dictionaries are
        # indexed by keys, and the keys of deckOfCards are randomly assorted, we convert both keys and values to
        # lists to get the card on the top of the deck and add it to class

        del deck[list(deck.keys())[0]]  # delete the card at the top of the deck
        self.update_points()

    def show_cards(self):
        print("Cards: ", end="")
        for key in self.__cards:
            print(key, end=" | ")
        print("\nPoints: ", self.points, "\n")

    def compare_points(self):
        return self.points


class Dealer(Player):  # define a dealers variables/functions
    def show_first_cards(self):
        print(list(self.__cards.keys())[0])

    def check17(self, deck):
        if self.points >= 17:
            pass
        else:
            self.add_cards(deck)


# =================Card Game Functions===

# players is playerDict, deck is deckOfCards, winList is winnersList


def initialize_cards(players, deck):  # give each player two cards
    for i in range(0, 2):
        for key in players:
            players[key].add_cards(deck)


def show_all_cards(players):  # show the cards of all players
    for key in players:
        players[key].show_cards()


def check_winners(players, win_list):
    for key in players:
        if players[key].points == 21:
            win_list.append(key)


def hit(players, position, deck):
    players[position].add_cards(deck)
    players[position].show_cards()


# =================Play Game==========================================


deckOfCards = shuffled_deck(3)  # deck
winnersList = []  # players who win go in here
n = int(input("How many players will play?\n"))  # Asks the amount of players

# creates an instance of a each player playing a game
dealer = Dealer()
playerDict = {}
for i in range(0, n):
    playerDict[
        "player" + str(i)
    ] = Player()  # result is {'player0': Player()..., 'player[n]': Player()}


# initialize the game
print(deckOfCards, len(deckOfCards))
initialize_cards(playerDict, deckOfCards)
show_all_cards(playerDict)


# Check for winners/
check_winners(playerDict, winnersList)

while not winnersList:  # while winnerList empty, run game of hit and stands function
    for key in playerDict:
        print()
        playerDict[key].show_cards()
        while playerDict[key].notLoss and not playerDict[key].stayFlag:
            print(key, "is playing")
            decision = int(input("Select your decision:\n1) Hit\n2)Stand\n"))
            if decision == 1:
                hit(playerDict, key, deckOfCards)
            if decision == 2:
                playerDict[key].stayFlag = True
    if key == "player" + str(n - 1):  # if last character and no one has 21
        break


if not winnersList:  # check again, if to avoid putting same person 2ice in list
    check_winners(playerDict, winnersList)

if not winnersList:
    mostPoints = 0
    for key in playerDict:
        if not playerDict[key].notLoss:
            pass
        elif playerDict[key].points > mostPoints:
            winnersList.clear()
            mostPoints = playerDict[key].points
            winnersList.append(key)
        elif playerDict[key].points == mostPoints:
            winnersList.append(key)

print("The winner(s):", winnersList)
