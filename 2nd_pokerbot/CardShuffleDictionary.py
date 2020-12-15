import random

# Define the card types and values
FACE = {
    "ACE": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "JACK": 10,
    "QUEEN": 10,
    "KING": 10,
}

TYPE = ["Clubs", "Spades", "Hearts", "Diamonds"]


# used for the dictionary definition of the cards
def get_list(dict1):
    return list(dict1.keys())


def get_values(dict1):
    return list(dict1.values())


# shuffles the deck to allow dicitonary values
def shuffled_deck():
    shuffled_cards = {}
    key = get_list(FACE)
    value = get_values(FACE)

    for i in range(0, 13):
        for j in TYPE:
            shuffled_cards[key[i] + " of " + j] = value[i]

    shuffler = list(shuffled_cards.items())
    random.shuffle(shuffler)
    shuffled_cards = dict(shuffler)
    return shuffled_cards
