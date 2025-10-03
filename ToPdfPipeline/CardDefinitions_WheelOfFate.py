def nothing(kwargs):
        return

def removeColons(line):
    res = line.replace(":","")
    return res

def texifyMultSign(line):
    
    
    line = line.replace('*',r" $\times $ ")
    return line

symbolDict = {
    
    #"L":r"\symLoot", Mechanic removed from game
    "E":r"\symEnergy",
    "Energy":r"\symEnergy",
    "A":r"\symAttack",
    "R":r"\symRange",
    "Ranged":r"\symRange",
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

    # Banes
    "Curse":r"\symCurse",
    "Disadvantage":r"\symDisadvantage",
    "Muddle":r"\symDisadvantage",
    "Confuse":r"\symConfuse",
    "Vulnerable":r"\symVulnerable",
    "Wounded":r"\symWound",
    "Wound":r"\symWound",
    "Trauma":r"\symTrauma",
    "Stun":r"\symStun",
    "Cripple":r"\symCripple",
    "Disarm":r"\symDisarm",
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
    "Stun":r"\symStun",
    "Cripple":r"\symCripple",
    "Disarm":r"\symDisarm",
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
                    
                        res += " " + symbolDict[word.split(":")[0]] + "~" + word + " "
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
                res += "~" + parts[0] 
                if len(parts) == 2:
                    res += ":~" + parts[1]
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

        "Exhaust":appendModifier,
        "Unrecoverable":appendModifier,

        "Fire":appendAction,
        "Earth":appendAction,
        "Metal":appendAction,
        "Water":appendAction,
        "Wood":appendAction,
        
    }

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

    def serializeToNandeck(self, order):
        

        template_line_mod = open('Templates/Tableau_Line_Mod.txt', 'r')
        template_line_mod = template_line_mod.read()

        self.L1R1 = template_line_mod.replace(r"${Mod}", '"' + self.L1R1.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
        self.L1R1 = self.L1R1.replace(r"${Order}",str(order)).replace(r"${Hor}",str(0)).replace(r"${Vert}",str(0))
        self.L1R2 = template_line_mod.replace(r"${Mod}", '"' + self.L1R2.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
        self.L1R2 = self.L1R2.replace(r"${Order}",str(order)).replace(r"${Hor}",str(1)).replace(r"${Vert}",str(0))
        self.L1R3 = template_line_mod.replace(r"${Mod}", '"' + self.L1R3.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
        self.L1R3 = self.L1R3.replace(r"${Order}",str(order)).replace(r"${Hor}",str(2)).replace(r"${Vert}",str(0))
        self.L1R4 = template_line_mod.replace(r"${Mod}", '"' + self.L1R4.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
        self.L1R4 = self.L1R4.replace(r"${Order}",str(order)).replace(r"${Hor}",str(3)).replace(r"${Vert}",str(0))

        self.L2R1 = template_line_mod.replace(r"${Mod}", '"' + self.L2R1.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
        self.L2R1 = self.L2R1.replace(r"${Order}",str(order)).replace(r"${Hor}",str(0)).replace(r"${Vert}",str(1))
        self.L2R2 = template_line_mod.replace(r"${Mod}", '"' + self.L2R2.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
        self.L2R2 = self.L2R2.replace(r"${Order}",str(order)).replace(r"${Hor}",str(1)).replace(r"${Vert}",str(1))

        self.L3R1 = template_line_mod.replace(r"${Mod}", '"' + self.L3R1.replace("Add", r"\13\Add").replace("Remove", r"\13\Remove") + '"')
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

    def setLife(self, l):
        self.life = l
    
    assignmentDict = {
        "Life":setLife, #stat cards start here
    }
    #%Input: name, tier, stats, passive, skills
    def serializeToLatex(self):
        res = r"\statusCard"
        res += "{" + self.name + "}"
        res += "{" + str(self.rank) + "}"
        res += "{" 
        res += symbolDict["Life"] + r"\hspace{0.0cm} Life: " + str(self.life) + r"\\ "
        res += "}"
        res += "{" + self.passive + "}"
        res += "{" + self.modifierUpgrades + r" \\ "
        #for line in self.explanations:
        #    res += line + r" \\ "  + dictExplanation[line.split(":")[1]] + r" \\" 
        for line in self.elements:
            res += line
        res += r"} "
        res += "\n"
        return res

    def serializeToNandeck(self, order):
        
        if isinstance(self.tableau, tableauRace):

            
            template_line_life = open('Templates/Tableau_Line_Life.txt', 'r')
            template_line_life = template_line_life.read()
            template_line_passive = open('Templates/Tableau_Line_Passive.txt', 'r')
            template_line_passive = template_line_passive.read()
            template_line_lore = open('Templates/Tableau_Line_Lore.txt', 'r')
            template_line_lore = template_line_lore.read()
            template_race = open('Templates/Tableau_Race_Single.txt', 'r')
            template_race = template_race.read()

            
            lines_mods = self.tableau.serializeToNandeck(order)
            

            template_line_life = template_line_life.replace(r"${Order}",str(order)).replace(r"${Life}",self.life)
            template_line_passive = template_line_passive.replace(r"${Order}",str(order)).replace(r"${Passive}",self.passive)
            template_line_lore = template_line_lore.replace(r"${Order}",str(order)).replace(r"${Lore}",self.lore)
            template_race = template_race.replace(r"${Order}",str(order)).replace(r"${Race}", self.name )
            res = template_race.replace(r"${Mods}", lines_mods).replace(r"${Life}",template_line_life).replace(r"${Passive}",template_line_passive).replace(r"${Explanation}",template_line_lore)

        else:
            title = self.name + " " + str(self.rank)
            templateShingle = open('Templates/Shingle_Class_Card.txt', 'r')
            templateShingle = templateShingle.read()

            res = templateShingle.replace(r"${Order}", str(order)).replace(r"${Title}",title).replace(r"${Life}", str(self.life)).replace(r"${Passive}", self.passive)

        return res
    
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
        #print(self.actions)
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

class ItemCard:

    def __init__(self):

        self.name = ""
        
        self.pips = -1
        self.text = ""

        self.exhaust = False
        self.armoutNeg = False
        self.cost = "-1"
        self.quantity = 2
        self.slot = "Bagpack"
        self.level = "0"
        self.amourType = ""
        self.amourDurability = ""

    def setName(self,n):
        self.name = n

    def setLevel(self,n):
        self.level = n
    
    def setCost(self,n):
        self.cost = n

    def setQuantity(self,n):
        n = n.split(":")[1]
        try:
            self.quantity = int(n)
        except:
            print(n, " is not an integer for item quant")

    def setSlot(self,n):
        self.slot = n

    def setPips(self,n):
        n = n.split(":")[1]
        try:
            self.pips = int(n)
        except:
            print(n, " is not an integer for item pips")

    def setExhaust(self,n):
        self.exhaust = True

    def setArmourNeg(self,n):
        self.armoutNeg = True

    def setText(self,n):
        self.text = n

    def setAmour(self,n):
        try:
            amourType, dura = n.split(":")
            self.amourType += amourType
            self.amourDurability += dura

        except Exception as ex:
            print("Broken armour" + ex)
        self.text = n
 
    assignmentDict = {
        "Name":setName, #stat cards start here
        "Cost":setCost,
        "Quantity":setQuantity,
        "Quant":setQuantity,
        "Slot":setSlot,
        "Pips":setPips,
        "exhaust":setExhaust,
        "Exhaust":setExhaust,
        "ArmourNegative":setArmourNeg,
        "Cloth":setAmour,
        "Leather":setAmour,
        "Metal":setAmour,


    }
    #%Input: name, tier, stats, passive, skills
    def serializeToLatex(self):

        res = r"\itemCard"
        res += r"{\raggedright " + self.name + r" \hfill "
        res += "}"
        res += "{" + self.cost.split(":")[1] + r"~G}"
        

        pipcommand = ""
        if(self.pips != -1):
            #{Pips3}
            pipcommand = r"\symPipItem{Pips" + str(self.pips) + "}"
            if not self.amourType == "":
                pipcommand += r" \\ "

        if not self.amourType == "":   
            pipcommand = r"\symPipItem{" + self.amourType + self.amourDurability + "}"

        res += "{" + pipcommand + "}"

        
        if(self.text.strip() == ""):
            self.text = " ~ "
        res += "{" + self.text + "}"

        res += "{"
        if self.exhaust:
            res += r"\symExhaust "
        if self.armoutNeg:
            res += r"\symArmourNeg "
        res += r" \hfill \symSlot" + self.slot.split(":")[1]
        res += r"\\ "

        res += self.level + " "
        res += r"\hfill "
        res += "Quantity: " + str(self.quantity) + " "

        res += "}"
        res += "\n"


        resQuantMod = ""
        #print(self.quantity)
        for i in range(self.quantity):
            resQuantMod += res
        return resQuantMod