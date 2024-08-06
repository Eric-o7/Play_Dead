from graphics import *
from combatant import *

class Abilities():
    def __init__(self, effect: str, damage: int, area: int):
        self.effect = effect
        self.damage = damage
        self.area = area

class Spells(Abilities):
    def __init__ (self, effect: str, damage: int, area: int, mana_cost: int):
        super().__init__(effect, damage, area)
        self.mana_cost = mana_cost
        
        
        
        
class Styles(Abilities):
    def __init__ (self, effect: str, damage: int, area: int, endurance_cost: int):
        super().__init__(effect, damage, area)
        self.endurance_cost = endurance_cost