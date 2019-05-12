from AI_methods import *

# Create a Colorfight Instance. This will be the object that you interact
# with.
game = Colorfight()

# Connect to the server. This will connect to the public room. If you want to
# join other rooms, you need to change the argument
game.connect(room = 'test-run1')
# game.connect(room = 'public')
userAI = 'chipsAI'
passAI = 'chippy'

# game.register should return True if succeed.
# As no duplicate usernames are allowed, a random integer string is appended
# to the example username. You don't need to do this, change the username
# to your ID.
# You need to set a password. For the example AI, the current time is used
# as the password. You should change it to something that will not change
# between runs so you can continue the game if disconnected.
if game.register(username = userAI, password = passAI):#, join_key="chips"):
    # This is the game loop
    while True:
        # The command list we will send to the server
        cmd_list = []
        # The list of cells that we want to attack
        my_attack_list = []
        # update_turn() is required to get the latest information from the
        # server. This will halt the program until it receives the updated
        # information.
        # After update_turn(), game object will be updated.
        game.update_turn()

        cheap_tiles = []

        # Check if you exist in the game. If not, wait for the next round.
        # You may not appear immediately after you join. But you should be
        # in the game after one round.
        if game.me == None:
            continue

        me = game.me
        has_house = False

        # game.me.cells is a dict, where the keys are Position and the values
        # are MapCell. Get all my cells.
        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                # Get the MapCell object of that position
                c = game.game_map[pos]
                cheap_tiles.append(c)
                # Attack if the cost is less than what I have, and the owner
                # is not mine, and I have not attacked it in this round already
                # We also try to keep our cell number under 100 to avoid tax

                    # cmd_list.append(game.attack(pos, c.attack_cost))
                    # print("We are attacking ({}, {}) with {} energy".format(pos.x, pos.y, c.attack_cost))
                    # game.me.energy -= c.attack_cost
                    # my_attack_list.append(c.position)

            # If we can upgrade the building, upgrade it.
            # Notice can_update only checks for upper bound. You need to check
            # tech_level by yourself.
            if cell.owner == me.uid and cell.building.name=="home":
                has_house = True

            if cell.building.can_upgrade and \
                    (cell.building.is_home or cell.building.level < me.tech_level) and \
                    cell.building.upgrade_gold < me.gold and \
                    cell.building.upgrade_energy < me.energy:
                if len(me.cells) < 500 or me.gold > 100_000:
                    cmd_list.append(game.upgrade(cell.position))
                    print("We upgraded ({}, {})".format(cell.position.x, cell.position.y))
                    me.gold   -= cell.building.upgrade_gold
                    me.energy -= cell.building.upgrade_energy

            # Build a random building if we have enough gold
            if cell.owner == me.uid and not cell.building.is_empty and me.gold >= 100:
                if cell.building.name != "fortress" and nearEnemy(cell,game):
                    building = BLD_FORTRESS
                    cmd_list.append(game.build(cell.position, building))
                    print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
                    me.gold -= 100
            if cell.owner == me.uid and cell.building.is_empty and me.gold >= 100:
                building = None
                if nearEnemy(cell,game):
                    building = BLD_FORTRESS
                elif len(me.cells) < 200:
                    building = random.choice([BLD_GOLD_MINE,BLD_ENERGY_WELL,BLD_ENERGY_WELL,BLD_ENERGY_WELL])
                else:
                    building = BLD_GOLD_MINE
                cmd_list.append(game.build(cell.position, building))
                print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
                me.gold -= 100


        if not has_house:
            building = BLD_HOME
            cmd_list.append(game.build(list(me.cells.keys())[0], building))
            print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
            me.gold -= 100
        cheap_tiles.sort(key=(lambda a:a.attack_cost))#,reverse=True)
        k = 0
        while True:
            if k>=len(cheap_tiles):
                break
            c = cheap_tiles[k]
            if c.attack_cost < me.energy and c.owner != game.uid \
                    and c.position not in my_attack_list:
                    # and len(me.cells) < 95:
                cmd_list.append(game.attack(c.position, c.attack_cost))
                my_attack_list.append(c.position)
                print("We are attacking ({}, {}) with {} energy".format(c.position.x, c.position.y, c.attack_cost))
                me.energy -= c.attack_cost
            k+=1
        cheap_tiles = []
        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)
