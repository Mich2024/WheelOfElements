
#Globals
countPlayers = 3
countEnemies = 3
stratTargeting = "Leftmost"
stratsTargetingList = [
    "Leftmost",
    "LowestRight",
    "Priority",
    ]

#sta = "LowestLeft"

class Player:
    life = 18
    damage = 3
    heal = 2

class Enemy:
    life = 10
    damage = 3
    heal = 0

class Quint:
    player = Player()
    enemies = []

    def __init__(self):
        for i in range(countEnemies):
            self.enemies.append(Enemy())

class Board:
    #quints rotate tot he left, so to left is +1, tot he right is -1
    quints = []
    def __init__(self):
        for i in range(countPlayers):
            self.quints.append(Quint())
    

def takeDamage(entity, damage):
        entity.life = min(0, entity.life - damage)

#getLife #unused, no special effects


def damageEnemy(enemies: list, damage: int):
    if(stratTargeting == "Leftmost"):
        if(len(enemies)) > 0:
            takeDamage(enemies[0],damage)
            if(enemies[0].life == 0):
                enemies.remove(enemies[0])
    
    elif(stratTargeting == "LowestRight"):
        minLife = 1000
        index = -1
        for i, enemy in reversed(enumerate(enemies)):
            if enemy.life < minLife:
                minLife = enemy.life
                index = i
        if(len(enemies)) > 0:
            takeDamage(enemies[index],damage)
            if(enemies[index].life == 0):
                enemies.remove(enemies[index])
    
def damagePlayer(player: Player, damage: int):
    #### replace with status effect list ####
    #if(hasattr(player, "shield")):
    #    damage -= player.shield
    player.life -= damage

def healPlayer(player: Player, heal: int):
    player.life += heal

def rotateOut(q: Quint):
    if(len(q.enemies)>0):
        enemy = q.enemies.pop(0)
    else:
        enemy = None
    return enemy

def rotateIn(q: Quint, enemy: Enemy):
    if enemy != None:
        q.enemies.append(enemy)

def disengage(b: Board, q: Quint):
    indexFrom = Board.quints.index(q)
    indexTo = (indexFrom + 1) % len(Board.quints)

    rotateIn(Board.quints[indexTo],rotateOut(q))

def cleanup(b: Board):

    #rotate
    enemies = []
    for q in b.quints:
        enemies.append(rotateOut(q))
    enemies.insert(0, enemies.pop(-1))
    for i, enemy in enumerate(enemies):
        rotateIn(b.quints[i],enemy)
