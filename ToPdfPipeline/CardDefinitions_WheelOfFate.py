import inflect
import copy

def nothing(kwargs):
        return

linebreakStringNanDeck_TEXT = "\\13\\"
linebreakStringNanDeck_htmltext = "<br>"

def removeColons(line):
    res = line.replace(":","")
    return res

def texifyMultSign(line):
    
    
    line = line.replace('*',r" $\times $ ")
    return line

def addNanDeckLinebreaks(text: str):
    res = ""
    last_copy = 0
    last_space = 0
    for i, letter in enumerate(text):
        if letter == " ":
            last_space = i
        
        '''if letter in [".", "!", "?"] :
            last_space = i+1
            res += text[last_copy:last_space] + "\\13\\"
            last_copy = last_space + 1'''

        if i % 21 == 0:
            if(i == 0):
                continue
            res += text[last_copy:last_space] + "\\13\\"
            last_copy = last_space + 1 # the +1 gets rid of leading spaces
            break

    res += text[last_copy:]

    return res

#expexts bronze, silver, gold or diamond or mithril as input.
def tier_str_to_int(str_tier):
    res = -1
    str_tier = str_tier.strip().lower()
    if(str_tier == "bronze"):
        res = 1
    elif(str_tier == "silver"):
        res = 2
    elif(str_tier == "gold"):
        res = 3
    elif(str_tier == "diamond"):
        res = 4
    elif(str_tier == "mithril"):
        res = 4
    return res

#expexts int from 1 to 4
def tier_int_to_str(int_tier):
    res = "error"
    str_tier = str_tier.strip().lower()
    if(str_tier == 1):
        res = "bronze"
    elif(str_tier == 2):
        res = "silver"
    elif(str_tier == 3):
        res = "gold"
    elif(str_tier == 4):
        res = "mithril"
    return res

symbolDict = {
    
    #"L":r"\symLoot", Mechanic removed from game
    "E":r"\symEnergy",
    "Energy":r"\symEnergy",
    "A":r"\symAttack",
    "Attack":r"\symAttack",
    "R":r"\symRanged",
    "Ranged":r"\symRanged",
    "T":r"\symTargets",
    "AOE":"todo", # todo
    "H":r"\symHeal",
    "Heal":r"\symHeal",
    "M":r"\symMovement",
    "Jump":r"\symJump",
    
    #stat symbols
    "Life":r"\symLife",
    "Stamina":r"\symStamina",
    "Maximum Energy":r"\symEnergy",
    "Energy Regeneration":r"\symEnergyRegen",

    #Types, meta effets
    "TypeAttack":r"\symTypeAttack",
    "TypeMovement":r"\symTypeMovement",
    "TypeSpecial":r"\symTypeSpecial",
    "Exhaust":r"\symExhaust",
    "Unrecoverable":r"\symUnrecoverable",
    "Perpetual":r"\symPerpetual",
    "Pips":r"\symPips",

    #Elements 
    "Fire":r"\symAddFire",
    "Earth":r"\symAddEarth",
    "Metal":r"\symAddMetal",
    "Water":r"\symAddWater",
    "Wood":r"\symAddWood",

    # Attack effects
    "Pull":r"\symPull",
    "Push":r"\symPush",
    "Pierce":r"\symPierce",
    "P":r"\symPierce", #Todo, maybe rename?
    "Corrosion":r"\symCorrosion",
    "Corrode":r"\symCorrosion",
    "D6":r"\symD6",
    "Blaze":r"\symBlaze",
    

    # Boons
    "Blessing":r"\symBlessing",
    "Bless":r"\symBlessing",
    "Advantage":r"\symAdvantage",
    "Fortify":r"\symFortify",
    "Shield":r"\symShield",
    "S":r"\symShield",
    "Vengeance":r"\symVengeance",
    "V":r"\symVengeance",
    "Regeneration":r"\symRegenerate",
    "Regenerate":r"\symRegenerate",
    "Invisibility":r"\symInvisibility",
    "Invisibile":r"\symInvisibility",
    "Powerful":r"\symPowerful",
    "Disengage":r"\symDisengage",
    "Flurry":r"\symFlurry",

    # Banes
    "Curse":r"\symCurse",
    "Disadvantage":r"\symDisadvantage",
    "Muddle":r"\symDisadvantage",
    "Confuse":r"\symConfuse",
    "Vulnerable":r"\symVulnerable",
    "Wounded":r"\symWound",
    "Wound":r"\symWound",
    "Trauma":r"\symTrauma",
    "Disarm":r"\symDisarm",
    "Cripple":r"\symCripple",
    "Stun":r"\symStun",
    "Silence":r"\symSilence",
    "Poison":r"\symPoison",

    #Modifier specific
    "Draw":r"\symDraw",

}


attackModifiers = {

    "R":r"\symRange",
    "T":r"\symTargets",

    #Elements 
    "AFire":r"\symAddFire",
    "AEarth":r"\symAddEarth",
    "AMetal":r"\symAddMetal",
    "AWater":r"\symAddWater",
    "AWood":r"\symAddWood",

    # Attack effects
    "Pull":r"\symPull",
    "Push":r"\symPush",
    "Pierce":r"\symPierce",
    "P":r"\symPierce", #Todo, maybe rename?
    "Corrosion":r"\symCorrosion",
    "Corrode":r"\symCorrosion",
    

    # Boons
    "Blessing":r"\symBlessing",
    "Bless":r"\symBlessing",
    "Advantage":r"\symAdvantage",
    "Fortify":r"\symFortify",
    "Shield":r"\symShield",
    "S":r"\symShield",
    "Vengeance":r"\symVengeance",
    "V":r"\symVengeance",
    "Regeneration":r"\symRegenerate",
    "Regenerate":r"\symRegenerate",
    "Invisibility":r"\symInvisibility",
    "Invisibile":r"\symInvisibility",

    # Banes
    "Curse":r"\symCurse",
    "Disadvantage":r"\symDisadvantage",
    "Muddle":r"\symDisadvantage",
    "Confuse":r"\symConfuse",
    "Vulnerable":r"\symVulnerable",
    "Wounded":r"\symWound",
    "Wound":r"\symWound",
    "Trauma":r"\symTrauma",
    "Disarm":r"\symDisarm",
    "Cripple":r"\symCripple",
    "Stun":r"\symStun",
    "Silence":r"\symSilence",
    "Poison":r"\symPoison",

}

dictExplanation = {

    # Attack effects
    "Pull":r"Pulls a dude",
    "Push":r"Pushes a dude",    
    "Pirece":r"Pierce is deprecated, remove it from your cards",   

    # Boons
    "Blessing":r"Add a temporary *2 to the targets discard. Removed when modifier is used",
    "Bless":r"Add a temporary *2 to the targets discard. Removed when modifier is used",
    "Shield":r"Prevents one damage from any attack that hits you. Removed at the start of the turn",
    "S":r"Prevents one damage from any attack that hits you. Removed at the start of the turn",
    "Vendetta":r"Attacks against targets with Vendetta cause the attacker to loose 1 life per stack after the attack. Removed at the start of the turn",
    "V":r"Attacks against targets with Vendetta cause the attacker to loose 1 life per stack after the attack. Removed at the start of the turn",
    "Regeneration":r"At the start of the turn, gain 2 life and remove a stack of regeneration",
    "Regenerate":r"At the start of the turn, gain 2 life and remove a stack of regeneration",
    "Invisibility":r"Monsters cannot target invisible players. Removed at the start of the turn",
    "Invisibile":r"Monsters cannot target invisible players. Removed at the start of the turn",
    "Powerful":r"Add A:+1 to your attacks",

    # Banes
    "Curse":r"Add a temporary *0 to the targets discard. Removed when modifier is used",
    "Vulnerable":r"Vulnerable Targets take one extra damage from every attack. Cannot stack. Cannot be removed without card effects",
    "Poison":r"\symPoison",

    # Esoteric
    "Obstacle":r"Obstacles can only be placed on tiles without units. They cannot be placed in such a way as to make hex without an obstacle unreachable by standard movement. They can be placed on difficult and dangerous terrain.",
    "Obstacles":r"Obstacles can only be placed on tiles without units. They cannot be placed in such a way as to make hex without an obstacle unreachable by standard movement. They can be placed on difficult and dangerous terrain.",
    "Taunt":r"Move the rightmost enemy from the left player, or the leftmost enemy from the right player to your enemy pool.",

}

#converst an action list into tex. Does not add "{}"
def serializeActionToTex(inputActions):
    res = ""
    flagAttackChainStarted = False
    flagFirstLinebreak = True
    for action in inputActions:
            #print(action)

            if isinstance(action, list):
                flagAttackChainStarted = False
                if not flagFirstLinebreak:
                    res += r"\\ "
                else:
                    flagFirstLinebreak = False
                action = action[1:] # remove "Text:"" .split(":")[0]
                action = action[0].split(" ")
                for word in action:
                    #print(word.split(":")[0])
                    if(word.split(":")[0] in symbolDict):
                    
                        res += " " + symbolDict[word.split(":")[0]] + " " + word + " "
                    else:
                        res += word + " "
                    
            
            else:
                # three cases: 
                # movement: always gets new line, does not start chain
                # attack & Heal: always gets new line, starts chain
                # Modifier: if not chain -> gets new line, starts chain

            #TODO check for elemental removes?

                parts = action.split(":")
                if (parts[0] == "A" or parts[0] == "H" or ( parts[0] in attackModifiers and flagAttackChainStarted == False) ):
                    if not flagFirstLinebreak:
                        res += r"\\ "
                    else:
                        flagFirstLinebreak = False
                if (parts[0] == "A" or parts[0] == "H" or parts[0] in attackModifiers):
                    flagAttackChainStarted = True
                else:
                    flagAttackChainStarted = False

                if parts[0] in symbolDict:
                    res += " " + symbolDict[parts[0]]
                res += " " + parts[0] 
                if len(parts) == 2:
                    res += ":~" + parts[1]
                    res += " "
                

    return res

#converst an action list into nandeck String. Does not add "" around the text
def serializeActionToNanDeck(inputActions):
    res = ''
    first = True
    for action in inputActions:
            if not first:
                res += linebreakStringNanDeck_htmltext
            else:
                first = False
            #print(action)

            if isinstance(action, list): #Text
                action = action[1:] # remove "Text:"" .split(":")[0]
                action = action[0].split(" ")
                for word in action:
                    #print(word.split(":")[0])
                    if(word.split(":")[0] in symbolDict):
                    
                        res += " " + symbolDict[word.split(":")[0]] + " " + word + " "
                    else:
                        res += word + " "
                    
            
            else:
                if action.casefold() == "opt":
                    res += "------ Opt Paid ------ "

                elif action.split(":")[0].casefold() == "blaze":
                    res += r"---Card 1 -> \symBlaze Blaze " + action.split(":")[1] + "---"
                else:

                    parts = action.split(":")
                    if parts[0] in symbolDict:
                        res += " " + symbolDict[parts[0]]
                    res += " " + parts[0] 
                    if len(parts) == 2:
                        res += ": " + parts[1]
                        res += " "
                
    return res.strip()

#converst an action list into nandeck String. Does not add "" around the text
def serializeMonsterActionToNanDeck(inputActions):
    res = ''
    for action in inputActions:
            #print(action)

            if isinstance(action, list): #Text
                action = action[1:] # remove "Text:"" .split(":")[0]
                action = action[0].split(" ")
                for word in action:
                    #print(word.split(":")[0])
                    if(word.split(":")[0] in symbolDict):
                    
                        res += " " + symbolDict[word.split(":")[0]] + " " + word + " "
                    else:
                        res += word + " "
                    
            
            else:
                if action.casefold() == "opt":
                    res += "------ Opt Paid ------ "

                elif action.split(":")[0].casefold() == "blaze":
                    res += r"--- \symBlaze Blaze " + action.split(":")[1] + " --- "
                else:

                    parts = action.split(":")
                    if parts[0] in symbolDict:
                        res += " " + symbolDict[parts[0]]
                    res += " " + parts[0] 
                    if len(parts) == 2:
                        res += ": " + parts[1]
                        res += " "
                
    return res

class actionCard:

    '''energyCost = "0"
    cardType = "Special" #Should be Attack, Movement or Special
    cardName = ""
    cardModifiers = []
    actions = []
    level = "0"
    aoe = ""
    tier = "0"'''

    def __init__(self):

        self.energyCost = "0"
        #format in here is: [Opt;Earth;X, Wood;2] etc
        self.manaCost = ""
        self.cardType = "Special" #Should be Attack or Special
        self.cardName = ""
        self.classname = "Class designation missing"
        self.cardModifiers = []
        self.actions = []
        self.rank = "0"
        self.aoe = ""
        self.tier = "0"
    

    def setLevel(self, x):
        self.rank = x
    def setType(self, x):
        self.cardType = x
    def setEnergyCost(self, x):
        self.energyCost = x
    def appendManaCost(self, x):
        #print(x.split(":")[1])
        self.manaCost = x.split(":")[1]
    def appendAction(self, x):
        self.actions.append(x)
    def appendModifier(self, x):
        self.cardModifiers.append(x)
    def appendAoe(self, x):
        self.aoe = x
    def appendText(self, x):
        self.actions.append(["Text: ", x])


    assignmentDict = {
        "Type":setType,
        "Attack":setType,
        "Special":setType,
        "L":setLevel,
        "E":setEnergyCost,
        "ManaCost":appendManaCost,
        "Text":appendText,

        "A":appendAction,
        "R":appendAction,
        "Ranged":appendAction,
        "T":appendAction,
        "Targets":appendAction,
        "Target":appendAction,
        
        "AOE":appendAoe,
        "Aoe":appendAoe,

        "H":appendAction,
        "Heal":appendAction,
        "Regeneration":appendAction,
        "Regenerate":appendAction,
        "Invisibility":appendAction,
        "Bless":appendAction,
        "Blessing":appendAction,
        "Advantage":appendAction,
        "Powerful":appendAction,
        "Self":appendAction,
        "Flurry":appendAction,

        "M":appendAction,
        "Jump":appendAction,
        "P":appendAction,
        "Pierce":appendAction,
        "S":appendAction,
        "Shield":appendAction,
        "Push":appendAction,
        "Pull":appendAction,
        "Corrode":appendAction,
        "Cripple":appendAction,
        "Disarm":appendAction,
        "Confuse":appendAction,
        "Poison":appendAction,
        "Wound":appendAction,
        "Disadvantage":appendAction,
        "Trauma":appendAction,
        "Vulnerable":appendAction,
        "Stun":appendAction,
        "Curse":appendAction,
        "V":appendAction,
        "Vendetta":appendAction,
        "Panic":appendAction,
        "Taunt":appendAction,
        "Disengage":appendAction,
        "D6":appendAction,
        "Blaze":appendAction,
        "Opt":appendAction,

        "Exhaust":appendModifier,
        "Unrecoverable":appendModifier,

        "Fire":appendAction,
        "Earth":appendAction,
        "Metal":appendAction,
        "Water":appendAction,
        "Wood":appendAction,
        
    }

    def serializeToNandeck(self, order: int):

        
        template_card = open('Templates/Action_Card_Single.txt', 'r')
        template_card = template_card.read()
        template_line_aoe = ""
        

        if self.aoe != "":
            template_line_aoe = open('Templates/Action_Card_AOE_Line.txt', 'r')
            template_line_aoe = template_line_aoe.read()
            template_line_aoe = template_line_aoe.replace( r"${aoe}", removeColons(self.aoe))
        template_card = template_card.replace(r"${AOE}",template_line_aoe)
            

        template_card = template_card.replace(r"${Order}",str(order)).replace(r"${Name}", self.cardName)

        optCost = ""
        
        if(self.manaCost) != "":
            cost = self.manaCost.split(";")
            for c in cost:
                sym = ""
                if(c in symbolDict):
                    sym += symbolDict[c]
                    optCost += sym + " "
                else:
                    optCost += c + " "
        else: 
            optCost = " - "
                    

        template_card = template_card.replace(r"${Opt_Cost}",optCost)

        textAction = serializeActionToNanDeck(self.actions)

        template_card = template_card.replace(r"${TextBox}",textAction)

        classname = self.classname 
        if(not str(self.rank) == "0"):
            classname += " " + str(self.rank)
        template_card = template_card.replace(r"${Class}",classname)

        textTier = "Undef"
        colTier = "bronze"
        if self.tier == "1":
            textTier = "Bronze"
            colTier = "Bronze"
        elif self.tier == "2":
            textTier = "Silver"
            colTier = "Silver"
        elif self.tier == "3":
            textTier = "Gold"
            colTier = "Gold"
        elif self.tier == "4":
            textTier = "Dia"
            colTier = "Dia"

        template_card = template_card.replace(r"${Rank}",textTier).replace(r"${Col_Rank}",colTier)
        
        return template_card


    def serializeToLatex(self):

        #print(self.actions)
        res = ""
        
        if(self.aoe != ""):
            #%Input: tier/level, name, Type, Energy Cost, Text, aoesym
            res += r"\aoeCard"
        else:
            #%Input: tier/level, name, Type, Energy Cost, Text
            res += r"\basicCard"
        res += "{" + self.cardName + "}"
        res += "{" + self.classname + str(self.rank) + "}"
        res += "{" + self.cardType + "}"

        #Costs
        res += "{" 

        if("Exhaust" in self.cardModifiers):
            res += " " + symbolDict["Exhaust"] + " "

        cost = self.manaCost.split(";")
        for c in cost:
            sym = ""
            if(c in symbolDict):
                sym += symbolDict[c]
                res += sym + " "
            else:
                res += c + " "
            

        res += r"}" 
        
        res += "{"
        #print(self.actions)
        res += serializeActionToTex(self.actions)
                
        res += "} {"

        while len(self.cardModifiers) > 0:
            mod = self.cardModifiers[0]

            res += symbolDict[mod] + " "
            self.cardModifiers = self.cardModifiers[1:]


        res += "}"


        if(self.aoe != ""):
            res += "{" + r"\symAoe{" + removeColons(self.aoe) + "} }"
        res += "\n"
        #\symCardTier
        return res
    
    




class modifierCard:
    def __init__(self):
        self.specials = [] # should be a list of stirngs like, wound, draw, target...
        self.classname = "Class designation missing"
        self.modifier = "0" 

    def serializeToLatex(self):
        res = r"\modifierCard"
        res += "{" + self.modifier + r"}{ \\ "
        for s in self.specials:
            if s in symbolDict:
                res += symbolDict[s] + " "
            else:
                res += s + r"\\ "
        res += r"}"

        res += "{" + self.classname + "}"
        res += "\n"
        return res

class tableauRace:
    def __init__(self):


        self.L1R1 = ""
        self.L1R2 = ""
        self.L1R3 = ""
        self.L1R4 = ""

        self.L2R1 = ""
        self.L2R2 = ""

        self.L3R1 = ""

        self.mods = [self.L1R1,self.L1R2,self.L1R3,self.L1R4,self.L2R1,self.L2R2,self.L3R1]

    def symbolify_mod(self, words_mod):
        line_mod = ""
        for word in words_mod:
            #print(word.split(":")[0])
            word = word.replace(",","")
            if(word.split(":")[0] in symbolDict):
            
                line_mod += " " + symbolDict[word.split(":")[0]]

            elif(word.split(":")[0].lower() == "draw"):
                print(word)
                line_mod += " " + r"\symDraw" + " " + word + " "
            else:
                line_mod += word + " "

        return line_mod


    def serializeToNandeck(self, order):
        

        template_line_mod = open('Templates/Tableau_Line_Mod.txt', 'r')
        template_line_mod = template_line_mod.read()

        self.L1R1 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L1R1.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L1R1 = self.L1R1.replace(r"${Order}",str(order)).replace(r"${Hor}",str(0)).replace(r"${Vert}",str(0))
        self.L1R2 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L1R2.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L1R2 = self.L1R2.replace(r"${Order}",str(order)).replace(r"${Hor}",str(1)).replace(r"${Vert}",str(0))
        self.L1R3 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L1R3.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L1R3 = self.L1R3.replace(r"${Order}",str(order)).replace(r"${Hor}",str(2)).replace(r"${Vert}",str(0))
        self.L1R4 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L1R4.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L1R4 = self.L1R4.replace(r"${Order}",str(order)).replace(r"${Hor}",str(3)).replace(r"${Vert}",str(0))

        self.L2R1 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L2R1.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L2R1 = self.L2R1.replace(r"${Order}",str(order)).replace(r"${Hor}",str(0)).replace(r"${Vert}",str(1))
        self.L2R2 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L2R2.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L2R2 = self.L2R2.replace(r"${Order}",str(order)).replace(r"${Hor}",str(1)).replace(r"${Vert}",str(1))

        self.L3R1 = template_line_mod.replace(r"${Mod}", '"' + self.symbolify_mod(self.L3R1.split(" ")).replace("Add ", r"<br>Add ").replace("Remove", r"<br>Remove").replace(",","") + '"')
        self.L3R1 = self.L3R1.replace(r"${Order}",str(order)).replace(r"${Hor}",str(0)).replace(r"${Vert}",str(2))
        
        lines_mods = ""

        lines_mods += self.L1R1
        lines_mods += self.L1R2
        lines_mods += self.L1R3
        lines_mods += self.L1R4
        lines_mods += self.L2R1
        lines_mods += self.L2R2
        lines_mods += self.L3R1
            
        return lines_mods
    
    def serializeModToNandeck(self, words_mod ,order, name_species):
        count = int(words_mod[0])
        line_mod = self.symbolify_mod(words_mod[1:])

        template_mod_single = open('Templates/Dice_Single.txt', 'r')
        template_mod_single = template_mod_single.read()

        template_mod_single = template_mod_single.replace(r"${Mod}",line_mod)

        res = ""
        for i in range(count):
            res += template_mod_single.replace(r"${Order}",str(order+i))
        return count, res
    

    
    def serializeModifiersToNandeck(self,order, name_species):
        nandeckMods = ""

        count_total = 0

        self.mods = [self.L1R1,self.L1R2,self.L1R3,self.L1R4,self.L2R1,self.L2R2,self.L3R1]

        for line_mod in self.mods:
            words = line_mod.split(" ")
            mode = "Add"
            breakpoints = ["Add", "Remove"]
            words_current = []
            for word in words:
                #print(word)
                if word in breakpoints:
                    #print(words_current)
                    if(words_current != []):
                        count_curr, nanDeckOut = self.serializeModToNandeck(words_current,order+count_total, name_species)

                        nandeckMods += nanDeckOut
                        count_total += count_curr
                        words_current = []
                    mode = word
                else:
                    if(mode =="Add"):
                        words_current.append(word)
            if(words_current != []):
                count_curr, nanDeckOut = self.serializeModToNandeck(words_current,order+count_total, name_species)

                nandeckMods += nanDeckOut
                count_total += count_curr
                words_current = []

        return count_total, nandeckMods




class statCard:

    def __init__(self):

        self.name = "No Init"
        self.rank = "No Init"
        self.life = "No Init"
        self.passive = ""
        self.elements = []
        self.explanations = []
        self.tableau = None
        self.lore = "Ipsum Lorum"
        self.tierCards = "[col_mithril]"
        self.tierPassive = "[col_mithril]"
        self.intTierPassive = 4
        self.intTierCards = 4
        self.intTierDice = 4
        self.tierMods = "[col_mithril]"

    def setLife(self, l):
        self.life = l
    def setTierCards(self, l: str):
        self.tierCards = "[col_" + l.strip().lower() + "]"
        self.intTierCards = tier_str_to_int(l)
    def setTierPassive(self, l: str):
        self.tierPassive = "[col_" + l.strip().lower() + "]"
        self.intTierPassive = tier_str_to_int(l)
    def setTierMods(self, l: str):
        self.tierMods = "[col_" + l.strip().lower() + "]"
        self.intTierDice = tier_str_to_int(l)
    
    assignmentDict = {
        "Life":setLife, #stat cards start here
        "TierCards":setTierCards, 
        "TierPassive":setTierPassive, 
        "TierMods":setTierMods, 
    }
    #%Input: name, tier, stats, passive, skills
    def serializeToLatex(self):
        res = r"\statusCard"
        res += "{" + self.name + "}"
        res += "{" + str(self.rank) + "}"
        res += "{" 
        res += symbolDict["Life"] + r"\hspace{0.0cm} Life: " + str(self.life) + r"\\ "
        res += "}"
        res += "{" + self.passive + " \\ }"
        res += "{" + self.modifierUpgrades + r" \\ "
        #for line in self.explanations:
        #    res += line + r" \\ "  + dictExplanation[line.split(":")[1]] + r" \\" 
        for line in self.elements:
            res += line
        res += r"} "
        res += "\n"
        return res

    def serializeToNandeck(self, order):
        passive_new = ""

        for word in self.passive.split(" "):
            if(word.split(":")[0] in symbolDict):
            
                passive_new += " " + symbolDict[word.split(":")[0]] + " " + word + " "
            else:
                passive_new += word + " "
        passive_new = passive_new.strip()
        
        if isinstance(self.tableau, tableauRace):

            
            template_line_life = open('Templates/Tableau_Line_Life.txt', 'r')
            template_line_life = template_line_life.read()
            template_line_passive = open('Templates/Tableau_Line_Passive.txt', 'r')
            template_line_passive = template_line_passive.read()
            template_race = open('Templates/Tableau_Race_Single.txt', 'r')
            template_race = template_race.read()
            

            
            #lines_mods = self.tableau.serializeToNandeck(order)
            

            template_line_life = template_line_life.replace(r"${Order}",str(order)).replace(r"${Life}",self.life.strip())
            template_line_passive = template_line_passive.replace(r"${Order}",str(order)).replace(r"${Passive}",passive_new).replace(r"${IntTierPassive}",str(self.intTierPassive))
            template_race = template_race.replace(r"${Order}",str(order)).replace(r"${Race}", self.name ).replace(r"${IntTierCards}",str(self.intTierCards)).replace(r"${IntTierDice}",str(self.intTierDice))
            template_race = template_race.replace(r"${TierMod}",self.tierMods).replace(r"${TierPassive}",self.tierPassive)
            res = template_race.replace(r"${Life}",template_line_life).replace(r"${Passive}",template_line_passive)

        else:
            title = self.name + " " + str(self.rank)
            templateShingle = open('Templates/Shingle_Class_Card.txt', 'r')
            templateShingle = templateShingle.read()

            #print(self.passive)

            
            templateEdge = ""
            if(self.rank == 1):
                templateEdge = open('Templates/Shingle_Class_Edge_TR.txt', 'r')
                templateEdge = templateEdge.read()
            if(self.rank == 2):
                templateEdge = open('Templates/Shingle_Class_Edge_BR.txt', 'r')
                templateEdge = templateEdge.read()
            if(self.rank == 3):
                templateEdge = open('Templates/Shingle_Class_Edge_BL.txt', 'r')
                templateEdge = templateEdge.read()

            res = templateShingle.replace(r"${Edge}", templateEdge).replace(r"${Order}", str(order)).replace(r"${Title}",title).replace(r"${Life}", str(self.life).strip()).replace(r"${Passive}", passive_new)

        return res
    
    def serializeModifiersToNandeck(self, order):
        assert isinstance(self.tableau, tableauRace)
        return self.tableau.serializeModifiersToNandeck(order, self.name)
    
    def serializeStripToNandeck(self, order):

        if isinstance(self.tableau, tableauRace): #strips only exist for classes
            return ""
        
        title = self.name + " " + str(self.rank)
        templateStrip = open('Templates/Strip_Single.txt', 'r')
        templateStrip = templateStrip.read()

        templateRank = open('Templates/Strip_Rank_' + str(self.rank) + '.txt', 'r')
        templateRank = templateRank.read()

        nandeckStrip = templateStrip.replace(r"${Name}", str(self.name).strip() + " " + str(self.rank)  ).replace(r"${Sym_Rank}", templateRank)

        ele_1 = self.elements[0]
        ele_2 = ""
        if len(self.elements) > 1:
            ele_2 = self.elements[1]
        nandeckStrip = nandeckStrip.replace(r"${Order}",str(order)).replace(r"${Element_1}",ele_1).replace(r"${Element_2}",ele_2)


        #print(self.passive)

        return nandeckStrip

class monsterAICard:

    def __init__(self):

        self.name = ""
        self.life = ""
        self.passive = ""
        self.count = 0
        self.actions = []
        self.tempAction = []
        self.flagAB = False
        self.flagHardMode = False

    def setName(self,n):
        self.name = n

    def setLife(self,n):
        numString = n.split(":")[1]
        self.life = numString

    def setPassive(self,n):
        passive = n.split(":")
        passive = ' '.join(passive[1:])
        self.passive = passive

    def appendAction(self,n):
        if("Rolls" in n):
            if(self.tempAction != []):
                self.actions.append(self.tempAction[:])
                self.tempAction = []
        self.tempAction.append(n)

    def setAB(self, x):
        if x == "AB":
            self.flagAB = True
        else:
            self.flagAB = x
    def setHardmode(self, s):
        self.flagHardMode = s
 
    assignmentDict = {
        "Name":setName, #stat cards start here
        "Rolls":appendAction,
        "AB":setAB,

        "Life":setLife,
        "Passive":setPassive,

    }
    #%Input: name, tier, stats, passive, skills
    def serializeToLatex(self):

        if(self.tempAction != []):
                self.actions.append(self.tempAction[:])# appends the last temp action to the real list

        res = r"\monsterAICard"
        res += "{" + self.name
        if self.flagHardMode == True:
            res += r" Hardmode"
        res += "}"
        #res += "{Hardmode " + str(self.flagHardMode) + "}"
        #res += "{AB " + str(self.flagAB) + "}"

        #Life: #3 \\
							#4 \\
							#5

        #Life: #6 #9\\
							#7 \\
							#8


        res += "{ Life: "+ self.life
        
        if self.passive != "":
            res += r" \\"
            res += " Passive: "
            res += self.passive
        res += "}"

        res += "{"
        #make actions into nice boxes
        #print(self.actions)
        print(self.actions)
        for index, action in enumerate(self.actions):
            #print(action[0])
            rolls = action[0].split(":")[1]
            res += rolls + r" "
            action = action[1:]
            res += serializeActionToTex(action)
            res += r"\\"
                
            
        res += "}"
        
        res += "\n"

        res = texifyMultSign(res)
        res = self.count*res
        return res
    
    def serializeToNandeck(self,order):

        if(self.tempAction != []):
                self.actions.append(self.tempAction[:])# appends the last temp action to the real list

        template_monster_line_life = open('Templates/Monster_Line_Life.txt', 'r')
        template_monster_line_life = template_monster_line_life.read()
        #life_max = int(self.life)
        nanDeckLife = template_monster_line_life.replace(r"${Life}", self.life)
        #print(nanDeckLife)
        #print(life_max)
        '''row = 0 #line
        col = 0
        while(life_max) > 0:
            if life_max >= 50:
                tmp = template_monster_line_life.replace(r"${Color}", "[col_mithril]").replace(r"${Life}", "50")
                life_max -= 50
            elif life_max >= 10:
                tmp = template_monster_line_life.replace(r"${Color}", "[col_gold]").replace(r"${Life}", "10")
                life_max -= 10
            elif life_max >= 5:
                tmp = template_monster_line_life.replace(r"${Color}", "[col_silver]").replace(r"${Life}", "5")
                life_max -= 5
            else:
                print("[Error] unfuck the life total of: " + self.name + " sitting at: " + str(life_max))
            
            nanDeckLife += tmp.replace(r"${PosX}", "[x_hp_" + str(col) + "]").replace(r"${PosY}", str(row))
            row += 1
            if row > 4:
                row = 0
                col = 1'''
        

        

        #print(self.actions)
        count_actions = len(self.actions)
        start_actions = "[start_actions]"
        if(count_actions < 3):
            start_actions = "[start_actions] + [space_text_18] * 2"
        if(count_actions > 3):
            print("[Error] unfuck the action count of: "  + self.name + " sitting at: " + str(count_actions) )

        template_monster_line_passive = open('Templates/Monster_Line_Passive.txt', 'r')
        template_monster_line_passive = template_monster_line_passive.read()
        nanDeckPassive = ""
        if (self.passive != ""):
            nanDeckPassive = template_monster_line_passive.replace(r"${Passive}", self.passive).replace(r"${StartActions}", start_actions)

        template_monster_line_action = open('Templates/Monster_Line_Action.txt', 'r')
        template_monster_line_action = template_monster_line_action.read()

        template_monster_line_dice = open('Templates/Monster_Line_Dice.txt', 'r')
        template_monster_line_dice = template_monster_line_dice.read()

        template_monster_line_box = open('Templates/Monster_Line_Box.txt', 'r')
        template_monster_line_box = template_monster_line_box.read()

        nanDeckActions = ""
        count_action_curr = 0
        
        for index, action in enumerate(self.actions):
            nanDeckDice = ""
            rolls = action[0].split(":")[1]
            dice = ""
            count_dice = 0
            count_dice_remaining = len(rolls.split(","))
            flag_second_row = 0
            for roll in rolls.split(","):
                count_dice += 1
                count_dice_remaining -= 1
                p = inflect.engine()

                try: #rolls
                    dice += r"\symD" + p.number_to_words(int(roll.strip())).capitalize()
                    if(count_dice == 2):
                        #print(start_actions)
                        nanDeckDice += template_monster_line_dice.replace(r"${Dice}", dice).replace(r"${PosYAction}", start_actions + " + [space_text_18] * " + str(2*count_action_curr + flag_second_row)).replace(r"${PosXAction}", "0")
                        count_dice = 0
                        dice = ""
                        flag_second_row = 1
                    elif(count_dice_remaining == 0):
                        nanDeckDice += template_monster_line_dice.replace(r"${Dice}", dice).replace(r"${PosYAction}", start_actions + " + [space_text_18] * " + str(2*count_action_curr + flag_second_row)).replace(r"${PosXAction}", "0.2")
                except: #abc
                    dice += roll.strip()
                    nanDeckDice += template_monster_line_box.replace(r"${Dice}", dice).replace(r"${PosYAction}", start_actions + " + [space_text_18] * " + str(2*count_action_curr + flag_second_row)+ " + 0.3 ")
                
            action = action[1:]
            html_act = serializeMonsterActionToNanDeck(action)
            nanDeckActions += template_monster_line_action.replace(r"${Lines_Dice}", nanDeckDice).replace(r"${Action}", html_act ).replace(r"${PosYAction}", start_actions + " + [space_text_18] * " + str(2*count_action_curr) )
            count_action_curr += 1


        template_monster_single = open('Templates/Monster_Single.txt', 'r')
        template_monster_single = template_monster_single.read()

        
        res = template_monster_single.replace(r"${LifeBox}", nanDeckLife).replace(r"${Name}", self.name).replace(r"${Passive}", nanDeckPassive).replace(r"${Actions}", nanDeckActions).replace(r"${Order}", str(order))

        return res

class EventCard:

    def __init__(self):

        self.name = ""
        
        self.upside = ""
        self.downside = ""
        self.flavour = ""

    def setName(self,n):
        self.name = n

    def setUpside(self,n):
        self.upside = n
    
    def setDownside(self,n):
        self.downside = n

 
    assignmentDict = {
        "Name":setName, #stat cards start here
        "Upside":setUpside,
        "Downside":setDownside

    }
    def serializeToNandeck(self, order):

        self.upside = self.upside.replace(";",",")
        self.downside = self.downside.replace(";",",")
        self.flavour = self.flavour.replace(";",",")

        
        template_event_single = open('Templates/Event_Single.txt', 'r')
        template_event_single = template_event_single.read()
        
        res = template_event_single.replace(r"${Order}", str(order))
        res = res.replace(r"${Upside}",str(self.upside).strip()).replace(r"${Downside}", str(self.downside).strip())
        res = res.replace(r"${Name}",str(self.name).strip()).replace(r"${Flavour}", str(self.flavour).strip())

        return res
    

class EncounterCard:
    def __init__(self):


        self.name = ""
        self.encounter = 1
        self.P1 = ""
        self.P2 = ""
        self.P3 = ""
        self.P4 = ""
        self.P5 = ""

        

    def serializeToNandeck(self, order):
        

        template_story_single = open('Templates/Story_Single.txt', 'r')
        template_story_single = template_story_single.read()

        lineups = [self.P1,self.P2,self.P3,self.P4,self.P5]
        lineups_new: list[str] = []

        for lineup in lineups:
            lineup = "Left, " + lineup + " Right"
            res = ""
            einruck = 1
            for word in lineup.split(" "):
                res += word.replace(",", "," + ("&ensp;" * einruck)) # add progressively more space
                einruck += 1 #stepsize
            lineups_new.append(res)

        res = template_story_single.replace(r"${Order}", str(order))
        res = res.replace(r"${Lineup1}",lineups_new[0].strip().replace(",", linebreakStringNanDeck_htmltext))
        res = res.replace(r"${Lineup2}",lineups_new[1].strip().replace(",", linebreakStringNanDeck_htmltext))
        res = res.replace(r"${Lineup3}",lineups_new[2].strip().replace(",", linebreakStringNanDeck_htmltext))
        res = res.replace(r"${Lineup4}",lineups_new[3].strip().replace(",", linebreakStringNanDeck_htmltext))
        res = res.replace(r"${Lineup5}",lineups_new[4].strip().replace(",", linebreakStringNanDeck_htmltext))
            
        return res