#Import modules
from AI_methods import *

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
        estimated_attacks = int(total_energy/200 + 0.5);

        attack_canidates = [];

        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                c = game.game_map[pos]

                if c.attack_cost < me.energy and c.owner != game.uid and c.position not in my_attack_list:# and len(me.cells) < 95:
                    cmd_list.append(game.attack(pos, c.attack_cost))
                    print("We are attacking ({}, {}) with {} energy".format(pos.x, pos.y, c.attack_cost))
                    game.me.energy -= c.attack_cost
                    my_attack_list.append(c.position)

        result = game.send_cmd(cmd_list)
        print(result)
