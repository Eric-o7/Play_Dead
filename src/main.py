from graphics import root, game_out, game_text
import time
from combatant import *
import items




def main():
    root.mainloop()

gstate = 1
 
def gamestate(text):
    if gstate == 1:
        gamestate1(text)
    elif gstate == 2:
        gamestate2(text)
    elif gstate == 3:
        gamestate3(text)
    elif gstate == 4:
        gamestate4(text)
    elif gstate == 5:
        gamestate5(text)
    elif gstate == 6:
        gamestate6(text)
    elif gstate == 7:
        gamestate7(text)
    elif gstate == 8:
        gamestate8(text)
        
        
def gamestate1(text):
    if text.lower() == "start":
        game_out(text.capitalize())
        game_out("Enter character name:", "blue_bold")
        global gstate
        gstate = 2
        
def gamestate2(text):
    if 1 < len(text) < 13:
        game_out(text)
        game_out(f"Welcome, {text.capitalize()}!", "purple_bold")
        global char_name 
        char_name = text.capitalize()
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
        global gstate
        gstate = 3
    else:
        game_out(f"Please enter a name between 2 and 12 characters in length")


def gamestate3(text):
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
        global gstate
        gstate = 4
        
def gamestate4(text):
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
    global gstate
    gstate = 5
    

def gamestate5(text):
    pass

def gamestate6(text):
    pass

def gamestate7(text):
    pass

def gamestate8(text):
    pass     

if __name__ == "__main__":        
    main()