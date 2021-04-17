# from urllib.parse import urlparse
import requests
import json
import urllib.parse

with open("../config.json") as json_data_file:
    data = json.load(json_data_file)

my_headers = {"Authorization": "Bearer " + data['apiToken']}

# TODO RETURN ERROR IF PLAYER DOESN'T EXIST
# searching player
def GetPlayer(player):
    url = data['uri'] + "/players/" + urllib.parse.quote("#" + player, safe='')
    response = requests.get(url, headers=my_headers).json()

    name = response['name']
    thLevel = response['townHallLevel']
    league = response['league']['name']
    thTrophies = response['trophies']
    thPeakTrophies = response['bestTrophies']
    attackWins = response['attackWins']
    try:
        role = response['role']
        if role == 'admin':
            role = 'elder'
        donationsGive = response['donations']
        donationsReceive = response['donationsReceived']
        return f'**Name:** {name} \n**TownHall Level:** {thLevel} \n**League:** {league} \n**Trophies:** {thTrophies} \n**Peak Trophies:** {thPeakTrophies} \n**Multiplayer Wins:** {attackWins} \n**Role:** {role.capitalize()} \n**Troops Donated:** {donationsGive} \n**Troops Received:** {donationsReceive}'
    except:
        return f'**Name:** {name} \n**TownHall Level:** {thLevel} \n**League:** {league} \n**Trophies:** {thTrophies} \n**Peak Trophies:** {thPeakTrophies} \n**Multiplayer Wins:** {attackWins} \n**Not In A Clan**'

def GetClanInfo(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='')
    response_one = requests.get(url, headers=my_headers).json()

    clanName = response_one['name']
    clanLevel = response_one['clanLevel']
    teamSize = response_one['members']
    wins = response_one['warWins']
    losses = response_one['warLosses']
    ties = response_one['warTies']
    winStreak = response_one['warWinStreak']

    return f'**Clan Name:** {clanName} \n**Clan Level:** {clanLevel} \n**Member Size:** {teamSize} \n**Wins:** {wins} \n**Losses:** {losses} \n**Ties:** {ties} \n**Win Streak:** {winStreak}'

def GetWarInfo(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='') + "/currentwar"
    response = requests.get(url, headers=my_headers).json()

    if response['state'] is not 'notInWar':
        state = response['state']
        result = ''
        teamSize = response['teamSize']

        name = response['clan']['name']
        clanLevel = response['clan']['clanLevel']
        attacks = response['clan']['attacks']
        stars = response['clan']['stars']
        destPerc = response['clan']['destructionPercentage']

        opponentName = response['opponent']['name']
        opponentClanLevel = response['opponent']['clanLevel']
        opponentAttacks = response['opponent']['attacks']
        opponentStars = response['opponent']['stars']
        opponentDestPerc = response['opponent']['destructionPercentage']

        if state == 'warEnded':
            url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='') + "/warlog"
            response_two = requests.get(url, headers=my_headers).json()
            result = response_two['items'][0]['result']
            return f'**War State:** {state} ({result}) \n**Team Size:** {teamSize} \n \n**Clan Name:** {name} \n**Clan Level:** {clanLevel} \n**Attacks:** {attacks} \n**Stars:** {stars} \n**Destruction %:** {destPerc} + \n \n**Opponent Name:** {opponentName} \n**Opponent Clan Level:** {opponentClanLevel} \n**Opponent Attacks:** {opponentAttacks} \n**Opponent Stars:** {opponentStars} \n**Opponent Destruction %:** {opponentDestPerc}'

        return f'**War State:** {state} \n**Team Size:** {teamSize} \n \n**Attacks:** {attacks} \n**Stars:** {stars} \n**Destruction %:** {destPerc} \n \n**Opponent Name:** {opponentName} \n**Opponent Clan Level:** {opponentClanLevel} \n**Opponent Attacks:** {opponentAttacks} \n**Opponent Stars:** {opponentStars} \n**Opponent Destruction %:** {opponentDestPerc}'

    return f'Clan is not in war'

def GetWarLogInfo(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='') + "/warlog"
    response = requests.get(url, headers=my_headers).json()

    result = response['items'][0]['result']
    teamSize = response['items'][0]['teamSize']

    name = response['items'][0]['clan']['name']
    clanLevel = response['items'][0]['clan']['clanLevel']
    attacks = response['items'][0]['clan']['attacks']
    stars = response['items'][0]['clan']['stars']
    destPerc = response['items'][0]['clan']['destructionPercentage']
    exp = response['items'][0]['clan']['expEarned']

    opponentName = response['items'][0]['opponent']['name']
    opponentClanLevel = response['items'][0]['opponent']['clanLevel']
    opponentStars = response['items'][0]['opponent']['stars']
    opponentDestPerc = response['items'][0]['opponent']['destructionPercentage']

    return f'**Result:** {result} \n**Team Size:** {teamSize} \n \n**Clan Name:** {name} \n**Clan Level:** {clanLevel} \n**Clan Stars:** {stars} \n**Clan Destruction %:** {destPerc} \n**Exp Gained:** {exp} \n \n**Opponent Name:** {opponentName} \n**Opponent Clan Level:** {opponentClanLevel} \n**Opponent Stars:** {opponentStars} \n**Opponent Destruction %:** {opponentDestPerc}'

def GenMVPInfo(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='') + "/currentwar"
    response = requests.get(url, headers=my_headers).json()

    if response['state'] in 'warEnded':
        members = response['clan']['members']
        sixStarList = []
        fiveStarList = []

        for member in members:
            stars = 0
            try:
                for attack in member['attacks']:
                    stars = stars + attack['stars']
            except:
                continue

            if stars == 6:
                sixStarList.append(member['name'])
            if stars == 5:
                fiveStarList.append(member['name'])

        sixStarString = ''
        fiveStarString = ''

        for player in sixStarList:
            sixStarString += player + '\n'

        for player in fiveStarList:
            fiveStarString += player + '\n'

        return f'**__Six Stars__** \n' + sixStarString + f'\n **__Five Stars__** \n' + fiveStarString
    else:
        return f'War has not recently been completed'

def GenDogsInfo(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='') + "/currentwar"
    response = requests.get(url, headers=my_headers).json()

    if response['state'] in 'warEnded':
        members = response['clan']['members']
        zeroStarList = []
        oneStarList = []
        twoStarList = []
        noAttackList = []


        for member in members:
            stars = 0
            try:
                for attack in member['attacks']:
                    stars = stars + attack['stars']
            except:
                noAttackList.append(member['name'])
                continue

            if stars == 0:
                zeroStarList.append(member['name'])
            if stars == 1:
                oneStarList.append(member['name'])
            if stars == 2:
                twoStarList.append(member['name'])

        zeroStarString = ''
        oneStarString = ''
        twoStarString = ''
        noAttackString = ''

        for player in zeroStarList:
            zeroStarString += player + '\n'

        for player in oneStarList:
            oneStarString += player + '\n'

        for player in twoStarList:
            twoStarString += player + '\n'

        for player in noAttackList:
            noAttackString += player + '\n'

        return f'**__No Attacks__** \n' + noAttackString + f'\n**__Zero Star__** \n' + zeroStarString + f'\n**__One Star__** \n' + oneStarString + f'\n**__Two Star__** \n' + twoStarString
    else:
        return f'War has not recently been completed'

def GenLeader(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='')
    response = requests.get(url, headers=my_headers).json()

    memberList = response['memberList']
    leaderList = []

    for member in memberList:
        if member['role'] == 'leader':
            leaderList.append(member['name'])

    leaderString = ''

    for leader in leaderList:
        leaderString += leader + '\n'

    return f'**__Leader__** \n' + leaderString

def GenCoLeaders(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='')
    response = requests.get(url, headers=my_headers).json()

    memberList = response['memberList']
    coleaderList = []

    for member in memberList:
        if member['role'] == 'coLeader':
            coleaderList.append(member['name'])

    coleaderString = ''

    for coleader in coleaderList:
        coleaderString += coleader + '\n'

    return f'**__CoLeaders__** \n' + coleaderString

def GenElder(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='')
    response = requests.get(url, headers=my_headers).json()

    memberList = response['memberList']
    elderList = []

    for member in memberList:
        if member['role'] == 'admin':
            elderList.append(member['name'])

    elderString = ''

    for elder in elderList:
        elderString += elder + '\n'

    return f'**__Elders__** \n' + elderString

def GenMember(clanID):
    url = data['uri'] + "/clans/" + urllib.parse.quote("#" + clanID, safe='')
    response = requests.get(url, headers=my_headers).json()

    memberList = response['memberList']
    memberRegList = []

    for member in memberList:
        if member['role'] == 'member':
            memberRegList.append(member['name'])

    memberString = ''

    for member in memberRegList:
        memberString += member + '\n'

    return f'**__Members__** \n' + memberString

def GenRoles(clanID):
    return GenLeader(clanID) + '\n' + GenCoLeaders(clanID) + '\n' + GenElder(clanID) + '\n' + GenMember(clanID)

def GenUpgrades(player):
    url = data['uri'] + "/players/" + urllib.parse.quote("#" + player, safe='')
    response = requests.get(url, headers=my_headers).json()

    troopList = []
    heroList = []
    spellList = []
    siegeList = []
    siegeName = ["Stone Slammer", "Wall Wrecker", "Battle Blimp", "Siege Barracks", "Log Launcher"]

    thLevel = str(response['townHallLevel'])
    labLevel = str(data['ThToLab'][thLevel])


    for troop in response['troops']:
        if troop['village'] == 'home' and not 'Super' in troop['name'] and not 'Sneaky' in troop['name'] and not 'Inferno' in troop['name'] and not 'Ice Hound' in troop['name']:
            try:
                if troop['name'] in siegeName:
                    siegeList.append('**' + troop['name'] + ': **' + str(troop['level']) + ' / ' + str(data['SiegeUpgrades'][labLevel][troop['name']]))
                else:
                    troopList.append('**' + troop['name'] + ': **' + str(troop['level']) + ' / ' + str(data['upgrades'][labLevel][troop['name']]))
            except:
                troopList.append('**' + troop['name'] + ': **' + str(troop['level']) + ' / ' + "1")

    for hero in response['heroes']:
        if hero['name'] not in 'Battle Machine':
            heroList.append('**' + hero['name'] + ': **' + str(hero['level']) + ' / ' + str(data['HeroUpgrades'][thLevel][hero['name']]))


    for spell in response['spells']:
        try:
            spellList.append('**' + spell['name'] + ': **' + str(spell['level']) + ' / ' + str(data['upgrades'][labLevel][spell['name']]))
        except:
            spellList.append('**' + spell['name'] + ': **' + str(spell['level']) + ' / ' + "1")

    troopString = ''
    heroString = ''
    spellString = ''
    siegeString = ''

    for troop in troopList:
        troopString += troop + '\n'

    for hero in heroList:
        heroString += hero + '\n'

    for spell in spellList:
        spellString += spell + '\n'

    for siege in siegeList:
        siegeString += siege + '\n'

    if siegeString == '':
        return f'**__Max Labratory Level at TH Level {thLevel}: {labLevel}__**' + '\n \n' + f'**__Troops__** \n' + troopString + '\n' + f'**__Heroes__** \n' + heroString + '\n' + f'**__Spells__** \n' + spellString

    return f'**__Max Labratory Level at TH Level {thLevel}: {labLevel}__**' + '\n \n' + f'**__Troops__** \n' + troopString + '\n' + f'**__Heroes__** \n' + heroString + '\n' + f'**__Spells__** \n' + spellString + '\n' + f'**__Siege Machines__** \n' + siegeString
