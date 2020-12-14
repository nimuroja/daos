import discord
from CardShuffleDictionary import shuffledDeck, getValues, getList
import test

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$test'):
        await message.channel.send(test)

    if message.content.startswith('$help'):
        x = 'Printing the list of all available commands.'
        await message.channel.send(test)
    
    if message.content.startswith('$cardshuffle'):
        x = shuffledDeck()
        await message.channel.send(x)

    if message.content.startswith('$poker'):
        x = 'Starting a poker game!'
        await message.channel.send(x)

    if message.content.startswith('$blackjack'):
        x = 'Starting a blackjack game!'
        await message.channel.send(x)

    if message.content.startswith('$music'):
        x = 'Preparing youtube playback to your voice channel!'
        await message.channel.send(x)

    if message.content.startswith('$cashout'):
        x = 'Cashing out of this game... Your total winnings were: '
        await message.channel.send(x)

    if message.content.startswith('$overview'):
        x = 'Displaying an overview of the winnings of the last game...'
        await message.channel.send(x)

client.run('Bot_Token')
