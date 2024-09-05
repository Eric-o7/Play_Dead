import time
import random
import importlib

from graphics import root, game_out, char_stats, typing_animation

def main():
    root.mainloop()

gamestate = 1
combatstate = 1
combatround = 0

def delay(seconds):
    time.sleep(seconds)

def reset_game():
    import os, sys
    os.execl(sys.executable, *([sys.executable]+sys.argv))

def gamestate_bus(text):
    global gamestate
    if gamestate == 1:
        start_game(text)
    elif gamestate == 2:
        enter_name(text)
    elif gamestate == 3:
        choose_class(text)
    elif gamestate == 4:
        choose_equipment(text)
    elif gamestate == 5:
        choose_styles(text)
    elif gamestate == 6:
        choose_spells(text)
    elif gamestate == 7:
        wizard_spells(text)
    elif gamestate == 8:
        pass
        
def combatstate_bus(text, *args):
    if combatstate == 1:
        combat_order()
        #set combat order by rolling agi + 2d6
        #clear previous ability counter dictionary
    elif combatstate == 2:
        player_action(text)
        #dot counters are decreased automatically
    elif combatstate == 3:
        npc_action()
    elif combatstate == 4:
        player_target(text)
    elif combatstate == 5:
        extra_attack(text)
    elif combatstate == 6:
        check_range(text)


enemies = []
target = None

def combat_order(player, *args): 
    global enemies
    enemies = []
    for combatant in args[0]:
        print(combatant.name)
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
        if len(enemies) <= 1:
            combatstate = 2
            wait_player_input()
        else:
            ask_player_target()    
    else:
        npc_action()   

def player_action(text):
    global player, combatround
    combatround +=1
    if "damage_over_time" in player.status:
        damage_over_time(player)
    print([style.name for style in player.styles])
    print([spell.name for spell in player.spells])
    if target == None:
        ask_player_target()
    game_out(f"{text.title()}", "combat_pc")
    if (text.lower() == "attack" and (player.equipment["Mhand"].name != "Shurikens")
        and player.equipment["Mhand"].name != "Wand"):
        if player.status["Ranged"] == True:
            player.status["Ranged"] = False
            player.set_deflection()
            game_out(f"You move back into melee range to attack.", "combat_pc")
        player.basic_attack(target)
        ask_extra_attack()
    elif text.lower() == "attack":
        player.basic_attack(target)
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
    elif text.lower() == "play dead":
        pass
    elif text.lower() == "target":
        ask_player_target()
    else:
        game_out(f"{text} is not a valid command, please try again.", "error")

def ask_attack_range():
    game_out(f"Would you like to try to outmaneuver the enemies to gain a bonus to deflection?", "combat_pc_question")
    global combatstate
    combatstate = 6
    
def check_range(text): #combatstate 6
    global player
    if text.lower() not in {'yes', 'no'}:
        game_out(f"{text} is not a valid response, please enter Yes or No.", "error")
        ask_attack_range()
        return
    if text.lower() == "no":
        player.status["Ranged"][1] = "no"
        wait_player_input()
        return
    for e in enemies:
        if "entangled" not in e.status and player.max_speed <= e.max_speed:
            game_out(f"You try to maneuver around your opponents but they're too quick!", "combat_pc")
            player.status["Ranged"][1] = "failed"
            wait_player_input()
            return
    game_out(f"You successfully outrange your enemies, increasing your deflection by 1!", "effects")
    player.status["Ranged"][0] = True
    player.set_deflection()
    wait_player_input()
        

def ask_extra_attack():
    if player.speed >= 30:
        game_out(f"Would you like to use your speed to attack again this round?", "combat_pc_question")
        global combatstate
        combatstate = 5
        return
    else:
        npc_action()

def npc_action():
    global enemies, player
    print(f"NPC ACTION")
    #ALL ENEMIES GO
    for e in enemies:
        if "entangled" in e.status:
            e.status["entangled"][0] -= 1
            if e.status["entangled"][0] == 0:
                del e.status["entangled"]
        if "damage_over_time" in e.status:
            damage_over_time(e)
            if e.check_death():
                if len(enemies) == 0:
                    gamestate_bus()
                return
        npc_decision(e)
    wait_player_input()
    
def npc_decision(enemy): #logic affecting conditions - entangled, stealth, extra attack is its own function
    global player
    aoe_styles = {"Lotus Bloom", "Arcane Pulse", "Sweeping Strike"}
    player_health_status = float(player.health  / player.max_health) * 100
    enemy_health_status = float(enemy.health  / enemy.max_health) * 100
    print(f"Player health: {player_health_status}%, Enemy health: {enemy_health_status}%")
    print(f"Enemy resources: Speed - {enemy.speed}, Endurance - {enemy.endurance}, Mana - {enemy.mana}")
    check_aoe = [style.name for style in enemy.styles if style.name in aoe_styles]
    range_difference = True if player.status["Ranged"][0] == True and enemy.status["Ranged"][0] == False else False
    if "stealth" in player.status:
        if len(check_aoe) > 0:
            if enemy.endurance > check_aoe[0].endurance_cost:
                check_aoe[0].use_style(enemy, player)
                del player.status["stealth"]
                game_out(f"{enemy.name} has revealed your location using {check_aoe[0].name}", "combat_npc")
        else:
            return game_out(f"{enemy.name} cannot see you while you're stealthed!", "combat_npc")
    elif player_health_status > enemy_health_status:
        if enemy.endurance > enemy.mana:
            available_styles = [style for style in enemy.styles if enemy.endurance > style.endurance_cost]
            if range_difference: available_styles = [style for style in available_styles if style.ranged == True]
            for style in available_styles:
                print(style.name)
            if available_styles:
                random_style = random.choice(available_styles)
                random_style.use_style(enemy, player)
                game_out(f"{enemy.name} uses {random_style.name}!","combat_npc")
            else:
                npc_basic_attack(range_difference, enemy)
        else:
            available_spells = [spell for spell in enemy.spells if enemy.mana > spell.mana_cost]
            if available_spells:
                random_spell = random.choice(available_spells)
                random_spell.use_spell(enemy, player)
                game_out(f"{enemy.name} uses {random_spell.name}!","combat_npc")
            else:
                print(range_difference)
                npc_basic_attack(range_difference, enemy)
    print(enemy.status)
    set_char_stats()
    if enemy.speed > 30 and player_health_status > enemy_health_status and enemy.status["Extra Attack"] < combatround:
        if npc_basic_attack(range_difference, enemy):
            enemy.use_speed(30)
            enemy.status["Extra Attack"] += 1
    return 
    
def npc_basic_attack(range_difference, enemy):
    print(f"Range Difference is {range_difference}")
    if range_difference and "Entangled" in enemy.status:
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

def extra_attack(text):
    if text.lower() == "yes":
        global player
        player.use_speed(30)
        player.basic_attack(target)
        set_char_stats()
        ask_extra_attack()
    elif text.lower() == "no":
        npc_action()
    else:
        game_out(f"{text} is not a valid response, please enter Yes or No", "error")

def wait_player_input():
    if ((player.equipment["Mhand"].name == "Wand" or player.equipment["Mhand"].name == "Shurikens")
        and player.status["Ranged"] == [False, "status"]):
        ask_attack_range()
    else:
        game_out(f"What would you like to do?", "combat_pc_question")
        game_out(f"You can ATTACK, use a style(STYLE NAME), cast a spell(SPELL NAME), change TARGET, attempt to PLAY DEAD.", "combat_pc")
        global combatstate
        combatstate = 2

def ask_player_target():
    global enemies, target
    if len(enemies) == 0:
        game_out(f"You've defeated all enemies!", "combat_pc")
    if len(enemies) == 1:
        target = enemies[0]
        game_out(f"{target.name} is your target!", "combat_pc")
        wait_player_input()
        return
    game_out(f"Which enemy would you like to target?","combat_pc_question")
    for e in enemies:
        if e.player_class == None:
            game_out(f"{e.name}")
            global combatstate
            combatstate = 4

def player_target(text): #combatstate 4
    names = [e.name for e in enemies]
    if text.title() in names:
        for e in enemies:
            if text.title() == e.name:
                game_out(f"{text.title()} is targeted!", "combat_pc")
                global target
                target = e
                wait_player_input()
    else:
        game_out(f"Cannot find {text}, please try again!", "error")    
        

def narrative_read(identifier:str, tag = "blue"):
    with open("text_files/narrative.txt") as narrative:
        narrative = narrative.readlines()
    count = 0
    beginning = f"***{identifier}Start***"
    end = f"***{identifier}End***"
    section = []
    for line in narrative:
        if beginning in line:
            section.append(count)
        if end in line:
            section.append(count)
        count += 1
    for line in narrative[section[0]+1:section[1]]:
        game_out(line, tag)

        
def start_game(text):
    if text.lower() == "start":
        narrative_read("Intro")
        typing_animation("Now rise, you white dog, and tell us your name!", "blue_bold")
        global gamestate
        gamestate = 2
        
def enter_name(text):
    if 1 < len(text) < 13:
        game_out(f"\nWhat a wonderful name, {text.capitalize()}!", "purple_bold")
        global char_name 
        char_name = text.capitalize()
        #Choose class prompt
        narrative_read("ClassDesc")
        typing_animation(f"Choose your class - ", "blue_bold")
        global gamestate
        gamestate = 3
    else:
        game_out(f"{text} is an invalid name. Please enter a name between 2 and 12 characters in length", "error")

def set_char_stats():
    if player:
        char_stats.set(f""" Player Info \n\n\n {player.name}\n the\n {player.player_class}\n
Level: {player.level}\n
Health: {player.health} / {player.max_health}
Mana: {player.mana} / {player.max_mana}
End: {player.endurance} / {player.max_endurance}
Speed: {player.speed} / {player.max_speed}\n 
Deflection: {player.deflection} 
Avoidance: {player.avoidance} 
Resistance: {player.resistance}""")      
        
def choose_class(text):
    from combatant import Combatant
    from items import pinecone_mail, leafrobe, snakeweave
    player_class = text.capitalize()
    if player_class not in {"Warrior", "Ninja", "Wizard"}:
        game_out(f"That is not a valid option, please try entering the name of your class again!", "error")
    else:
        global player
        player = Combatant(char_name, 1, 0, player_class, styles=[], spells=[])
        player.set_playerclass(player_class)
        game_out(f"You are now {player.name} the {player.player_class} 'possum!\n", "purple_bold")
        game_out(f"Put this on, {player.player_class}", "blue")
        if player.player_class == "Warrior":
            player.equip_item(pinecone_mail)
        elif player.player_class == "Wizard":
            player.equip_item(leafrobe)
        elif player.player_class == "Ninja":
            player.equip_item(snakeweave)
        set_char_stats()
        #Choose equipment prompt
        narrative_read(f"{player_class}Weps")
        typing_animation(f"Choose your starting weapon - ", "blue_bold")
        global gamestate
        gamestate = 4
        
def choose_equipment(text):
    from items import starting_weapons, shield
    item_name = text.capitalize()
    if item_name not in starting_weapons:
        game_out(f"That is not a valid option, please try again!", "error")
    item = starting_weapons[item_name]
    player.equip_item(item)
    if item.name in {"Sword", "Rod"}:
        player.equip_item(shield)
        player.set_avoidance()
    narrative_read(item.name)
    typing_animation(f"Choose a style to start with - ", "blue_bold")
    #Choose styles prompt
    global gamestate
    gamestate = 5
    

def choose_styles(text):
    from abilities import starting_styles
    style_name = text.title()
    if style_name not in starting_styles:
        game_out(f"That is not a valid option, please try again!", "error")
    style_choice = starting_styles[style_name]
    if len(player.styles) < 1:
        player.styles.append(style_choice)
        game_out(f"You have learned {style_choice.name}!\n", "purple")
    else:
        game_out(f"You've already chosen a style!", "error")
    narrative_read(f"{player.player_class}Spells")
    if player.player_class != "Wizard":
        typing_animation(f"You're almost ready for your first trial. Choose a spell to start with.", "blue_bold")
    if player.player_class == "Wizard":
        typing_animation(f"You're almost ready for your first trial. Choose two spells to start with.", "blue_bold")
    global gamestate
    gamestate = 6
    

def choose_spells(text):
    from abilities import starting_spells
    spell_name = text.title()
    if spell_name not in starting_spells:
        game_out(f"That is not a valid option, please try again!", "error")
    spell_choice = starting_spells[spell_name]
    player.spells.append(spell_choice)
    game_out(f"\n{spell_choice.name} has been added to your list of spells.", "purple")
    global gamestate
    if player.player_class == "Wizard":
        gamestate = 7
    else:
        gamestate = 8
        opening_combat()
    
def wizard_spells(text):
    from abilities import starting_spells
    spell_name = text.title()
    if spell_name not in starting_spells:
        game_out(f"That is not a valid option, please try again!", "error")
    spell_choice = starting_spells[spell_name]
    if spell_choice not in player.spells:
        player.spells.append(spell_choice)
        game_out(f"{spell_choice.name} has been added to your list of spells.", "purple")
        global gamestate
        gamestate = 8
        opening_combat()
    else:
        game_out(f"{spell_choice.name} is already in your list of spells!", "error")

def opening_combat():
    from combatant import dire_beetle
    game_out(f"\n{char_name}, your {player.player_class} is ready for combat!\n", "combat")
    game_out(f"\nTest your new abilities against a Dire Beetle!\n", "purple_bold")
    combat_order(player, [dire_beetle])
        

def post_tutorial_combat(text):
    pass
#read from narrative - 


def restart_combat():
    enemies.append(player)
    status_conditions = {"damage_over_time", "entangled", "vulnerability", "raise_avoidance", "raise_deflection", "stealth", "reflect"}
    for e in enemies:
        e.health = e.max_health
        e.endurance = e.max_endurance
        e.speed = e.max_speed
        e.mana = e.max_mana
        e.status["Ranged"][1] = "status"
        for condition in status_conditions:
            if condition in e.status:
                del e.status[condition]
    enemies.pop()
    global combatround, combatstate
    combatstate = 1
    combatround = 0
    print([enemy.name for enemy in enemies])
    combat_order(player, enemies)
    set_char_stats()
    
    

if __name__ == "__main__":        
    main()