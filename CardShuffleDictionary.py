import random

#Define the card types and values
FACE = {'ACE': 11, '2': 2, '3': 3, '4':4, '5':5, '6':6, '7':7, '8': 8, 
        '9': 9, '10': 10, 'JACK': 10, 'QUEEN': 10, 'KING':10}

TYPE = ['CLUBS', 'SPADES', 'HEARTS', 'DIAMOND']

#used for the dictionary definition of the cards
def getList(dict1): 
    return list(dict1.keys()) 

def getValues(dict1):
    return list(dict1.values())
"""
This function recieves the key of FACE and concatenates that to the type
of card it is. The value of FACE is then added and turned into a dictionary.
It is shuffled by turning each item into a list item and then turned back
into a dictionary by the dict() function
"""
#shuffles the deck to allow dicitonary values
def shuffledDeck(): 
    #Variables
    shuffledCards = {}
    #gets the faces and turns into list
    key = getList(FACE)
    #gets the weight of the card, turns into list
    value = getValues(FACE)
        
   
    for i in range(0,13): #amount of FACE cards
        for j in TYPE:
            shuffledCards[key[i] + ' of ' + j] = (value[i])

    shuffler = list(shuffledCards.items())
    random.shuffle(shuffler)
    shuffledCards = dict(shuffler)
    return shuffledCards


