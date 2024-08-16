from graphics import root, game_out, game_text
import time
from combatant import *
import items




def main():
    root.mainloop()

gamestate = 1
combatstate = 1

def gamestate(text):
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
        gamestate7(text)
    elif gamestate == 8:
        gamestate8(text)
        
def combatstate():
    if combatstate == 1:
        combat_order()
        #set combat order by comparing speed
        #clear previous ability counter dictionary
        #create new ability counter dictionary {pc_name:[counter1, counter2], npc_name:[counter1, counter2]}
    elif combatstate == 2:
        take_turn_pc()
        #counters are decreased
    elif combatstate == 3:
        take_turn_npc()
        #counters are decreased
    elif combatstate == 4:
        eval_pc_turn()
        #counters are set up
    elif combatstate == 5:
        eval_npc_turn()
        #counters are set up

def set_combat_counter():
    pass
        
        
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
        with open("text_files/narrative.txt") as class_desc:
            class_desc = class_desc.readlines()
        count = 0
        beginning = "***ClassDescStart***"
        end = "***ClassDescEnd***"
        section = []
        for line in class_desc:
            if beginning in line:
                section.append(count)
            if end in line:
                section.append(count)
            count += 1
        for line in range(section[0]+1, section[1]):
            game_out(class_desc[line], "blue")
        global gamestate
        gamestate = 3
    else:
        game_out(f"Please enter a name between 2 and 12 characters in length")


def choose_class(text):
    player_class = text.capitalize()
    if player_class not in {"Warrior", "Ninja", "Wizard"}:
        game_out(f"That is not a valid option, please try entering the name of your class again!")
    else:
        game_out(text)
        global player
        player = Combatant(char_name, 1, 0, player_class)
        player.set_playerclass(player_class)
        game_out(f"You are {player.name} the {player.player_class}!\n", "purple_bold")
        game_out(f"Have some armor {player.name}!", "blue")
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
        with open("text_files/narrative.txt") as equipment:
            equipment = equipment.readlines()
        count = 0
        beginning = f"***{player_class}WepsStart***"
        end = f"***{player_class}WepsEnd***"
        section = []
        for line in equipment:
            if beginning in line:
                section.append(count)
            if end in line:
                section.append(count)
            count += 1
        for line in range(section[0]+1, section[1]):
            game_out(equipment[line], "blue")
        game_out(f"Enter the words in capital letters to make your selection")
        global gamestate
        gamestate = 4
        
def choose_equipment(text):
    item_name = text.capitalize()
    if item_name not in {"Sword", "Zweihander",
                        "Rod", "Staff",
                        "Shurikens", "Claws"}:
        game_out(f"That is not a valid option, please try again!")
    item = weapons[item_name]
    player.equip_item(item)
    if item.name in {"Sword", "Rod"}:
        player.equip_item(shield)
    print(player.equipment)
    #Choose styles prompt
    global gamestate
    gamestate = 5
    

def choose_styles(text):
    pass

def choose_spells(text):
    pass

def gamestate7(text):
    pass

def gamestate8(text):
    pass     

if __name__ == "__main__":        
    main()