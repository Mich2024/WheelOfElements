import os
import re
from CardDefinitions_WheelOfFate import *
import copy

maxRankToPrint = 8
flagPrintHardAI = False

def removeLinebreaks(lines):
    res = []
    for line in lines:
        res.append(line.replace("\n",""))
    return res

def removeDoubleQuotes(lines):
    res = []
    for line in lines:
        res.append(line.replace('"',""))
    return res

def removeComments(lines):
    res = []
    for line in lines:
        if not line[0] == "#":
            res.append(line)
    return res

def removeEmptyLines(lines):
    res = []
    for line in lines:
        spacelessLine = removeSpaces(line)
        if not spacelessLine == "":
            res.append(line)
    return res

def addSpacesAfterText(lines):
    res = []
    for line in lines:
        res.append(line.replace('Text:"', 'Text: "'))
    return res

def addSpacesBetweenEmptyText(lines):
    res = []
    for line in lines:
        res.append(line.replace('""', '" "'))
    return res

def removeTrailingSpaces(lines):
    res = []
    for line in lines:
        strippedLine = line.strip()
        res.append(strippedLine)
    return res

def removeMonAIAnnotation(lines):
    res = []
    for line in lines:
        spacelessLine = removeSpaces(line)
        if spacelessLine != "StatsNormal" and spacelessLine != "StatsElite":
            res.append(line)
    return res


def removeSpaces(str):
    return str.replace(" ", "")



def truncateFile(lines):
    res = []
    for line in lines:
        if line == "End Of File":
            return res
        else:
            res.append(line)
    return res

def startsWith(line, word):
    res = False
    if(len(line) > len(word)):
        if line[:len(word)] == word:
            res = True
    return res

# input -> list of words
# returns -> tuple of ("Text as one string", ["list","with","rest","of","words"])
def parseTextFromWords(words: list):
    text = ""
    #print(words)
    quotationMarks = 0
    i = 0
    #print(i)
    while quotationMarks < 2:
        #print(words[i])
        #print(len(words[i].split(r'"')) - 1)
        quotationMarks += len(words[i].split(r'"')) - 1 #effectively counts the number of quotation marks in string
        #print(words[i])
        tmp = words[i].split(r'"')
        if (tmp[0] == ""):
            tmp = tmp[1:]
        text += " " + tmp[0]
        i += 1
    text = text[1:] #remove leading space
    words = words[i:] #remove entries that we just parsed

    return (text, words)


#returns a dict with variants, types, modifiers, 
def sliceClassToCardTypes(lines):

    CardsBegin = lines.index("Tier1")
    return (lines[:CardsBegin],lines[CardsBegin:])

def sliceStatsToCards(lines):
    
    #print(lines)
    passiveBegin = lines.index("Passive")        
    typeBegin = lines.index("Type")
    

    if("Modifier Tableau" not in lines):
        semantics = {passiveBegin:"Passive", typeBegin:"Type"}
        order = [passiveBegin,typeBegin]
    else: #Race
        tableauBegin = lines.index("Modifier Tableau")
        semantics = {passiveBegin:"Passive", tableauBegin:"Modifier Tableau",typeBegin:"Type"}
        order = [passiveBegin, tableauBegin, typeBegin]

    
    order.sort()
    #print(order)
    #print(semantics)

    res = {}

    for key, value in semantics.items():
        startIndex = order.index(key)
        start = order[startIndex]
        if startIndex == (len(order)-1): #if we have found the last entry, take everything left
            end = len(lines)
        else:
            end = order[startIndex+1]

        res[value] = lines[start+1:end:]


    #print(res)

    return res

#returns an entire action card, without associated level
def parseActionCardFromLine(line, nameClass, rank, tier):

    #Name: "Guarded Punch" ManaCost:Opt;Earth;2 S:1 Text: "--- Opt cost paid ---" S:X Text: "X is equal to your shield" Type:Special


    actCard = actionCard()
    actCard.classname = nameClass
    actCard.rank = rank
    actCard.tier = tier
    
    words = line.split(" ")
    words = [i for i in words if i != ""]  #remove leftovers from double spaces

    #print(words[0])
    if(words[0] == "Name:"): #stores name and deletes entries from words
        name, words = parseTextFromWords(words[1:])
        #print(name)
        actCard.cardName = name

    else:
        print("Error parsing cardName")

    while len(words) > 0:
        if not words[0] == "Text:":
            #print(words)
            parts = words[0].split(":")
            actCard.assignmentDict[parts[0]](actCard,words[0])
            words = words[1:] #remove entry that we just parsed

        else: #Text comes here and needs special treatment
            parts = words[0].split(":")
            text, words = parseTextFromWords(words[1:])
            actCard.assignmentDict[parts[0]](actCard,text)
            

    return actCard        

def parseTableauFromLines(linesTableau):
    res = tableauRace()
    res.L1R1=linesTableau[1]
    res.L1R2=linesTableau[2]
    res.L1R3=linesTableau[3]
    res.L1R4=linesTableau[4]

    res.L2R1=linesTableau[6]
    res.L2R2=linesTableau[7]

    res.L3R1=linesTableau[9]

    return res


# input: all lines before cards 
# output: cards
def parseStatLinesToCards(lines, name, rank):

    res = []

    parts = sliceStatsToCards(lines)
    linesTableau = []
    passive = parts["Passive"] # we are dropping variant 2
    if("Modifier Tableau" in parts.keys()): #Race
        #print(linesTableau)
        linesTableau = parts["Modifier Tableau"]

    TypeExplanation = parts["Type"]
    elements = []
    explanations = []
    #print(linesTableau)

    for line in TypeExplanation:
        #print(line)
        if startsWith(line, "Element"):
            elements.append(line)
        if startsWith(line, "Explanation"):
            explanations.append(line)

    
    
    card = statCard()
    card.explanations = explanations
    card.name = name
    card.rank = rank
    card.elements = elements

    mode = ""
    #print(passive)
    for line in passive:
        if startsWith(line, "Life:") or startsWith(line, "TierCards:") or startsWith(line, "TierPassive:") or startsWith(line, "TierMods:"):
            card.assignmentDict[line.split(":")[0]](card,line.split(":")[1])
            continue
        else:
            #print(line)
            card.passive += line + " "
    if (linesTableau != []):
        card.tableau = parseTableauFromLines(linesTableau)
        #print(card.tableau.L1R1)

    res.append(copy.deepcopy(card))
    return res

'''
def parseRaceLinesToCards(lines, name, rank):

    res = []

    parts = sliceStatsToCards(lines)
    Var1 = parts["Variant:1"]
    linesTableau = []
    linesTableau = parts["Modifier Tableau"]

    TypeExplanation = parts["Type"]
    elements = []
    explanations = []
    #print(linesTableau)

    for line in TypeExplanation:
        #print(line)
        if startsWith(line, "Element"):
            elements.append(line)
        if startsWith(line, "Explanation"):
            explanations.append(line)

    
    card = statCard()
    card.explanations = explanations
    card.name = name
    card.rank = rank
    card.elements = elements

    mode = ""
    for line in Var1:
        if line == "Passive":
            mode = "Passive"
            continue
        if startsWith(line, "Life:"):
            card.assignmentDict[line.split(":")[0]](card,line.split(":")[1])
            continue

        if mode == "Passive":
            card.passive += line + " "
    card.tableau = parseTableauFromLines(linesTableau)

    res.append(copy.deepcopy(card))
    return res'''




#returns and array of arrays, each secondary  arrays represent one monster
def sliceToEnemies(linesInput):
    indexes = []
    res = []
    for i, line in enumerate(linesInput):
        line = linesInput[i]
        if line[0:5] == "Name:":
            indexes.append(i)
    indexes.append(len(linesInput)) #add an end
    #print(indexes)
    for i in range(len(indexes)-1):
        res.append(linesInput[indexes[i]:indexes[i+1]])
        
    #print(res)
    print("monsterAIs read")
    return res

#returns a dict with Normal, Hard
def sliceMonsterToSemantics(lines):
    #print(lines)
    #print(lines)
    Normal = lines.index("Normal")
    Hard = lines.index("Hard")

    semantics = {Normal:"Normal", Hard:"Hard"}
    order = [Normal,Hard]
    
    order.sort()

    res = {}

    #print(semantics)
    #print(order)
    #print(len(lines))

    for key, value in semantics.items():
        startIndex = order.index(key)
        start = order[startIndex]
        #print(startIndex)
        #print(len(order))
        if startIndex == (len(order)-1): #if we have found the last entry, take everything left
            end = len(lines)
        else:
            end = order[startIndex+1]

        res[value] = lines[start+1:end:]

    return res



def parseMonsterAI():
    monsterAICards = []
    pathToMonsterAI = "../MonsterAI.txt"
    print("handling file: " + pathToMonsterAI )

    #open and sanitize file
    fileToParse = open(pathToMonsterAI,"r")
    lines = fileToParse.readlines()
    fileToParse.close()
    lines = removeComments(lines)
    lines = removeLinebreaks(lines)
    lines = removeEmptyLines(lines)
    lines = removeTrailingSpaces(lines)
    lines = truncateFile(lines)
    lines = addSpacesAfterText(lines)
    
    #print(lines)
    print("completed sanitization")

    lines = sliceToEnemies(lines)
    #print(lines)
    for linesMonster in lines:
        sectionsMonster = sliceMonsterToSemantics(linesMonster) #returns a dict with Stats Normal, Stats Elite, Normal AI, Hard AI

        #print(linesMonster)
        

        for key, lines in sectionsMonster.items():
            monCard = monsterAICard()
            monCard.setName(linesMonster[0].split(":")[1])
            if(key == "Normal"):
                monCard.setHardmode(False)
            if(key == "Hard"):
                monCard.setHardmode(True)
        
            for line in lines:
                if(startsWith(line,"Life")):
                    monCard.life = line.split(":")[1]
                if(startsWith(line,"Count")):
                    monCard.count = int(line.split(":")[1])
                if(startsWith(line,"Passive")):
                    monCard.passive = line.split(":")[1]

                if(startsWith(line,"Rolls")):
                    words = line.split(" ")
                    words = [i for i in words if i != ""]  #remove leftovers from double spaces
                    assignmentFunction = monCard.assignmentDict[words[0].split(":")[0]]
                    while len(words) > 0:
                        if not words[0] == "Text:":
                            #print(words)
                            assignmentFunction(monCard,words[0])
                            words = words[1:] #remove entry that we just parsed

                        else: #Text comes here and needs special treatment
                            text, words = parseTextFromWords(words[1:])
                            assignmentFunction(monCard, ["Text: ", text])

                '''
                            for words in linesAI:
                words = words.split(" ")
                #print(words[0].split(":")[0])
                assignmentFunction = card.assignmentDict[words[0].split(":")[0]]
                while len(words) > 0:
                    
                    if not words[0] == "Text:":
                        #print(words)
                        assignmentFunction(card,words[0])
                        words = words[1:] #remove entry that we just parsed
                    else: #Text comes here and needs special treatment
                        #print(words)
                        quotationMarks = 0
                        i = 1
                        result = ""
                        #print(i)
                        while quotationMarks < 2:
                            if '"' in words[i]:
                                quotationMarks += 1
                            #print(words[i])
                            tmp = words[i].split(r'"')
                            if (tmp[0] == ""):
                                tmp = tmp[1:]
                            result += " " + tmp[0]
                            i += 1
                        #result = removeDoubleQuotes(result)
                        assignmentFunction(card, ["Text: ", result])
                        words = words[i:] #remove entries that we just parsed'''
            

            #parseTextFromWords
            monsterAICards.append(copy.deepcopy(monCard))

            

    print("completed parsing MonsterAI")
    
    texMonAI = ""
    #print(len(monsterAICards))
    for monsterAIcard in monsterAICards:
        #print(monsterAIcard.name)
        flagCardHardAI = monsterAIcard.flagHardMode
        if(flagCardHardAI == True and flagPrintHardAI == False):
            continue
        texMonAI += monsterAIcard.serializeToLatex()

    fileToPrint = open('toPrintMonAI.tex', 'w+')
    fileToPrint.write(texMonAI)

    print("wrote AI file")

def parseItems():
    itemCards = []
    pathToItems = "../Items.txt"
    print("handling file: " + pathToItems )

    #open and sanitize file
    fileToParse = open(pathToItems,"r")
    lines = fileToParse.readlines()
    fileToParse.close()
    lines = removeComments(lines)
    lines = removeLinebreaks(lines)
    lines = removeEmptyLines(lines)
    lines = removeTrailingSpaces(lines)
    #lines = removeMonAIAnnotation(lines) used now
    lines = truncateFile(lines)
    
    #print(lines)
    print("completed sanitization")

    #lines = sliceToShopLevels(lines)
    #print(lines)
    shopLevelCurrent = "Level parsing did not work"
    for lineItem in lines:

        

        if(lineItem[0:9] == "ShopLevel"):
            #print(lineItem[10:])
            shopLevelCurrent = lineItem[10:]
        else:
            
            itemCard  = ItemCard()
            itemCard.setLevel(shopLevelCurrent)

            
            
            words = lineItem.split(" ")
            #print(words[0].split(":")[0])

            if(words[0] == "Name:"): #stores name and deletes entries from words
                nameWordcount = 1
                for word in words[1:]:
                    if not ":" in word:
                        itemCard.name += word
                        itemCard.name += " " 
                        nameWordcount += 1
                    else:
                        itemCard.name = itemCard.name[0:]
                        words = words[nameWordcount:]
                        break
            else:
                print("Error parsing item name")

            while len(words) > 0:
                
                if not words[0] == "Text:":
                    #print(words)
                    #print(words)
                    itemCard.assignmentDict[words[0].split(":")[0]](itemCard,words[0])
                    words = words[1:] #remove entry that we just parsed
                else: #Text comes here and needs special treatment
                    #print(words)
                    quotationMarks = 0
                    i = 1
                    result = ""
                    #print(i)
                    while quotationMarks < 2:
                        if '"' in words[i]:
                            quotationMarks += 1
                        #print(words[i])
                        tmp = words[i].split(r'"')
                        if (tmp[0] == ""):
                            tmp = tmp[1:]
                        result += " " + tmp[0]
                        i += 1
                    #result = removeDoubleQuotes(result)
                    itemCard.setText(result)
                    words = words[i:] #remove entries that we just parsed

                  
            itemCards.append(itemCard)

    print("completed parsing Items")
    
    texItems = ""
    #print(len(monsterAICards))
    for itemCard in itemCards:
        #print(itemCard.name)
        texItems += itemCard.serializeToLatex()

    fileToPrint = open('toPrintItems.tex', 'w+')
    fileToPrint.write(texItems)

    print("wrote Item file")


def parseRacesAndClasses(files_Input):

    #card lists. should contain classes from card.py
    modifierCards = []
    actionCards = []
    statusCards = []


    for filelong in files_Input:
        print("handling file: " + filelong )
        file = filelong.split("/")[2] # Drops the prefix from the card
        if("Classes" in filelong):
            rank = int(file.split(".")[0][-1]) # classes have tier 1 to 3
            name = file.split(".")[0]
            name = name[:-1] #drop rank
        else:
            rank = 0 #signifies race
            name = file.split(".")[0]

        if rank > maxRankToPrint:
            continue

        #open and sanitize file
        fileToParse = open(filelong,"r")
        lines = fileToParse.readlines()
        fileToParse.close()
        lines = removeComments(lines)
        lines = removeLinebreaks(lines)
        lines = removeEmptyLines(lines)
        lines = truncateFile(lines)
        lines = addSpacesAfterText(lines)
        print("completed sanitization")

        linesStats, linesActions = sliceClassToCardTypes(lines)

        
        
        statusCards.extend(parseStatLinesToCards(linesStats, name, rank))
        if(rank) == 1:
            statusCards.extend(parseStatLinesToCards(linesStats, name, rank))
        tier = "1"
        for line in linesActions: #######################################
            if startsWith(line, "Tier"):
                tier = line[4]
            else:
                
            #def parseActionCardFromLine(line, nameClass, rank, tier):
                newActCard = parseActionCardFromLine(line, name, rank, tier)
                
                actionCards.append(copy.deepcopy(newActCard))
                if rank == 1:
                    actionCards.append(copy.deepcopy(newActCard))

        print("parsed action cards")
        

    print("completed parsing")

    nandeckStatCards = ""
    nandeckRaces = ""
    orderRaces = 1
    orderClasses = 1

    for i, statusCard in enumerate(statusCards):
        #print(statusCard.name)
        if statusCard.tableau == None:

            nandeckStatCards += statusCard.serializeToNandeck(orderClasses)
            orderClasses += 1
        else:
            #print(statusCard.tableau.L1R1)
            nandeckRaces += statusCard.serializeToNandeck(orderRaces)
            orderRaces += 1


    texModCards = ""
    #for modCard in modifierCards:
    #    texModCards += modCard.serializeToLatex()

    orderActions = 1
    nandeckActCards = ""
    for actCard in actionCards:
        nandeckActCards += actCard.serializeToNandeck(orderActions) 
        orderActions += 1

        

    template_boilerplate_classes = open('Templates/Shingle_Class_Boilerplate.txt', 'r')
    template_boilerplate_classes = template_boilerplate_classes.read()
    template_boilerplate_classes = template_boilerplate_classes.replace(r"${Classes}", nandeckStatCards).replace(r"${CardCount}", str(orderClasses-1))


    fileToPrint = open('out/classShingles.txt', 'w+')
    fileToPrint.write(template_boilerplate_classes)
    fileToPrint.close()

    template_boilerplate_actions = open('Templates/Action_Boilerplate.txt', 'r')
    template_boilerplate_actions = template_boilerplate_actions.read()
    template_boilerplate_actions = template_boilerplate_actions.replace(r"${Cards}", nandeckActCards).replace(r"${CardCount}", str(orderActions-1))

    fileToPrint = open('out/ActCards.txt', 'w+')
    fileToPrint.write(template_boilerplate_actions)
    fileToPrint.close()
    
    template_boilerplate_races = open('Templates/Tableau_Boilerplate.txt', 'r')
    template_boilerplate_races = template_boilerplate_races.read()

    template_boilerplate_races = template_boilerplate_races.replace(r"${Races}", nandeckRaces).replace(r"${CardCount}",str(orderRaces-1))

    fileToPrint = open('out/raceTableaus.txt', 'w+')
    fileToPrint.write(template_boilerplate_races)
    fileToPrint.close()

    print("wrote file")


    #outCards = open("RacesClasses.tex","w")
    #outModifiers = open("RacesClasses.tex","w")


if __name__ == "__main__":
    ### INPUT OF PROPER RACES AND CLASSES
    files_Input = []    

    files_Input.append(r"../Races/Centaur.txt")
    #files_Input.append(r"../Races/Dragonblood.txt")
    #files_Input.append(r"../Races/Dwarf.txt")
    #files_Input.append(r"../Races/Elf.txt")

    #files_Input.append(r"../Races/Fae.txt")
    files_Input.append(r"../Races/Halfelf.txt")
    files_Input.append(r"../Races/Human.txt")
    #files_Input.append(r"../Races/Merman.txt")
    #files_Input.append(r"../Races/Silverkin.txt")
    files_Input.append(r"../Races/Solarian.txt")
    files_Input.append(r"../Races/Thyger.txt")
    files_Input.append(r"../Races/Wyrmkin.txt")
    
    files_Input.append(r"../Classes/Toxicologist1.txt")
    files_Input.append(r"../Classes/Toxicologist2.txt")
    files_Input.append(r"../Classes/Toxicologist3.txt")

    files_Input.append(r"../Classes/Assassin1.txt")
    files_Input.append(r"../Classes/Assassin2.txt")
    files_Input.append(r"../Classes/Assassin3.txt")

    files_Input.append(r"../Classes/Berserker1.txt")
    files_Input.append(r"../Classes/Berserker2.txt")
    files_Input.append(r"../Classes/Berserker3.txt")

    files_Input.append(r"../Classes/Druid1.txt")
    files_Input.append(r"../Classes/Druid2.txt")
    files_Input.append(r"../Classes/Druid3.txt")

    files_Input.append(r"../Classes/DrunkenMaster1.txt")
    files_Input.append(r"../Classes/DrunkenMaster2.txt")
    files_Input.append(r"../Classes/DrunkenMaster3.txt")
    
    #files_Input.append(r"../Classes/Guerilla1.txt")
    #files_Input.append(r"../Classes/Guerilla2.txt")
    #files_Input.append(r"../Classes/Guerilla3.txt")

    files_Input.append(r"../Classes/Knight1.txt")
    files_Input.append(r"../Classes/Knight2.txt")
    files_Input.append(r"../Classes/Knight3.txt")

    files_Input.append(r"../Classes/Koloss1.txt")
    files_Input.append(r"../Classes/Koloss2.txt")
    files_Input.append(r"../Classes/Koloss3.txt")

    #files_Input.append(r"../Classes/Monk1.txt")
    #files_Input.append(r"../Classes/Monk2.txt")
    #files_Input.append(r"../Classes/Monk3.txt")

    files_Input.append(r"../Classes/Pyromancer1.txt")
    files_Input.append(r"../Classes/Pyromancer2.txt")
    files_Input.append(r"../Classes/Pyromancer3.txt")

    files_Input.append(r"../Classes/Ranger1.txt")
    files_Input.append(r"../Classes/Ranger2.txt")
    files_Input.append(r"../Classes/Ranger3.txt")

    files_Input.append(r"../Classes/Sangromancer1.txt")
    files_Input.append(r"../Classes/Sangromancer2.txt")
    files_Input.append(r"../Classes/Sangromancer3.txt")

    

    

    
    maxRankToPrint = 5
    flagPrintHardAI = False
    parseRacesAndClasses(files_Input)
    parseMonsterAI()
    #parseItems()


#### Deprecated Classes:
r"""
#files_Input.append(r"../Races/Faceless.txt")
#files_Input.append(r"../Races/Kobolds.txt") # Deprecated
#files_Input.append(r"../Races/Solarian.txt") # Deprecated

files_Input.append(r"../Classes/Assassin1.txt")
files_Input.append(r"../Classes/Assassin2.txt")
files_Input.append(r"../Classes/Assassin3.txt")

files_Input.append(r"../Classes/Cultist1.txt")
files_Input.append(r"../Classes/Cultist2.txt")
files_Input.append(r"../Classes/Cultist3.txt")

files_Input.append(r"../Classes/Drunkenmaster1.txt")
files_Input.append(r"../Classes/Drunkenmaster2.txt")
#files_Input.append(r"../Classes/Drunkenmaster3.txt")

files_Input.append(r"../Classes/Necromancer1.txt")
files_Input.append(r"../Classes/Necromancer2.txt")
#files_Input.append(r"../Classes/Necromancer3.txt")

files_Input.append(r"../Classes/PlagueDoctor1.txt")
files_Input.append(r"../Classes/PlagueDoctor2.txt")
files_Input.append(r"../Classes/PlagueDoctor3.txt")

files_Input.append(r"../Classes/Rogue1.txt")
files_Input.append(r"../Classes/Rogue2.txt")
files_Input.append(r"../Classes/Rogue3.txt")


files_Input.append(r"../Classes/Spearman1.txt")
files_Input.append(r"../Classes/Spearman2.txt")
#files_Input.append(r"../Classes/Spearman3.txt")

files_Input.append(r"../Classes/Summoner1.txt")
files_Input.append(r"../Classes/Summoner2.txt")
#files_Input.append(r"../Classes/Summoner3.txt")
"""