import discord
import asyncio
from PlayerClass import *

client = discord.Client()  # Bot
card_emoji = "\U0001F0CF"

print(pot, player_raised_bet_id, blinds, bet_raised)


@client.event
async def ask_to_play(message):
    msg = await message.channel.send(
        "Who would like to play Texas Hold 'Em Poker?\nPlease respond react within 10 seconds"
    )

    await msg.add_reaction(card_emoji)
    await asyncio.sleep(6)  # Wait for people to react/ Add them to playing list
    await msg.delete()


@client.event
async def options(message):
    msg = await message.channel.send(
        "\nPress 📞 to Call.\nPress 🔼 to Raise.\nPress 🇫 to Fold\n\nYou will automatically fold in 30 seconds\nThere are 5 unknown cards.\n"
    )

    await send_users_tokens_dm(message)

    game_reaction = await message.channel.send("Select your options")
    await game_reaction.add_reaction("📞")
    await game_reaction.add_reaction("🔼")
    await game_reaction.add_reaction("🇫")

    for i in range(
        0, 12
    ):  # Wait for 12 seconds, if someone did not move they automatically fold
        await asyncio.sleep(1)
        if check_for_move():
            break

    remove_timed_out()  # remove timed out players
    await msg.delete()
    await game_reaction.delete()


@client.event
async def on_bet(message):

    global pot
    global bet_raised
    global player_raised_bet_id
    global blinds

    empty_list(blinds)  # if player raised, blind can move
    bet_raised = 0  # reset raise amount

    count = 0
    for i in range(0, 10):  # Wait for ten seconds or until user raised the bet
        if bet_raised:
            break
        else:
            count += 1
            await asyncio.sleep(1)

    if count == 10:  # User timeout - they auto fold - connected with for loop above
        poker_player_dict[player_raised_bet_id].fold()
        fold_msg = await message.channel.send(
            "{} did not raise in time".format(
                poker_player_dict[player_raised_bet_id].user.name
            )
        )
        await asyncio.sleep(3)
        await fold_msg.delete()

    else:  # Bet was raised in time, prompt user to select choice
        print("bet properly raised at 75")
        poker_player_dict[player_raised_bet_id].tokens -= bet_raised
        pot += bet_raised  # Add money to the pt if player raised

        poker_player_dict[
            player_raised_bet_id
        ].bet_flag_on()  # This user has raised and cannot move while waiting for repsonses, move flag is still on
        bet_inc_msg = await message.channel.send(
            "{} raised the bet by {}".format(
                poker_player_dict[player_raised_bet_id].user.name, bet_raised
            )
        )  # send user raised amount

        #
        await send_users_tokens_dm(message)  # Send the tokens of each player

        # ============== Being of Ask For User Input, player_raised_bet_id cannot interact! ==============
        # msg = await message.channel.send(
        #    "Press 📞 to Call.\nPress 🔼 to Raise.\nPress 🇫 to Fold\n\nYou will automatically fold in 30 seconds\nThere are 5 unknown cards."
        # )

        game_reaction = await message.channel.send("Select your options")
        await game_reaction.add_reaction("📞")
        await game_reaction.add_reaction("🔼")
        await game_reaction.add_reaction("🇫")

        for i in range(
            0, 12
        ):  # Wait for 12 seconds, if someone did not move they automatically fold
            await asyncio.sleep(1)
            print("checking for move 97")
            if check_for_move():
                break

        remove_timed_out()  # remove timed out players
        # await msg.delete()
        await game_reaction.delete()

        # =============== End of ask for user input =========================
        await bet_inc_msg.delete()


@client.event
async def on_ready():
    print("Running bot as {0.user}".format(client))


@client.event
async def send_users_cards_dm(message):
    for key in poker_player_dict:  # Send player dm of their hand and tokens
        await poker_player_dict[key].user.send(
            "Your hand in this round: {}\nYour tokens this round: {}".format(
                poker_player_dict[key].hand, poker_player_dict[key].tokens
            )
        )


@client.event
async def send_users_tokens_dm(message):
    for key in poker_player_dict:  # Send player dm of their hand and tokens
        await poker_player_dict[key].user.send(
            "Your tokens this round: {}".format(poker_player_dict[key].tokens)
        )


@client.event
async def send_blinds(message):

    blind_message = await message.channel.send(
        "\n{} is the little blind\n{} is the big blind\n".format(
            poker_player_dict[blinds[0]].user.name,
            poker_player_dict[blinds[1]].user.name,
        )
    )

    poker_player_dict[blinds[1]].is_big_blind()
    poker_player_dict[blinds[0]].is_little_blind()
    await asyncio.sleep(2)
    await blind_message.delete()


@client.event
async def on_reaction_add(reaction, user, tokens=tokens):

    global player_raised_bet_id
    global pot
    global blinds

    if (
        reaction.message.author == client.user  # React must come from bot
        and reaction.message.content  # Must be from initial message
        == "Who would like to play Texas Hold 'Em Poker?\nPlease respond react within 10 seconds"
        and not user.bot  # Ignore bot reacts
    ):
        poker_player_dict[user.id] = Player(tokens=tokens, user=user)
        print("Adding {} to the list".format(user.name))
        print(poker_player_dict)

    elif (
        reaction.message.author == client.user  # Message came from bot
        and (  # Bot must say these messages
            reaction.message.content == "Select your options"
        )
        and not user.bot  # Reaction from bot does not come through
        and user.id in list(poker_player_dict.keys())  # Ensure user is playing
        and not poker_player_dict[user.id].moved_flag  # User has not moved
        and not poker_player_dict[
            user.id
        ].raised_bet_flag  # User cannot raise twice in one round
        and not poker_player_dict[user.id].folded  # User has not folded
        and not poker_player_dict[
            user.id
        ].big_blind  # Big blind does not if beginning of round
    ):
        poker_player_dict[user.id].moved()  # Raise the move flag
        print(poker_player_dict[user.id], " passed at 138")

        if reaction.emoji == "🔼":
            if not a_player_raised():  # Raise the bet
                print("{} raised the bet!".format(user.name))
                player_raised_bet_id = user.id  # You have raised the bet
            elif a_player_raised():
                if poker_player_dict[a_player_raised()].raised_bet_flag:
                    print("{} raised the bet!".format(user.name))
                    player_raised_bet_id = user.id  # You have raised the bet
            else:  # You are marked as move but didn't raise in time
                pass

        elif reaction.emoji == "🇫":
            print("{} folded!".format(user.name))
            poker_player_dict[user.id].fold()

        elif reaction.emoji == "📞":
            print("here 155")
            if poker_player_dict[user.id].little_blind:
                print("{} called!".format(user.name))
                poker_player_dict[user.id].tokens -= 1
                pot += bet_raised
            else:
                print("{} called!".format(user.name))
                poker_player_dict[user.id].tokens -= bet_raised
                pot += bet_raised


@client.event
async def on_message(message):

    global player_raised_bet_id

    # ===============POKER====================
    if message.content.startswith("$Poker"):

        # ========Variables for the game===========

        global bet_raised
        global pot
        global blinds
        deck = list(shuffled_deck())
        community_cards = []

        # ========Initialize players=> Create a player dictionary from user reactions

        await ask_to_play(message)

        # =======Game Start==================

        bet_raised = 2
        pot = 3

        initialize_game(deck, community_cards)
        initialize_cards(
            poker_player_dict, deck, community_cards
        )  # Gives cards to players and the board

        # ===========Game Loop=============
        # Round 1

        pre_flop_msg = "=" * 5 + "\nPre-Flop\n" + "=" * 5
        pre_flop = await message.channel.send(pre_flop_msg)

        blinds = select_blinds(
            poker_player_dict, blinds
        )  # Select Blinds and take tokens

        await send_blinds(message)  # Sends message of who is the blinds and user cards
        await send_users_cards_dm(message)

        await options(message)  # Give options to play, delete once all answered

        set_blinds_off()  # Preperation for next round
        empty_list(blinds)
        print(blinds)

        """
        for key in poker_player_dict:
            if poker_player_dict[key].moved_flag:
                print(poker_player_dict[key].user.id, 'move flag on')
            else:
                print(poker_player_dict[key].user.id, 'move flag off')

        move_flag_off(2)  # Unmove all player to prepare for next round, dont unmove the player who raised the bet

        for key in poker_player_dict:
            if poker_player_dict[key].moved_flag:
                print(poker_player_dict[key].user.id, 'move flag on')
            else:
                print(poker_player_dict[key].user.id, 'move flag off')
        """

        while a_player_raised():  # if a player raised the bet
            bet_msg = await message.channel.send(
                "{}, please enter raise amount.\nYou will be timed out in ten seconds".format(
                    poker_player_dict[player_raised_bet_id].user.name
                )
            )
            await on_bet(message)
            move_flag_off(2)
            await asyncio.sleep(1)
            bet_msg.delete()

        move_flag_off(1)
        player_raised_bet_id = 0

        await pre_flop.delete()
        # =======================Round 2 Start ==================

        flop_msg = "=" * 5 + "\nFlop\n" + "=" * 5
        flop = await message.channel.send(flop_msg)
        shown_cards = "The shown community cards are: \n\n"
        for i in range(0, 3):
            shown_cards = (
                shown_cards + "\n" + str(community_cards[i])
            )  # Print community cards
        shown_cards = shown_cards + "\n"
        community_cards_msg = await message.channel.send(shown_cards)

        blinds = select_blinds(
            poker_player_dict, blinds
        )  # Select Blinds and take tokens
        await send_blinds(message)  # Sends message of who is the blinds and user cards

        await send_users_tokens_dm(message)
        await options(message)  # Give options to play, delete once all answered

        set_blinds_off()  # Preperation for next round
        empty_list(blinds)

        set_blinds_off()  # In case of player bet raised
        blinds.clear()

        while a_player_raised():  # if a player raised the bet
            bet_msg = await message.channel.send(
                "{}, please enter raise amount.\nYou will be timed out in ten seconds".format(
                    poker_player_dict[player_raised_bet_id].user.name
                )
            )
            await on_bet(message)
            move_flag_off(2)
            await asyncio.sleep(1)
            bet_msg.delete()

        move_flag_off(1)
        player_raised_bet_id = 0
        await flop.delete()
        await community_cards_msg.delete()

        # =======================Round 3 Start ===================

        turn_msg = "=" * 5 + "\nTurn\n" + "=" * 5
        turn = await message.channel.send(turn_msg)
        shown_cards = "The shown community cards are: \n\n"
        for i in range(0, 4):
            shown_cards = (
                shown_cards + "\n" + str(community_cards[i])
            )  # Print community cards
        shown_cards = shown_cards + "\n"
        community_cards_msg = await message.channel.send(shown_cards)

        blinds = select_blinds(
            poker_player_dict, blinds
        )  # Select Blinds and take tokens
        await send_blinds(message)  # Sends message of who is the blinds and user cards

        await send_users_tokens_dm(message)
        await options(message)  # Give options to play, delete once all answered

        set_blinds_off()  # Preperation for next round
        empty_list(blinds)

        set_blinds_off()  # In case of player bet raised
        blinds.clear()

        while a_player_raised():  # if a player raised the bet
            bet_msg = await message.channel.send(
                "{}, please enter raise amount.\nYou will be timed out in ten seconds".format(
                    poker_player_dict[player_raised_bet_id].user.name
                )
            )
            await on_bet(message)
            move_flag_off(2)
            await asyncio.sleep(1)
            bet_msg.delete()

        move_flag_off(1)
        player_raised_bet_id = 0

        await turn.delete()
        await community_cards_msg.delete()
        # ======================= River =====================

        river_msg = "=" * 5 + "\nRiver\n" + "=" * 5
        river = await message.channel.send(river_msg)
        shown_cards = "The shown community cards are: \n\n"
        for i in range(0, 5):
            shown_cards = shown_cards + "\n" + str(community_cards[i])
        shown_cards = shown_cards + "\n"  # Print community cards
        community_cards_msg = await message.channel.send(shown_cards)

        blinds = select_blinds(
            poker_player_dict, blinds
        )  # Select Blinds and take tokens
        await send_blinds(message)  # Sends message of who is the blinds and user cards

        await send_users_tokens_dm(message)
        await options(message)  # Give options to play, delete once all answered

        set_blinds_off()  # Preperation for next round
        empty_list(blinds)

        set_blinds_off()  # In case of player bet raised
        blinds.clear()

        while a_player_raised():  # if a player raised the bet
            bet_msg = await message.channel.send(
                "{}, please enter raise amount.\nYou will be timed out in ten seconds".format(
                    poker_player_dict[player_raised_bet_id].user.name
                )
            )
            await on_bet(message)
            move_flag_off(2)
            await asyncio.sleep(1)
            bet_msg.delete()

        move_flag_off(1)
        player_raised_bet_id = 0

        await river.delete()
        await community_cards_msg.delete()

        # =============== Determine Winner ==============

    if (
        message.author.id
        == player_raised_bet_id  # Establish amount came from person who raised bet
        and is_int(message.content)
    ):
        if poker_player_dict[message.author.id].tokens >= int(
            message.content
        ):  # Player must have more tokens than bet

            bet_raised = int(message.content)

        else:
            temp_msg = await message.channel.send(
                "Make sure you have enough money broke boi"
            )
            await asyncio.sleep(1)
            temp_msg.delete()


client.run("Bot_Token_Here")
