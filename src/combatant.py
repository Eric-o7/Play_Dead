from graphics import *
from maps import Maps

class Combatant():
    def __init__(self, name, level, health, 
                 strength=None, agility=None, 
                 acuity=None, map=None, coordinate=None):
        self.name = name
        self.level = level
        self.health = health
        self.strength = strength
        self.agility = agility
        self.acuity = acuity
        self.mana = (self.acuity + self.level) * 10
        self.endurance = (self.strength + self.level) * 10
        self.speed = (self.agility + self.level) * 10
        self.map = Maps(name)
        
    def set_health(self, strength):
        self.health = 6 + (self.level*2) + strength
        if self.strength >= 10:
            self.health += self.level / 2
        
        
    def take_damage(self, damage):
        self.health -= damage

    def use_mana(self, mana_cost):
        self.mana -= mana_cost

class PlayerCharacter(Combatant):
    def __init__(self, level, spells=None, styles = None):
        super().__init__()
        self.level = level
        self.styles = styles
        self.style_list = []
        self.spell_list = []
        self.spells = spells

    def add_spell(self, spell):
        self.spell_list.append(spell)
    
    def get_spell_list(self):   
        return self.spell_list
    
    def get_styles(self):
        return self.styles
    
    def level_up(self):
        self.level+=1

class Fighter(PlayerCharacter):
    def __init__(self):
        super().__init__()
        self.health = self.set_health()
        self.strength = 10
        self.agility = 3
        self.acuity = 3
        

