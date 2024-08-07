from graphics import root, game_out, game_text
import time
from combatant import *
import items

gstate = 1

def main():
    root.mainloop()
    
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
    if text.lower() == "play":
        game_out(text.capitalize())
        game_out("Enter character name:", "output")
        global gstate
        gstate = 2
        
def gamestate2(text):
    if 1 < len(text) < 13:
        game_out(text)
        game_out(f"Welcome, {text.capitalize()}!", "title")
    else:
        game_out(f"Please enter a name between 2 and 12 characters in length")
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
        game_out(class_desc[line], "output2")
    global gstate
    gstate = 3      

def gamestate3(text):
    player_class = text.capitalize()
    global player
    player = Combatant(char_name, 1, 0, player_class)
    player.set_playerclass(player_class)
    game_out(f"You are {player.name} the {player.player_class}!", "title")
    if player:
        char_stats.set(f""" Character Stats \n\n\n Name: {player.name}\n\n\n Level: {player.level}\n\n Health: {player.health}\n Mana: {player.mana}\n Endurance: {player.endurance}\n Speed: {player.speed}\n\n Strength: {player.strength}\n Acuity: {player.acuity}\n Agility: {player.agility}\n""")
    game_out(f"Choose your starting weapon:", "output")

def gamestate4(text):
    pass

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