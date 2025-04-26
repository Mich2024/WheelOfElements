import os
import re
from CardDefinitions_WheelOfFate import *
import copy

maxLevelToPrint = 8
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
    i = 1
    #print(i)
    while quotationMarks < 2:
        
        quotationMarks += len(words[i].split(r'"')) - 1 #effectively counts the number of quotation amrks in string
        #print(words[i])
        tmp = words[i].split(r'"')
        if (tmp[0] == ""):
            tmp = tmp[1:]
        text += " " + tmp[0]
        i += 1
    text = text[1:]
    words = words[i:] #remove entries that we just parsed

    return (text, words)


#returns a dict with stats, passive, modifiers, base cards, leveling cards
def sliceClassToCardTypes(lines):

    CardsBegin = lines.index("Tier1")
    return (lines[:CardsBegin],lines[CardsBegin:])

def sliceStatsToCards(lines):
    var1Begin = lines.index("Variant:1")
    var2Begin = lines.index("Variant:2")
    typeBegin = lines.index("Type")
    semantics = {var1Begin:"Variant:1", var2Begin:"Variant:2", typeBegin:"Type"}
    order = [var1Begin,var2Begin,typeBegin]
    
    order.sort()

    res = {}

    for key, value in semantics.items():
        startIndex = order.index(key)
        start = order[startIndex]
        if startIndex == (len(order)-1): #if we have found the last entry, take everything left
            end = len(lines)
        else:
            end = order[startIndex+1]

        res[value] = lines[start+1:end:]

    return res

#returns an entire action card, without associated level
def parseActionCardFromLine(line, in_classname):
    actCard = actionCard()
    actCard.classname = in_classname
    words = line.split(" ")
    err = False
    while err == False:
        try:
            words.remove("")
        except:
             err = True

    #print(words[0])
    if(words[0] == "Name:"): #stores name and deletes entries from words
        nameWordcount = 1
        for word in words[1:]:
            if not ":" in word:
                actCard.cardName += word
                nameWordcount += 1
                actCard.cardName += " " 
            else:
                actCard.cardName = actCard.cardName[0:]
                words = words[nameWordcount:]
                break
    else:
        print("Error parsing cardName")

    while len(words) > 0:
        if not words[0] == "Text:":
            #print(words)
            parts = words[0].split(":")
            actCard.assignmentDict[parts[0]](actCard,words[0])
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
            actCard.actions.append(["Text: ", result])
            words = words[i:] #remove entries that we just parsed
    return actCard        

# input: all lines before cards 
# output: cards
def parseStatLinesToCards(lines, in_classname):

    name = in_classname[:-1]
    rank = in_classname[:-1]

    parts = sliceStatsToCards(lines)
    Var1 = parts[0]
    Var2 = parts[1]
    TypeExplanation = parts[2][1:]
    elements = []
    explanations = []

    for line in TypeExplanation:
        if startsWith(line, "Element"):
            elements.append(line)
        if startsWith(line, "Explanation"):
            explanations.append(line)

    variants = [Var1, Var2]
    for var in variants:
        card = statCard()
        card.Explanations = explanations
        card.name = name
        card.rank = rank
        card.Type = elements

        mode = ""
        for line in var:
            if line == "Passive":
                mode = "Passive"
                continue
            if line == "Modifiers":
                mode = "Modifiers"
                continue
            if startsWith(line, "Life:"):
                card.assignmentDict[line.split(":")[0]](line.split(":")[1])
                continue

            if mode == "Passive":
                card.passive += line + " \\ "

            if mode == "Modifiers":
                card.modifierUpgrades += line + " \\ "



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

#returns a dict with Stats Normal, Stats Elite, Normal AI, Hard AI
def sliceMonsterToSemantics(lines):
    #print(lines)
    statsNormal = lines.index("Stats Normal")
    statsElite = lines.index("Stats Elite")
    aiNormal = lines.index("Normal AI")
    aiHard = lines.index("Hard AI")

    semantics = {statsNormal:"Stats Normal", statsElite:"Stats Elite", aiNormal:"Normal AI", aiHard:"Hard AI"}
    order = [statsNormal,statsElite,aiNormal,aiHard]
    
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
    #lines = removeMonAIAnnotation(lines) used now
    lines = truncateFile(lines)
    
    #print(lines)
    print("completed sanitization")

    lines = sliceToEnemies(lines)
    #print(lines)
    for linesMonster in lines:
        sectionsMonster = sliceMonsterToSemantics(linesMonster) #returns a dict with Stats Normal, Stats Elite, Normal AI, Hard AI

        #print(linesMonster)
        monAICardNormal = monsterAICard()
        monAICardNormal.setName(linesMonster[0].split(":")[1])
        monAICardNormal.setHardmode(False)


        monAICardHardmode = monsterAICard()
        monAICardHardmode.setName(linesMonster[0].split(":")[1])
        monAICardHardmode.setHardmode(True)
        
        cards = [monAICardNormal, monAICardHardmode]

        for index, card in enumerate(cards):
            #print(sectionsMonster)
            for line in sectionsMonster["Stats Normal"]:
                card.assignmentDict[line.split(":")[0]](card,line)

            for line in sectionsMonster["Stats Elite"]:
                card.assignmentDict[line.split(":")[0]](card,line)
        
            if index == 0: #get proper AI for this card
                linesAI = sectionsMonster["Normal AI"]
            else:
                linesAI = sectionsMonster["Hard AI"]

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
                        words = words[i:] #remove entries that we just parsed

                    
            monsterAICards.append(card)

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
            print(lineItem[10:])
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
        file = filelong.split("\\")[2] # Drops the prefix from the card
        if("Classes" in filelong):
            tier = int(file.split(".")[0][-1]) # classes have tier 1 to 3
        else:
            tier = 0 #signifies race

        #open and sanitize file
        fileToParse = open(filelong,"r")
        lines = fileToParse.readlines()
        fileToParse.close()
        lines = removeComments(lines)
        lines = removeLinebreaks(lines)
        lines = removeEmptyLines(lines)
        lines = truncateFile(lines)
        lines = addSpacesBetweenEmptyText(lines)
        lines = addSpacesAfterText(lines)
        print("completed sanitization")

        linesByCardType = sliceToCardtypes(lines, tier)
        #print(linesByCardType)
        linesStats = linesByCardType["Stats"]
        linesPassive = linesByCardType["Passive"]
        linesModifiers = linesByCardType["Modifiers"]
        linesBaseCards = linesByCardType["Base Cards"]
        if(tier == 1):
            linesLevelCards = linesByCardType["Level Cards"]


        statusCard = statCard() ###############################################
        statusCard.name = file.split(".")[0]
        statusCard.tier = tier
        if(len(linesPassive)==1):
            statusCard.passive = linesPassive[0]
        else:
            print("parsing the passive failed")
        for line in linesStats:
            statusCard.assignmentDict[line.split(":")[0]](statusCard,line.split(":")[1].replace(" ", ""))
        statusCard.modifierUpgrades = linesModifiers
        statusCards.append(statusCard)
        
        #print(statusCard.name)
        #print(statusCard.passive)


        for line in linesModifiers:##########################################
            modifierCards.extend(parseModifierCardFromLine(line, file.split(".")[0]))
            #modifierCards.append(modCard) Happens as part of the parse, since one line caould have multiple varying modifier cards i.e. fire mage +5 -5
        print("parsed modifiers")

        currLevel = (tier - 1) * 3  
        currLevel = max(currLevel, 1) # cap lowest level at 1
        for line in linesBaseCards: #######################################
            #print(line)
            if(currLevel > maxLevelToPrint):
                    break
                
            
            newActCard = parseActionCardFromLine(line, file.split(".")[0])

            newActCard.level = currLevel
            actionCards.append(newActCard)

        if(tier == 1):
            currLevel = 2
            for line in linesLevelCards: #######################################
                
                

                if (line[0:2] == "lv" or line[0:2] == "Lv" or line[0:2] == "LV"):
                    currLevel = int(line[2])
                elif (line[0:1] == "l" or line[0:1] == "L"):
                    currLevel = int(line[1])
                else:
                    if(currLevel > maxLevelToPrint):
                        break
                    actCard = parseActionCardFromLine(line, file.split(".")[0])
                    actCard.level = currLevel
                    actionCards.append(actCard)
        print("parsed action cards")
        

    print("completed parsing")

    texStatCards = ""
    for statusCard in statusCards:
        print(statusCard.name)
        texStatCards += statusCard.serializeToLatex()


    texModCards = ""
    #for modCard in modifierCards:
    #    texModCards += modCard.serializeToLatex()

    texActCards = ""
    for actCard in actionCards:
        texActCards += actCard.serializeToLatex() 


    fileToPrint = open('toPrint.tex', 'w+')
    fileToPrint.write(texStatCards + r"\newpage" + texModCards + texActCards)

    print("wrote file")


    #outCards = open("RacesClasses.tex","w")
    #outModifiers = open("RacesClasses.tex","w")


if __name__ == "__main__":
    ### INPUT OF PROPER RACES AND CLASSES
    files_Input = []    

    #files_Input.append(r"..\Races\Centaur.txt")
    #files_Input.append(r"..\Races\Dragonblood.txt")
    #files_Input.append(r"..\Races\Dwarf.txt")
    #files_Input.append(r"..\Races\Elf.txt")
    files_Input.append(r"..\Races\Fae.txt")
    files_Input.append(r"..\Races\HalfElf.txt")
    #files_Input.append(r"..\Races\Human.txt")
    files_Input.append(r"..\Races\Merman.txt")
    #files_Input.append(r"..\Races\Silverkin.txt")
    files_Input.append(r"..\Races\Thyger.txt")
    
    #files_Input.append(r"..\Classes\Alchemist1.txt")
    #files_Input.append(r"..\Classes\Alchemist2.txt")
    #files_Input.append(r"..\Classes\Alchemist3.txt")

    files_Input.append(r"..\Classes\BladeDancer1.txt")
    files_Input.append(r"..\Classes\BladeDancer2.txt")
    #files_Input.append(r"..\Classes\BladeDancer3.txt")

    #files_Input.append(r"..\Classes\Bloodknight1.txt")
    #files_Input.append(r"..\Classes\Bloodknight2.txt")
    #files_Input.append(r"..\Classes\Bloodknight3.txt")

    #files_Input.append(r"..\Classes\Druid1.txt")
    #files_Input.append(r"..\Classes\Druid2.txt")
    #files_Input.append(r"..\Classes\Druid3.txt")

    #files_Input.append(r"..\Classes\Huntsman1.txt")
    #files_Input.append(r"..\Classes\Huntsman2.txt")
    #files_Input.append(r"..\Classes\Huntsman3.txt")

    #files_Input.append(r"..\Classes\Koloss1.txt")
    #files_Input.append(r"..\Classes\Koloss2.txt")
    #files_Input.append(r"..\Classes\Koloss3.txt")

    #files_Input.append(r"..\Classes\Metallurge1.txt")
    #files_Input.append(r"..\Classes\Metallurge2.txt")
    #files_Input.append(r"..\Classes\Metallurge3.txt")

    files_Input.append(r"..\Classes\Monk1.txt")
    #files_Input.append(r"..\Classes\Monk2.txt")
    #files_Input.append(r"..\Classes\Monk3.txt")

    #files_Input.append(r"..\Classes\Priest1.txt")
    #files_Input.append(r"..\Classes\Priest2.txt")
    #files_Input.append(r"..\Classes\Priest3.txt")

    files_Input.append(r"..\Classes\Pyromancer1.txt")
    files_Input.append(r"..\Classes\Pyromancer2.txt")
    #files_Input.append(r"..\Classes\Pyromancer3.txt")

    files_Input.append(r"..\Classes\Ranger1.txt")
    #files_Input.append(r"..\Classes\Ranger2.txt")
    #files_Input.append(r"..\Classes\Ranger3.txt")

    files_Input.append(r"..\Classes\Strategist1.txt")
    files_Input.append(r"..\Classes\Strategist2.txt")
    #files_Input.append(r"..\Classes\Strategist3.txt")

    

    

    
    maxLevelToPrint = 5
    flagPrintHardAI = False
    #parseRacesAndClasses(files_Input)
    parseMonsterAI()
    #parseItems()

    #### Deprecated Classes:
r"""
#files_Input.append(r"..\Races\Faceless.txt")
#files_Input.append(r"..\Races\Kobolds.txt") # Deprecated
#files_Input.append(r"..\Races\Solarian.txt") # Deprecated

files_Input.append(r"..\Classes\Assassin1.txt")
files_Input.append(r"..\Classes\Assassin2.txt")
files_Input.append(r"..\Classes\Assassin3.txt")

files_Input.append(r"..\Classes\Cultist1.txt")
files_Input.append(r"..\Classes\Cultist2.txt")
files_Input.append(r"..\Classes\Cultist3.txt")

files_Input.append(r"..\Classes\Drunkenmaster1.txt")
files_Input.append(r"..\Classes\Drunkenmaster2.txt")
#files_Input.append(r"..\Classes\Drunkenmaster3.txt")

files_Input.append(r"..\Classes\Necromancer1.txt")
files_Input.append(r"..\Classes\Necromancer2.txt")
#files_Input.append(r"..\Classes\Necromancer3.txt")

files_Input.append(r"..\Classes\PlagueDoctor1.txt")
files_Input.append(r"..\Classes\PlagueDoctor2.txt")
files_Input.append(r"..\Classes\PlagueDoctor3.txt")

files_Input.append(r"..\Classes\Rogue1.txt")
files_Input.append(r"..\Classes\Rogue2.txt")
files_Input.append(r"..\Classes\Rogue3.txt")


files_Input.append(r"..\Classes\Spearman1.txt")
files_Input.append(r"..\Classes\Spearman2.txt")
#files_Input.append(r"..\Classes\Spearman3.txt")

files_Input.append(r"..\Classes\Summoner1.txt")
files_Input.append(r"..\Classes\Summoner2.txt")
#files_Input.append(r"..\Classes\Summoner3.txt")
"""