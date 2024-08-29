from graphics import root, game_out, char_stats
import time
from combatant import *
from random import randint

def main():
    root.mainloop()

gamestate = 1
combatstate = 1

def delay(seconds):
    time.sleep(seconds)

def gamestate_bus(text):
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
        tutorial_combat(text)
        
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
    for combatant in args:
        combatant.initiative = None
        enemies.append(combatant)
    player.initiative = player.agility + randint(2,12)
    game_out(f"You rolled an initiative score of {player.initiative}!")
    for combatant in enemies:
        combatant.initiative = combatant.agility + randint(2,12)
        game_out(f"{combatant.name} rolled an initiative score of {combatant.initiative}!")
    enemies.sort(key = lambda x: x.initiative, reverse = True)
    global combatstate
    if player.initiative > enemies[0].initiative:
        game_out(f"You go first!")
        if len(enemies) <= 1:
            combatstate = 2
            wait_player_input()
        else:
            ask_player_target()    
    else:
        npc_action()      

def player_action(text):
    global player
    game_out(text)
    if target == None:
        ask_player_target()
    game_out(f"{text}")
    if (text.lower() == "attack" and (player.player_class == "Wizard" or
        player.player_class == "Warrior")):
        if player.status["Ranged"] == True:
            player.status["Ranged"] = False
            player.set_deflection()
            game_out(f"You move back into melee range to attack.")
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
        ask_extra_attack()
    elif text.title() == [spell.name for spell in player.spells]:
        for spell in player.spells:
            if text.title() == spell.name:
                chosen_spell = spell
        chosen_spell.ability_effect(player, target)
        ask_extra_attack()
    elif text.lower() == "play dead":
        pass
    elif text.lower() == "target":
        ask_player_target()
    else:
        game_out(f"{text} is not a valid command, please try again.", "error")

def ask_attack_range():
    game_out(f"Would you like to try to outmaneuver the enemies to gain a bonus to deflection?")
    game_out(f"Respond with YES or NO")
    global combatstate
    combatstate = 6
    
def check_range(text): #combatstate 6
    global player
    if text.lower() not in {'yes', 'no'}:
        game_out(f"{text} is not a valid response, please enter Yes or No.", "error")
    if text.lower() == "no":
        wait_player_input()
        return
    for e in enemies:
        if "entangled" not in e.status and player.max_speed <= e.max_speed:
            game_out(f"You try to maneuver around your opponents but they're too quick!")
            wait_player_input()
            return
    game_out(f"You successfully outrange your enemies, increasing your deflection by 1!")
    player.status["Ranged"] = True
    player.set_deflection()
    wait_player_input()
        

def ask_extra_attack():
    if player.speed >= 30:
        game_out(f"Would you like to use your speed to attack again this round?")
        game_out(f"Respond with YES or NO")
        global combatstate
        combatstate = 5
    else:
        npc_action()

def npc_action():
    global enemies, player
    print(f"NPC ACTION")
    #ALL ENEMIES GO
    for e in enemies:
        if "damage_over_time" in e.status:
            damage_over_time(e)
            e.check_death()
        e.basic_attack(player)
    set_char_stats()
    wait_player_input()
    
def damage_over_time(enemy):
    for dot in enemy.status["damage_over_time"]:
        if enemy.status["damage_over_time"][dot][0] > 0:
            enemy.status["damage_over_time"][dot][0] -= 1
            enemy.health -= enemy.status["damage_over_time"][dot][1]
            game_out(f"{enemy.name} takes {enemy.status['damage_over_time'][dot][1]} damage from {enemy.status['damage_over_time'][dot][2]}")
        else:
            del enemy.status["damage_over_time"][dot]

def extra_attack(text):
    if text.lower() == "yes":
        global player
        player.use_speed(30)
        player.basic_attack(target)
        ask_extra_attack()
    elif text.lower() == "no":
        npc_action()
    else:
        game_out(f"{text} is not a valid response, please enter Yes or No", "error")

def wait_player_input():
    print(f"Player Main hand {player.equipment['Mhand']}")
    print(f"Player Status {player.status}")
    if ((player.player_class == "Wizard" or player.equipment["Mhand"].name == "Shurikens")
        and player.status["Ranged"] == False):
        ask_attack_range()
    else:
        game_out(f"What would you like to do?", "blue")
        game_out(f"You can ATTACK, use a style(STYLE NAME), cast a spell(SPELL NAME), change TARGET, attempt to PLAY DEAD.")
        global combatstate
        combatstate = 2

def ask_player_target():
    global enemies, target
    if len(enemies) == 0:
        game_out(f"You've defeated all enemies!")
    if len(enemies) == 1:
        target = enemies[0]
        game_out(f"{target.name} is your target!")
        wait_player_input()
        return
    game_out(f"Which enemy would you like to target?", "blue")
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
                game_out(f"{text.title()} is targeted!")
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
    for line in range(section[0]+1, section[1]):
        game_out(narrative[line], tag)
        
def start_game(text):
    if text.lower() == "start":
        game_out(text.capitalize())
        #Enter name prompt
        game_out("Enter character name:", "blue_bold")
        global gamestate
        gamestate = 2
        
def enter_name(text):
    if 1 < len(text) < 13:
        game_out(text)
        game_out(f"Welcome, {text.capitalize()}!", "purple_bold")
        global char_name 
        char_name = text.capitalize()
        #Choose class prompt
        narrative_read("ClassDesc")
        global gamestate
        gamestate = 3
    else:
        game_out(f"Please enter a name between 2 and 12 characters in length", "error")

def set_char_stats():
    if player:
        char_stats.set(f""" Character Stats \n\n\n {player.name}\n the\n {player.player_class}\n
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
    player_class = text.capitalize()
    if player_class not in {"Warrior", "Ninja", "Wizard"}:
        game_out(f"That is not a valid option, please try entering the name of your class again!", "error")
    else:
        game_out(text)
        global player
        player = Combatant(char_name, 1, 0, player_class)
        player.set_playerclass(player_class)
        game_out(f"You are {player.name} the {player.player_class}!\n", "purple_bold")
        game_out(f"Have some armor, {player.name}!", "blue")
        if player.player_class == "Warrior":
            player.equip_item(chain_mail)
        elif player.player_class == "Wizard":
            player.equip_item(robe)
        elif player.player_class == "Ninja":
            player.equip_item(leather_vest)
        set_char_stats()
        #Choose equipment prompt
        game_out(f"Choose your starting weapon:\n", "blue_bold")
        narrative_read(f"{player_class}Weps")
        game_out(f"Enter the words in capital letters to make your selection.")
        global gamestate
        gamestate = 4
        
def choose_equipment(text):
    item_name = text.capitalize()
    if item_name not in starting_weapons:
        game_out(f"That is not a valid option, please try again!", "error")
    item = starting_weapons[item_name]
    player.equip_item(item)
    if item.name in {"Sword", "Rod"}:
        player.equip_item(shield)
        player.set_avoidance()
    game_out(f"Based on your weapon choice, choose a starting style.", "blue_bold")
    #Choose styles prompt
    narrative_read(item.name)
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
        game_out(f"You have learned {style_choice.name}!", "purple")
    else:
        game_out(f"You've already chosen a style!", "error")
    if player.player_class != "Wizard":
        game_out(f"Your character is almost complete! Choose a spell to start with.", "blue_bold")
    if player.player_class == "Wizard":
        game_out(f"Your character is almost complete! Choose two spells to start with.", "blue_bold")
    narrative_read(f"{player.player_class}Spells")
    global gamestate
    gamestate = 6
    

def choose_spells(text):
    from abilities import starting_spells
    from combatant import snakey
    spell_name = text.title()
    if spell_name not in starting_spells:
        game_out(f"That is not a valid option, please try again!", "error")
    spell_choice = starting_spells[spell_name]
    player.spells.append(spell_choice)
    game_out(f"{spell_choice.name} has been added to your list of spells.", "blue")
    global gamestate
    if player.player_class == "Wizard":
        gamestate = 7
    else:
        game_out(f"{char_name}, your {player.player_class} is ready for combat!", "purple")
        gamestate = 8
        combat_order(player, snakey)
    
def wizard_spells(text):
    from abilities import starting_spells
    from combatant import snakey
    spell_name = text.title()
    if spell_name not in starting_spells:
        game_out(f"That is not a valid option, please try again!", "error")
    spell_choice = starting_spells[spell_name]
    if spell_choice not in player.spells:
        player.spells.append(spell_choice)
        game_out(f"{spell_choice.name} has been added to your list of spells.", "blue")
        game_out(f"{char_name}, your {player.player_class} is ready for combat!", "purple")
        global gamestate
        gamestate = 8
        combat_order(player, snakey)
    else:
        game_out(f"{spell_choice.name} is already in your list of spells!", "error")

def tutorial_combat(text):
    pass
        

def gamestate8(text):
    pass     




if __name__ == "__main__":        
    main()