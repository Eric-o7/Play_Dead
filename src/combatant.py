from graphics import *
from maps import *
from items import *

class Combatant():
    def __init__(self, name: str, level: int, health: int,
                 player_class = None, 
                 strength=None, agility=None, 
                 acuity=None, map=None, coordinate=None,
                 spells = None, styles = None, inventory = None):
        self.name = name
        self.level = level
        self.health = health
        self.strength = strength
        self.agility = agility
        self.acuity = acuity
        self.map = tutorial.name
        self.styles = styles
        self.style_list = []
        self.spell_list = []
        self.spells = spells
        self.player_class = player_class
        self.inventory = Item.get_inventory(self)
    
    def set_playerclass(self, player_class):
        if player_class == "Warrior":
            self.strength = 10
            self.acuity = 3
            self.agility = 3
        if player_class == "Wizard":
            self.strength = 3
            self.acuity = 10
            self.agility = 3
        if player_class == "Ninja":
            self.strength = 3
            self.acuity = 3
            self.agility = 10
        self.set_health()
    
    def set_mana(self):
        self.mana = (self.acuity + self.level) * 10
    
    def set_endurance(self):
        self.endurance = (self.strength + self.level) * 10
        
    def set_speed(self):
        self.speed = (self.agility + self.level) * 10
       
    def set_health(self):
        self.health = 6 + (self.level*2) + self.strength
        if self.strength >= 10:
            self.health += self.level / 2   


                        
    def take_damage(self, damage):
        self.health -= damage

    def use_mana(self, mana_cost):
        self.mana -= mana_cost
    
    def use_endurance(self, endurance_cost):
        self.endurance -= endurance_cost
    
    def add_spell(self, spell):
        self.spell_list.append(spell)
    
    def get_spell_list(self):   
        return self.spell_list
    
    def get_styles(self):
        return self.styles
    
    def level_up(self):
        self.level+=1

if __name__ == "__main__":
    player = Combatant("bob", 1, 0, "Warrior")
    dd = Item("dagger", 1, 1.5)
    Combatant.add_to_inventory(player, dd)
    print(player.inventory)