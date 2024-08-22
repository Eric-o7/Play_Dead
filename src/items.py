from graphics import *

class Item():
    def __init__(self, name: str, size: int, cost: float,
                 stat = None, min_stat_req: int = None, 
                 slot: tuple = None):
        self.name = name
        self.size = size
        self.cost = cost
        self.stat = stat
        self.min_stat_req = min_stat_req
        self.slot = slot

class Weapon(Item):
    def __init__(self, name: str, size: int, cost: float,
                 stat = None, min_stat_req: int = None, 
                 slot: tuple = None, style_class: str = None):
        super().__init__(name, size, cost, stat, min_stat_req, slot)
        self.style_class = style_class
        
dagger = Weapon("Dagger", 3, 3, None, None, (("Mhand")))
staff = Weapon("Staff", 7, 10, "acuity", 10, ("Mhand", "Ohand"))
sword = Weapon("Sword", 5, 5, ("strength", "agility"), 7, (("Mhand")))
shurikens = Weapon("Shurikens", 1, 1, "agility", 7, ("Mhand", "Ohand"))
shield = Weapon("Shield", 6, 3, ("strength", "acuity", "agility"), 3, ("Ohand"))
zweihander = Weapon("Zweihander", 14, 10, "strength", 10, ("Mhand", "Ohand"))
rod = Weapon("Rod", 5, 7, "acuity", 7, ("Mhand"))
claws = Weapon("Claws", 3, 10, "agility", 10, ("Mhand", "Ohand"))

starting_weapons = {"Sword": sword, "Zweihander": zweihander,
           "Rod": rod, "Staff": staff,
           "Shurikens": shurikens, "Claws": claws,
           "Shield": shield, "Dagger": dagger}

class Armor(Item):
    def __init__(self, name: str, size: int, cost: float,
                 stat: str = None, min_stat_req: int = None, 
                 slot: tuple = None, armor_class: int = None):
        super().__init__(name, size, cost, stat, min_stat_req,
                         slot)
        self.armor_class = armor_class

tunic = Armor("Tunic", 2, 1, None, None, ("Armor"), 0)
robe = Armor("Robe", 3, 5, "acuity", 7, ("Armor"), 2)
leather_vest = Armor("Leather Vest", 4, 6, "agility", 7, ("Armor"), 4)
chain_mail = Armor("Chain Mail", 8, 8, "strength", 7, ("Armor"), 6)
breastplate = Armor("Breastplate", 14, 18, "strength", 10, ("Armor"), 8)


armor = {"Tunic": tunic, "Robe": robe, "Leather Vest": leather_vest,
         "Chain Mail": chain_mail, "Breastplate": breastplate}
 
    

