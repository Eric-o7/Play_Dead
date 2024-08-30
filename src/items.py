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
                 slot: tuple = None, damage: int = None):
        super().__init__(name, size, cost, stat, min_stat_req, slot)
        self.damage = damage
        
dagger = Weapon("Dagger", size=3, cost=3, stat=None, min_stat_req=None, slot=(("Mhand")), damage=4)
staff = Weapon("Staff", size=7, cost=10, stat="acuity", min_stat_req=10, slot=("Mhand", "Ohand"), damage=6)
sword = Weapon("Sword", size=5, cost=5, stat=("strength", "agility"), min_stat_req=7, slot=("Mhand"), damage=5)
shurikens = Weapon("Shurikens", size=1, cost=1, stat="agility", min_stat_req=7, slot=("Mhand", "Ohand"), damage=4)
shield = Weapon("Shield", size=6, cost=3, stat=("strength", "acuity", "agility"), min_stat_req=3, damage=("Ohand"))
zweihander = Weapon("Zweihander", size=14, cost=10, stat="strength", min_stat_req=10, slot=("Mhand", "Ohand"), damage=8)
rod = Weapon("Rod", size=5, cost=7, stat="acuity", min_stat_req=7, slot=("Mhand"), damage=4)
claws = Weapon("Claws", size=3, cost=10, stat="agility", min_stat_req=10, slot=("Mhand", "Ohand"), damage=5)

starting_weapons = {"Sword": sword, "Zweihander": zweihander,
           "Rod": rod, "Staff": staff,
           "Shurikens": shurikens, "Claws": claws,
           "Shield": shield, "Dagger": dagger}

class Armor(Item):
    def __init__(self, name: str, size: int, cost: float,
                 stat: str = None, min_stat_req: int = None, 
                 slot: tuple = None, deflection_rating: int = None):
        super().__init__(name, size, cost, stat, min_stat_req,
                         slot)
        self.deflection_rating = deflection_rating

tunic = Armor("Tunic", size=2, cost=1, stat=None, min_stat_req=None, slot=("Armor"), deflection_rating=0)
robe = Armor("Robe", size=3, cost=5, stat="acuity", min_stat_req=7, slot=("Armor"), deflection_rating=2)
leather_vest = Armor("Leather Vest", size=4, cost=6, stat="agility", min_stat_req=7, slot=("Armor"), deflection_rating=4)
chain_mail = Armor("Chain Mail", size=8, cost=8, stat="strength", min_stat_req=7, slot=("Armor"), deflection_rating=6)
breastplate = Armor("Breastplate", size=14, cost=18, stat="strength", min_stat_req=10, slot=("Armor"), deflection_rating=8)


armor = {"Tunic": tunic, "Robe": robe, "Leather Vest": leather_vest,
         "Chain Mail": chain_mail, "Breastplate": breastplate}
 
    

