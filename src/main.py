from graphics import root, game_out, game_text
import time
from combatant import *

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
        npc_action(*args)
    elif combatstate == 4:
        player_target(text)


enemies = []

def combat_order(player, *args): 
    global enemies
    enemies = []
    for combatant in args:
        combatant.initiative = None
        enemies.append(combatant)
    player.initiative = player.agility + randint(2,12)
    game_out(f"You got an initiative score of {player.initiative}!")
    for combatant in enemies:
        combatant.initiative = combatant.agility + randint(2,12)
        game_out(f"{combatant.name} got an initiative score of {combatant.initiative}!")
    enemies.sort(key = lambda x: x.initiative, reverse = True)
    global combatstate
    if player.initiative > enemies[0].initiative:
        game_out(f"You go first!")
        if len(enemies) <= 1:
            combatstate = 2
            wait_player_input()
        else:
            game_out(f"Which enemy would you like to target?", "blue")
            for e in enemies:
                if e.player_class == None:
                    game_out(f"{e.name}")
                    print(f"{e.name}")
                    combatstate = 4
    else:
        combatstate = 3       

def player_action(text):
    if text.lower() == "attack":
        pass
    elif text.lower() == "style":
        pass
    elif text.lower() == "spell":
        pass
    elif text.lower() == "flee":
        pass
    else:
        game_out(f"{text} is not a valid command, please try again.", "error")

def npc_action():
    if enemies > 2:
        pass
    #BOTH ENEMIES GO OR FIND another way to rotate with multiple enemies?
    for e in enemies:
        pass
        #set up ATTACK METHOD

def wait_player_input():
    game_out(f"What would you like to do?", "blue")
    game_out(f"You can ATTACK, use a STYLE, cast a SPELL, change TARGET, or attempt to FLEE.")

def player_target(text):
    names = [e.name for e in enemies]
    if text.title() in names:
        game_out(f"{text.title()} is targeted!")
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


def choose_class(text):
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
        if player:
            char_stats.set(f""" Character Stats \n\n\n {player.name}\n the\n {player.player_class}\n
Level: {player.level}\n
Health: {player.health} 
Mana: {player.mana}
Endurance: {player.endurance} 
Speed: {player.speed}\n 
Strength: {player.strength} 
Acuity: {player.acuity} 
Agility: {player.agility}""")
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
    if len(player.style_list) < 1:
        player.style_list.append(style_choice)
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
    spell_name = text.title()
    if spell_name not in starting_spells:
        game_out(f"That is not a valid option, please try again!", "error")
    spell_choice = starting_spells[spell_name]
    player.spell_list.append(spell_choice)
    game_out(f"{spell_choice.name} has been added to your list of spells.", "blue")
    global gamestate
    if player.player_class == "Wizard":
        gamestate = 7
    else:
        game_out(f"{char_name}, your {player.player_class} is ready for combat!", "purple")
        gamestate = 8
        combat_order(player, earth_golem, mud_golem)
    
def wizard_spells(text):
    from abilities import starting_spells
    spell_name = text.title()
    if spell_name not in starting_spells:
        game_out(f"That is not a valid option, please try again!", "error")
    spell_choice = starting_spells[spell_name]
    if spell_choice not in player.spell_list:
        player.spell_list.append(spell_choice)
        game_out(f"{spell_choice.name} has been added to your list of spells.", "blue")
        game_out(f"{char_name}, your {player.player_class} is ready for combat!", "purple")
        global gamestate
        gamestate = 8
        combat_order(player, earth_golem, mud_golem)
    else:
        game_out(f"{spell_choice.name} is already in your list of spells!", "error")

def tutorial_combat(text):
    pass
        

def gamestate8(text):
    pass     




if __name__ == "__main__":        
    main()