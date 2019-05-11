#Import modules

from colorfight import Colorfight
import time
import random
import AI_methods
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

#Setup
game = Colorfight()
game.connect(room = 'Potato_Chips')

userAI = 'chipsAI'
passAI = 'chippy'

if game.register(username = userAI, password = passAI, join_key="chips"):
    while True:
        #command list to send
        cmd_list = []
        #attacks
        my_attack_list = []
        #get latest info
        game.update_turn()

        #make sure you are in the game
        if game.me == None:
            continue

        me = game.me

        total_energy = me.energy;
        estimated_attacks = total_energy/200;

        attack_canidates = [];

        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                c = game.game_map[pos]

                if c.attack_cost < me.energy and c.owner != game.uid and c.position not in my_attack_list and len(me.cells) < 95:
                    if c.natural_energy > 5 or c.natural_gold > 5:
                        addToCanidates(attack_canidates, pos, c)
