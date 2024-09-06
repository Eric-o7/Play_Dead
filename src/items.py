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
                 slot: tuple = None, damage: int = None, ranged: bool = None):
        super().__init__(name, size, cost, stat, min_stat_req, slot)
        self.damage = damage
        self.ranged = ranged
        
dagger = Weapon("Dagger", size=3, cost=3, stat=None, min_stat_req=None, slot=(("Mhand")), damage=4, ranged=False)
staff = Weapon("Staff", size=7, cost=10, stat="acuity", min_stat_req=10, slot=("Mhand", "Ohand"), damage=8, ranged=False)
bowie_knife = Weapon("Knife", size=5, cost=5, stat=("strength", "agility"), min_stat_req=7, slot=("Mhand"), damage=5, ranged=False)
shurikens = Weapon("Shurikens", size=1, cost=1, stat="agility", min_stat_req=7, slot=("Mhand", "Ohand"), damage=4, ranged=True)
shield = Weapon("Shield", size=6, cost=3, stat=("strength", "acuity", "agility"), min_stat_req=3, slot=("Ohand"))
hatchet = Weapon("Hatchet", size=14, cost=10, stat="strength", min_stat_req=10, slot=("Mhand", "Ohand"), damage=10, ranged=False)
wand = Weapon("Wand", size=5, cost=7, stat="acuity", min_stat_req=7, slot=("Mhand"), damage=4, ranged=True)
claws = Weapon("Claws", size=3, cost=10, stat="agility", min_stat_req=10, slot=("Mhand", "Ohand"), damage=6, ranged=False)

starting_weapons = {"Knife": bowie_knife, "Hatchet": hatchet,
           "Wand": wand, "Staff": staff,
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
leafrobe = Armor("Leaf-patched Robe", size=3, cost=5, stat="acuity", min_stat_req=7, slot=("Armor"), deflection_rating=0)
snakeweave = Armor("Snakeweave", size=4, cost=6, stat="agility", min_stat_req=7, slot=("Armor"), deflection_rating=2)
pinecone_mail = Armor("Pinecone Mail", size=8, cost=8, stat="strength", min_stat_req=7, slot=("Armor"), deflection_rating=4)
barkplate = Armor("Barkplate", size=14, cost=18, stat="strength", min_stat_req=10, slot=("Armor"), deflection_rating=6)


armor = {"Tunic": tunic, "Leaf-patched Robe": leafrobe, "Snakeweave": snakeweave,
         "Pinecone Mail": pinecone_mail, "Barkplate": barkplate}
 
    

