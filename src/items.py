from graphics import *
from combatant import *

class Item():
    def __init__(self, name: str, size: int, cost: float,
                 stat = None, min_stat_req: int = None, 
                 slot: tuple = None, style_class: str = None):
        self.name = name
        self.size = size
        self.cost = cost
        self.stat = stat
        self.min_stat_req = min_stat_req
        self.slot = slot

dagger = Item("Dagger", 3, 3, None, None, (("Mhand")))
staff = Item("Staff", 7, 10, "acuity", 10, ("Mhand", "Ohand"))
sword = Item("Sword", 5, 5, ("strength", "agility"), 5, (("Mhand")))
shurikens = Item("Shurikens", 1, 1, "agility", 7, ("Mhand", "Ohand"))
shield = Item("Shield", 6, 3, ("strength", "acuity", "agility"), 3, ("Ohand"))
zweihander = Item("Zweihander", 14, 10, "strength", 10, ("Mhand", "Ohand"))
rod = Item("Rod", 5, 7, "acuity", 7, ("Mhand"))
claws = Item("Claws", 3, 10, "agility", 10, ("Mhand", "Ohand"))

weapons = {"Sword": sword, "Zweihander": zweihander,
           "Rod": rod, "Staff": staff,
           "Shurikens": shurikens, "Claws": claws,
           "Shield": shield, "Dagger": dagger}

tunic = Item("Tunic", 2, 1, None, None, ("Armor"))
robe = Item("Robe", 3, 5, "acuity", 7, ("Armor"))
leather_vest = Item("Leather Vest", 4, 6, "agility", 7, ("Armor"))
chain_mail = Item("Chain Mail", 8, 8, "strength", 7, ("Armor"))
breastplate = Item("Breastplate", 14, 18, "strength", 10, ("Armor"))


armor = {"Tunic": tunic, "Robe": robe, "Leather Vest": leather_vest,
         "Chain Mail": chain_mail, "Breastplate": breastplate}
 
    

