from colorfight import Colorfight
import time
import random
import bisect
from colorfight.constants import BLD_HOME,BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

# TODO: this method needs to add
def addToCanidates(array, cell, game):
    if(len(array) > 5):
        for i in array:
            pass
    else:
        array.append(cell)

def cost(array):
    total_energy = 0
    for cell in array:
        total_energy += cell.attack_cost
    return total_energy

def nearEnemy(cell, game):
    for n in cell.position.get_surrounding_cardinals():
        c = game.game_map[n]
        if c.owner != game.me.uid and c.building.name != "empty":
            return True
        for nn in c.position.get_surrounding_cardinals():
            cc = game.game_map[nn]
            if cc.owner != game.me.uid and cc.building.name != "empty":
                return True
    return False
