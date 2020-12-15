from random import randint

from CardShuffleDictionary import *

temp_list = []
blinds = []

tokens = 300
bet_raised = 2
pot = 3
player_raised_bet_id = 0

poker_player_dict = {}



class Player:
    def __init__(self, user, tokens):
        self.user = user
        self.tokens = tokens
        self.hand = []
        self.complete_hand = []
        self.folded = False
        self.moved_flag = False
        self.raised_bet_flag = False
        self.big_blind = False
        self.little_blind = False
        self.hand_value = 0

    def is_little_blind(self):
        self.little_blind = True

    def is_not_little_blind(self):
        self.little_blind = False

    def is_big_blind(self):
        self.big_blind = True
        self.moved_flag = True

    def is_not_big_blind(self):
        self.big_blind = False

    def init_hand(self, cards):
        for i in range(0, 2):
            self.hand.append(cards[i])
            cards.remove(cards[i])

    def moved(self):
        self.moved_flag = True

    def unmove(self):
        self.moved_flag = False

    def bet_flag_on(self):
        self.raised_bet_flag = True

    def bet_flag_off(self):
        self.raised_bet_flag = False

    def fold(self):
        self.folded = True
        print(self.user.name, 'folded')

    def complete_hand_list(self, community_cards):
        self.complete_hand = Union(community_cards, self.hand)


def Union(lst1, lst2):
    final_list = lst1 + lst2
    return final_list


def move_flag_off(option): # 1: All players are unmoved 2: All players except for raised flag ummoved
    global player_raised_bet_id
    if option == 1:
        for key in poker_player_dict:
            poker_player_dict[key].unmove()

    elif option == 2:
        for key in poker_player_dict:
            if poker_player_dict[key].user.id == player_raised_bet_id:
                print('player has moved and is on bet')
                poker_player_dict[key].move()
            else:
                print('bet raised id is ', player_raised_bet_id)
                print(poker_player_dict[key].user.name, 'is unmoved')
                poker_player_dict[key].unmove()


def is_int(content): #is an int and greater than 0
    while True:
        try:
            if int(content) > 0:
                return True
            else:
                return False
        except ValueError:
            return False


def empty_list(player_list):
    player_list.clear()

def empty_blinds(list):
    global blinds
    blinds.clear()


def initialize_game(cards, unknown):
    for i in range(0, 5):
        unknown.append(cards[i])
        cards.remove(cards[i])


def initialize_cards(players_dict, cards, community):  # give each player two cards, complete list of cards
    for key in players_dict:
        players_dict[key].init_hand(cards)
    for key in players_dict:
        players_dict[key].complete_hand_list(community)


def remove_timed_out():
    for key in poker_player_dict:
        if not poker_player_dict[key].moved_flag:  # fold player if he did not move in time
            poker_player_dict[key].fold()


def check_for_move():  # Check if everyone has moved, loops every second until finished
    try:
        players_moved = 0
        for key in poker_player_dict:
            if poker_player_dict[key].moved_flag == False:  # if player has not moved)
                break
            else:  # if player has moved
                print(poker_player_dict[key].user.name, 'player has moved, 111')
                players_moved += 1
        if players_moved == len(poker_player_dict):  # check if players have moved
            return True
    except UnboundLocalError:
        print('unbound local error')


def select_blinds(players_dict: dict, blind_list: list):
    # return blinds as list of user id
    key = randint(0, len(players_dict) - 1)
    random_player = list(players_dict.keys())[key]
    players_dict[random_player].tokens -= 1  # little blind
    blind_list.append(players_dict[random_player].user.id)

    if (
        key == len(players_dict) - 1
    ):  # if little blind was end of list, come to top of list

        random_player = list(players_dict.keys())[0]
        players_dict[random_player].tokens -= 2
        blind_list.append(players_dict[random_player].user.id)

    else:  # little blind not top of the list

        random_player = list(players_dict.keys())[key + 1]
        players_dict[random_player].tokens -= 2
        blind_list.append(players_dict[random_player].user.id)

    return blind_list  # return the list of blinds that round


def set_blinds_off():
    for key in poker_player_dict:
        poker_player_dict[key].is_not_big_blind()
        poker_player_dict[key].is_not_little_blind()


def a_player_raised():
    count = 0
    for key in poker_player_dict:
        if poker_player_dict[key].user.id == player_raised_bet_id:
            print(player_raised_bet_id, 'is the player id')
            return player_raised_bet_id
            break
        count += 1
    if count == len(poker_player_dict):
        return 0

