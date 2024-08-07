from graphics import *
from combatant import *

class Item():
    def __init__(self, name: str, size: int, cost: float,
                 stat = None, min_stat_req: int = None, slot = None):
        self.name = name
        self.size = size
        self.cost = cost
        self.stat = stat
        self.min_stat_req = min_stat_req
        
    def __repr__(self):
        game_out(f"{Item.name}, Stat Required {Item.min_stat_req} {Item.stat}")

dagger = Item("Dagger", 3, 3, None, None, "Mhand")
staff = Item("Staff", 7, 10, "acuity", 10, ("Mhand", "Ohand"))
sword = Item("Sword", 5, 5, ("strength", "agility"), 5, "Mhand")
shurikens = Item("Shuriken", 1, 1, "agility", 7, "Mhand")
buckler = Item("Buckler", 6, 3, None, "Ohand")
zweihander = Item("Zweihander", 10, 10, "strength", 10, ("Mhand, Ohand"))
rod = Item("Rod", 5, 7, "acuity", 7, "Mhand")
claws = Item("Claws", 3, 10, "agility", 10, ("Mhand, Ohand"))

weapons = {}
 
    

