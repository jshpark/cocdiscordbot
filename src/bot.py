import os
import sys
import coc
import json

with open("../config.json") as json_data_file:
    data = json.load(json_data_file)

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD_TEST')
GUILD = os.getenv('DISCORD_GUILD_PROD')

client = discord.Client()

def CheckMessageContent(message):
    messageString = message.content.split(' ')
    if len(messageString) == 1:
        return 0
    else:
        return 1

def GetMessageContent(message):
    messageString = message.content.split(' ')
    return messageString[1]

def GenPlayerInfoN(message):
    if CheckMessageContent(message) == 0:
        return message.channel.send("Enter a player tag")

    playerID = GetMessageContent(message).lower()

    response = ''

    if playerID in data['users'].keys():
        playerID = data['users'][playerID]
    
    response = coc.GetPlayer(playerID)
    return message.channel.send(response)

def GenPlayerInfo(message, userName):
    response = coc.GetPlayer(data['users'][userName])
    return message.channel.send(response)

def GenClanInfo(message):
    if CheckMessageContent(message) == 0:
        response = coc.GetClanInfo('2yj00qlg2')
        return message.channel.send(response)
    else:
        response = coc.GetClanInfo(GetMessageContent(message))
        return message.channel.send(response)

def GenWarInfo(message):
    response = coc.GetWarInfo('2yj00qlg2')
    return message.channel.send(response)

def GenWarLogInfo(message):
    response = coc.GetWarLogInfo('2yj00qlg2')
    return message.channel.send(response)

def GenMVPInfo(message):
    response = coc.GenMVPInfo('2yj00qlg2')
    return message.channel.send(response)

def GenDogsInfo(message):
    response = coc.GenDogsInfo('2yj00qlg2')
    return message.channel.send(response)

def GenLeaders(message):
    response = coc.GenLeader('2yj00qlg2')
    return message.channel.send(response)

def GenCoLeaders(message):
    response = coc.GenCoLeaders('2yj00qlg2')
    return message.channel.send(response)

def GenElder(message):
    response = coc.GenElder('2yj00qlg2')
    return message.channel.send(response)

def GenMember(message):
    response = coc.GenMember('2yj00qlg2')
    return message.channel.send(response)

def GenRoles(message):
    response = coc.GenRoles('2yj00qlg2')
    return message.channel.send(response)

def GenUpgrades(message, userName):
    response = coc.GenUpgrades(data['users'][userName])
    return message.channel.send(response)

def GenUpgradesN(message):
    if CheckMessageContent(message) == 0:
        return message.channel.send("Enter a player tag")

    playerID = GetMessageContent(message).lower()

    response = ''

    if playerID in data['users'].keys():
        playerID = data['users'][playerID]
    
    response = coc.GenUpgrades(playerID)
    return message.channel.send(response)

@client.event
async def on_message(message):
    # searching player
    if '!player' in message.content:
        userName = message.author.name.lower()
        print("Player called: " + userName)
        if userName in data['users'].keys() and CheckMessageContent(message) == 0:
            await GenPlayerInfo(message, userName)
        else:
            await GenPlayerInfoN(message)

    # get clan info
    if '!clan' in message.content:
        await GenClanInfo(message)

    # get current war info
    if '!war' in message.content:
        await GenWarInfo(message)

    # get previous war info
    if '!log' in message.content:
        await GenWarLogInfo(message)

    # get 6 or 5 stars
    if '!mvp' in message.content:
        await GenMVPInfo(message)

    # get none, 0, 1, 2 stars
    if '!dogs' in message.content:
        await GenDogsInfo(message)

    # get list of Leader
    if '!leader' == message.content:
        await GenLeaders(message)

    # get list of coLeader
    if '!coleader' in message.content:
        await GenCoLeaders(message)
    
    # get list of elder
    if '!elder' in message.content:
        await GenElder(message)

    # get list of member
    if '!member' in message.content:
        await GenMember(message)

    # get list of all roles
    if '!role' in message.content:
        await GenRoles(message)

    #get list of upgrades
    if '!upgrade' in message.content:
        userName = message.author.name.lower()
        print("Upgrade called: " + userName)
        if userName in data['users'].keys() and CheckMessageContent(message) == 0:
            await GenUpgrades(message, userName)
        else:
            await GenUpgradesN(message)

client.run(TOKEN)