import random
from gamestate import set_char_stats, gamestate_bus
from graphics import game_out

enemies = []
target = None
combatstate = 1
combatround = 0

def combatstate_bus(text):
    global combatstate
    match combatstate:
        case 1:
            combat_order()
        #set combat order by rolling agi + 2d6
        #clear previous ability counter dictionary
        case 2:
            player_action(text)
        #dot counters are decreased
        case 3:
            npc_action()
        case 4:
            player_target(text)
        case 5:
            extra_attack(text)
        case 6:
            check_range(text)

def combat_order(player, *args):
    global enemies
    enemies = []
    for combatant in args[0]:
        # print(combatant.name)
        combatant.initiative = None
        enemies.append(combatant)
    player.initiative = player.agility + random.randint(2,12)
    game_out(f"You rolled an initiative score of {player.initiative}!", "combat")
    for combatant in enemies:
        combatant.initiative = combatant.agility + random.randint(2,12)
        combatant.status["Extra Attack"] = 0
        game_out(f"{combatant.name} rolled an initiative score of {combatant.initiative}!", "combat")
    enemies.sort(key = lambda x: x.initiative, reverse = True)
    global combatstate
    if player.initiative > enemies[0].initiative:
        game_out(f"You go first!", "blue_bold")
        if len(enemies) == 1:
            wait_player_input()
        elif len(enemies) > 1:
            ask_player_target()
        else:
            gamestate_bus("ok")
    else:
        npc_action()
    return

def wait_player_input():
    from gamestate import player
    if player.health <= 0:
        game_out(f"You're critically wounded, enter RESTART to try again.", "blue")
        return
    if target == None:
        ask_player_target()
        return
    if ((player.player_class == "Wizard" or player.equipment["Mhand"].ranged == True)
        and player.status["ranged"] == [False, "status"]):
        ask_attack_range()
        return
    if len(enemies) >= 1:
        game_out(f"What would you like to do?", "combat_pc_question")
        game_out(f"You can ATTACK, use a style(STYLE NAME), cast a spell(SPELL NAME), or change TARGET.", "combat_pc")
        global combatstate
        combatstate = 2
    return

def ask_player_target():
    from gamestate import player
    global enemies, target, combatround
    if len(enemies) == 0:
        game_out(f"You've defeated all enemies!", "combat_pc")
        restart_combat(player, enemies)
        gamestate_bus("ok")
        return
    elif len(enemies) == 1:
        target = enemies[0]
        game_out(f"{target.name} is your target!", "combat_pc")
        # print(f" COMBAT ROUND: {combatround}")
        if combatround == 0:
            wait_player_input()
        else:
            npc_action()
        return
    game_out(f"Which enemy would you like to target?","combat_pc_question")
    for e in enemies:
        if e.player_class == None:
            game_out(f"{e.name}")
            global combatstate
            combatstate = 4
    return

def player_action(text): #combatstate 2
    from gamestate import player
    global combatround, enemies
    combatround +=1
    if text.lower() == "restart":
        restart_combat(player, enemies)
    if "damage_over_time" in player.status:
        damage_over_time(player)
    # print([style.name for style in player.styles])
    # print([spell.name for spell in player.spells])
    # if target == None:
    #     ask_player_target()
    game_out(f"{text.title()}", "combat_pc")
    if text.lower() in {"attack", "att"} and (player.equipment["Mhand"].ranged == False):
        if player.status["ranged"][0] == True:
            player.status["ranged"][0] = False
            player.set_deflection()
            game_out(f"You move back into melee range to attack.", "combat_pc")
        player.basic_attack(target)
        if target:
            ask_extra_attack()
    elif text.lower() == "attack":
        player.basic_attack(target)
        if target:
            ask_extra_attack()
    elif text.title() in [style.name for style in player.styles]:
        for style in player.styles:
            if text.title() == style.name:
                chosen_style = style
        chosen_style.use_style(player, target)
    elif text.title() in [spell.name for spell in player.spells]:
        for spell in player.spells:
            if text.title() == spell.name:
                chosen_spell = spell
        chosen_spell.use_spell(player, target)
    elif text.lower() == "target":
        ask_player_target()
    else:
        game_out(f"{text} is not a valid command, please try again.", "error")
    return

def ask_attack_range():
    game_out(f"Would you like to try to outrange the enemies to gain a bonus to deflection?", "combat_pc_question")
    global combatstate
    combatstate = 6
    
def check_range(text): #combatstate 6
    from gamestate import player
    if text.lower() not in {'yes', 'no'}:
        game_out(f"{text} is not a valid response, please enter Yes or No.", "error")
        ask_attack_range()
        return
    if text.lower() == "no":
        player.status["ranged"][1] = "no"
        wait_player_input()
        return
    for e in enemies:
        if "entangled" not in e.status and player.max_speed <= e.max_speed:
            game_out(f"You try to maneuver around your opponents but they're too quick!", "combat_pc")
            player.status["ranged"][1] = "failed"
            wait_player_input()
            return
    game_out(f"You successfully outrange your enemies, increasing your deflection by 1!", "effects")
    player.status["ranged"][0] = True
    player.set_deflection()
    wait_player_input()
    return
        
def ask_extra_attack():
    from gamestate import player
    if player.speed >= 30 and len(enemies) >= 1:
        game_out(f"Would you like to use your speed to attack again this round?", "combat_pc_question")
        global combatstate
        combatstate = 5
        return
    else:
        npc_action()
    return

def extra_attack(text):
    from gamestate import player
    if text.lower() in {"yes", "attack"}:
        player.use_speed(30)
        player.basic_attack(target)
        set_char_stats()
        ask_extra_attack()
    elif text.lower() == "no":
        npc_action()
    else:
        game_out(f"{text} is not a valid response, please enter Yes or No", "error")
    return

def player_target(text): #combatstate 4
    names = [e.name for e in enemies]
    # print(f" List of enemies {names}")
    if text.title() in names:
        for e in enemies:
            if text.title() == e.name:
                game_out(f"{text.title()} is targeted!", "combat_pc")
                global target
                target = e
                # print(combatround)
                if combatround == 0:
                    wait_player_input()
                    return
                else:
                    npc_action()
                    return
    else:
        game_out(f"Cannot find {text}, please try again!", "error") 
        return  

def npc_action():
    from graphics import game_text
    global enemies, combatstate
    #ALL ENEMIES GO
    game_out(f"Your enemies are taking a turn.", "combat_npc")
    for e in enemies:
        if "entangled" in e.status:
            e.status["entangled"][0] -= 1
            if e.status["entangled"][0] == 0:
                del e.status["entangled"]
        if "damage_over_time" in e.status:
            damage_over_time(e)
            if e.check_death():
                if len(enemies) == 0:
                    gamestate_bus("ok")
                    return
                return
        game_text.after(2000, npc_decision, e)
    if not target:
        game_text.after(3000, ask_player_target)
        return
    game_text.after(3000, wait_player_input)
    
def npc_decision(enemy): #logic affecting conditions - entangled, stealth, extra attack is its own function
    from gamestate import player
    aoe_styles = {"Lotus Bloom", "Arcane Pulse", "Sweeping Strike"}
    player_health_status = float(player.health  / player.max_health) * 100
    enemy_health_status = float(enemy.health  / enemy.max_health) * 100
    # print(f"Player health: {player_health_status}%, Enemy health: {enemy_health_status}%")
    # print(f"Enemy resources: Speed - {enemy.speed}, Endurance - {enemy.endurance}, Mana - {enemy.mana}")
    check_aoe = [style.name for style in enemy.styles if style.name in aoe_styles]
    range_difference = True if player.status["ranged"][0] == True and enemy.status["ranged"][0] == False else False
    if "stealth" in player.status:
        if len(check_aoe) > 0:
            if enemy.endurance > check_aoe[0].endurance_cost:
                check_aoe[0].use_style(enemy, player)
                del player.status["stealth"]
                return game_out(f"{enemy.name} has revealed your location using {check_aoe[0].name}", "combat_npc")
                
        else:
            return game_out(f"{enemy.name} cannot see you while you're stealthed!", "combat_npc")
        return
    elif player_health_status >= enemy_health_status:
        if enemy.endurance > enemy.mana:
            available_styles = [style for style in enemy.styles if enemy.endurance > style.endurance_cost]
            if range_difference: available_styles = [style for style in available_styles if style.ranged == True]
            # for style in available_styles:
                # print(style.name)
            if available_styles:
                random_style = random.choice(available_styles)
                random_style.use_style(enemy, player)
            else:
                npc_basic_attack(range_difference, enemy)
        else:
            available_spells = [spell for spell in enemy.spells if enemy.mana > spell.mana_cost]
            if available_spells:
                random_spell = random.choice(available_spells)
                random_spell.use_spell(enemy, player)
            else:
                # print(range_difference)
                npc_basic_attack(range_difference, enemy)
    else:
        npc_basic_attack(range_difference, enemy)
    # print(enemy.status)
    set_char_stats()
    if enemy.speed > 30 and player_health_status > enemy_health_status and enemy.status["Extra Attack"] < combatround:
        if npc_basic_attack(range_difference, enemy):
            enemy.use_speed(30)
            enemy.status["Extra Attack"] += 1
    return 
    
def npc_basic_attack(range_difference, enemy):
    from gamestate import player
    # print(f"Range Difference is {range_difference}")
    if range_difference and "entangled" in enemy.status:
        return game_out(f"{enemy.name} cannot attack while entangled.", "combat_npc")
    enemy.basic_attack(player)
    return True

def damage_over_time(combatant):
    for dot in combatant.status["damage_over_time"].copy():
        if combatant.status["damage_over_time"][dot][0] > 0:
            combatant.status["damage_over_time"][dot][0] -= 1
            combatant.health -= combatant.status["damage_over_time"][dot][1]
            game_out(f"{combatant.name} takes {combatant.status['damage_over_time'][dot][1]} damage from {combatant.status['damage_over_time'][dot][2]}", "dot")
            if combatant.status["damage_over_time"][dot][0] == 0:
                del combatant.status["damage_over_time"][dot]  
        else:
            del combatant.status["damage_over_time"][dot]
            
def restart_combat(player, enemies):
    from gamestate import player
    enemies.append(player)
    global status_conditions, target
    target = None
    status_conditions = {"damage_over_time", "entangled", "vulnerability", "raise_avoidance", "raise_deflection", "stealth"}
    for e in enemies:
        e.health = e.max_health
        e.endurance = e.max_endurance
        e.speed = e.max_speed
        e.mana = e.max_mana
        e.status["ranged"][1] = "status"
        for condition in status_conditions:
            if condition in e.status:
                del e.status[condition]
    enemies.pop()
    global combatround, combatstate
    combatstate = 1
    combatround = 0
    if len(enemies) > 0:
        combat_order(player, enemies)
    set_char_stats()
    return
    
def regenerate_resources(player):
    from gamestate import player
    player.health = player.max_health
    player.endurance = player.max_endurance
    player.speed = player.max_speed
    player.mana = player.max_mana
    player.status["ranged"][1] = "status"
    for condition in status_conditions:
        if condition in player.status:
            del player.status[condition]
    return