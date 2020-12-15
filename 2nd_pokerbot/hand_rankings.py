import re
from collections import Counter

determine_type = re.compile(r"Clubs|Spades|Hearts|Diamonds")
determine_face = re.compile(r"ACE|JACK|QUEEN|KING|\d")


def hand_value_determiner(hand_list):
    type = []
    face = []

    amount_of_pairs = 0
    highest_value_pair = 0

    for i in hand_list:
        value = determine_face.search(i)
        type.append(value)

    for j in hand_list:
        cara = determine_type.search(i)
        face.append(j)

    counter = Counter(lst)
    paired_cards = [a for a, b in counter.items() if b > 1]

    while highest_value_pair == 0 and paired_cards != []:  # Determine largest
        for i in paired_cards:
            if i == "ACE":
                highest_value_pair = i
                break
        if highest_value_pair == 0:
            for i in paired_cards:
                if i == "KING":
                    highest_value_pair = i
                    break
        elif highest_value_pair == 0:
            for i in paired_cards:
                if i == "QUEEN":
                    highest_value_pair = i
                    break
        elif highest_value_pair == 0:
            for i in paired_cards:
                if i == "JACK":
                    highest_value_pair = i
                    break
        else:
            for i in paired_cards:
                if highest_value_pair < k:
                    highest_value_pair = i
                else:
                    pass

    amount_of_pairs = len(paired_cards)
