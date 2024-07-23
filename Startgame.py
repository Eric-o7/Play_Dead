class Combatant():
    def __init__(self, name, health, mana):
        self.name = name
        self.health = health
        self.mana = mana

    def take_damage(self, damage):
        self.health -= damage

    def use_mana(self, mana_cost):
        self.mana -= mana_cost

class PlayerCharacter(Combatant):
    def __init__(self, level, spells=None):
        super().__init__()
        self.level = level
        self.styles = []
        self.spell_list = []
        self.spells = spells

    def add_spell(self, spells):
        self.spell_list.append(self.spells)
    
    def get_spell_list(self):   
        return self.spell_list
    
    def get_styles(self):
        return self.styles
    
    def level_up(self):
        self.level+=1
    

class Paladin(PlayerCharacter):
    def __init__(self, holy_power):
        super().__init__()
        self.holy_power = holy_power
        
class Sorcerer(PlayerCharacter):
    def __init__(self, sorcery):
        super().__init__()
        self.sorcery = sorcery

class Abilities():
    def __init__(self, effect, damage):
        self.effect = effect
        self.damage = damage.

class Spells(Abilities):
    
class Styles(Abilities):
    
    

def main():
    print('Welcome to StartGame! \nStartGame is a text based role-playing game.\nProceed through the game by typing in an answer to the programs questions. \nResponses are case sensitive.')
    Start_Game_Prompt()
def Start_Game_Prompt():
    Ready_Start = input('Start Game? \nYes or No \n')
    if Ready_Start == 'Yes' or Ready_Start == "YES":
        player = PlayerCharacter()
        create_character()
    quit

def create_character():
    char_class = input('Do you want to play a SORCERER or PALADIN?\n')
    if char_class == "PALADIN":
        create_paladin()
    elif char_class == "SORCERER":
        create_sorcerer()
    else:
        char_class = input('Do you want to play a SORCERER or PALADIN?\n')

def create_paladin():
    spell_list = input('Select your first spell.\nHoly Word - Strong damage to undead creature \nRepent - Mild damage to any creature')
    

def create_sorcerer():
    pass
main()