

import random

class Players:
    def __init__(self, name, money, isDealer, isBetting, nextPlayer, cards, roundBet, isPlaying, winVal):
        self.name = name
        self.money = 10000
        self.isBetting = True
        self.isWinner = False
        self.nextPlayer = None
        self.cards = None
        self.roundBet = 0
        self.isPlaying = False
        self.winVal = 0


class LinkedList:
    def __init__(self):
        self.headval = None


# Circular queue
    # Could not think of or find a better way to implement a singly-linked list in Python
playerList = LinkedList()
p1 = Players(playerName, 10000)
p2 = Players(playerName, 10000)
p3 = Players(playerName, 10000)
p4 = Players(playerName, 10000)
p5 = Players(playerName, 10000)
p6 = Players(playerName, 10000)
p7 = Players(playerName, 10000)
p8 = Players(playerName, 10000)
playerList.headval = p1
p1.nextPlayer = p2
p2.nextPlayer = p3
p3.nextPlayer = p4
p4.nextPlayer = p5
p5.nextPlayer = p6
p6.nextPlayer = p7
p7.nextPlayer = p8
p8.nextPlayer = playerList.headval
tempList = [p1, p2, p3, p4, p5, p6, p7, p8]
tempList[numPlayers-1].nextPlayer = playerList.p1
for i in range(numPlayers):
    tempList[i].isPlaying = True

suits = ['hearts', 'diamonds', 'spades', 'clubs']
values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
faces = {
    'Ace': 14,
    'King': 13,
    'Queen': 12,
    'Jack': 11
}
ante = 10


# Makes a deck of numDecks standard 52-card poker decks
#   Each entry has a cardName as the key, and a list of [cardValue, id] as the dict value
#   id is tracked to know which of the numDecks it originally belonged to
def makeDecks(suit, value, face, numDecks=1):
    deck = {}
    for x in range(numDecks):
        for i in range(len(suit)):
            for key in face:
                cardName = key + ' of ' + suit[i]
                deck[cardName] = [face[key], x+1]

            for j in range(len(value)):
                cardName = str(value[j]) + ' of ' + suit[i]
                deck[cardName] = [value[j], x+1]
    return deck


# Takes decklist as argument and returns the decklist shuffled
def shuffleDeck(decklist):
    shuffler = list(decklist)
    random.shuffle(shuffler)
    newDecklist = dict(shuffler)
    return newDecklist


# Handles looping the linked list to deal each player 2 cards
def deal(pokerDeck, cardIndex):
    for Players in tempList:
        if Players.isPlaying:
            Players.cards[0] = pokerDeck[cardIndex]
            cardIndex = cardIndex + 1
            Players.cards[1] = pokerDeck[cardIndex]
            cardIndex = cardIndex + 1


# Handles betting until all players' round bets = minimumBet
def betting(headPtr):
    minBet = 0
    startPlayer = headPtr.headval.nextPlayer
    readyForFlip = False
    while (not readyForFlip):
        if startPlayer.isBetting:
            callPrice = minBet - startPlayer.roundBet
            print('1) Raise 2) Call {} 3) Fold\nEnter your choice: '.format(callPrice))
            choice = int(input())
            if choice == 1: #Raise
                print("How much would you like to raise? Must be higher than {}:".format(callPrice))
                bet = int(input())
                startPlayer.money = startPlayer.money - bet
                startPlayer.roundBet = startPlayer.roundBet + bet
                if bet > callPrice: minBet = startPlayer.roundBet
            elif choice == 2: #Call
                startPlayer.money = startPlayer.money - callPrice
                startPlayer.roundBet = startPlayer.roundBet + callPrice
            elif choice == 3: #Fold
                headPtr.isBetting = False
            else:
                print("Please enter a valid number")
                continue

            for Players in tempList:
                if Players.isBetting:
                    if Players.roundBet == minBet:
                        readyForFlip = True
                    else:
                        readyForFlip = False
                        break
        headPtr.headval = headPtr.headval.nextPlayer
    clearBets()


# Resets all players roundBets to 0
def clearBets():
    for Players in tempList:
        Players.roundBet = 0


# Checks to see if everyone folded before full river flop
def isOnlyPlayer():
    count = 0
    for Players in tempList:
        if Players.isBetting:
            count = count + 1

    if count == 1:
        return True
    else:
        return False


# Finds and returns the best hand given the players cards and the river
def findBestHand(listofCards, river):
    best = listofCards + river
    return best


# Play a game of Poker
def pokerHand(numPlayers):
    holdEmDecklist = shuffleDeck(makeDecks(suits, values, faces))
    river = []
    cardIndex = 0
    deal(holdEmDecklist, cardIndex)
    pot = 0
    pot = pot + (ante*numPlayers)
    for Players in tempList:
        Players.money = Players.money - ante
    river.append(holdEmDecklist[cardIndex])
    cardIndex = cardIndex+1
    river.append(holdEmDecklist[cardIndex])
    cardIndex = cardIndex + 1
    for i in range(3):
        betting(playerList.headval)
        if isOnlyPlayer():
            for Players in tempList:
                if Players.isBetting:
                    Players.money = Players.money + pot
                    break
        cardIndex = cardIndex+1
        river.append(holdEmDecklist[cardIndex])

    betting(playerList.headval)
    for Players in tempList:
        print("Player {}'s cards: {}".format(Players.name, Players.cards))
    for i in range(len(river)):
        print("The river cards are: {}".format(river))

    for Players in Players.isBetting:
        hand = Players.cards + river
        bestHand = findBestHand(hand)
        if bestHand is royalFlush:
            Players.winVal = 100
        elif bestHand is straightFlush:
            Players.winVal = 99
        elif bestHand is fourofaKind:
            Players.winVal = 98
        elif bestHand is flush:
            Players.winVal = 97
        elif bestHand is straight:
            Players.winVal = 96
        elif bestHand is threeofaKind:
            Players.winVal = 95
        elif bestHand is twoPair:
            Players.winVal = 94
        elif bestHand is pair:
            Players.winVal = 93
        elif bestHand is highCard:
            Players.winVal = 1

    for Players in Players.isBetting:
        highVal = 0
        if Players.winVal > highVal: highVal = Players.winVal
    for Players in Players.isBetting:
        if Players.winVal == highVal: Players.isWinner = True
    for Players in tempList:
        if Players.isWinner == True:
            Players.money = Players.money + pot

    for Players in Players.isPlaying:
        print("Your total profits were: {}".format(Players.money-10000))

