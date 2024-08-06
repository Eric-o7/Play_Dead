from graphics import *
from combatant import *

class Item():
    def __init__(self, name: str, size: int, cost: float):
        self.name = name
        self.size = size
        self.cost = cost
        self.inventory = {}
        
    def total_cost(self):
        return self.cost * self.quantity
    
    #inventory format: {name:[size, cost, quantity]}        
    def get_inventory(self):
        pass
    
    def add_to_inventory(self, Combatant):
        print(self.inventory_size(Combatant))
        if self.inventory_size(Combatant):
            self.inventory[self.name] = [self.size, self.cost, 1]
            print(f"{self.name} added to Inventory!")
        else:
            print(f"Inventory is full")
    
    def inventory_size(self, Combatant):
        sum = 0
        if len(self.inventory):
            for property in self.inventory.keys():
                print(f"we here")
                print(f"{property[0]} {property[2]}")
                #muiltiplies size and quantity of all items in inventory
                sum += property[0] * property[2]
        if sum + self.size < Combatant.health:
            return
        
class Equipment(Item):
    def __init__(self, name: str, size: int, cost: float, 
                 slot: str, stat: str, min_stat_req: int):
        super().__init__(name, size, cost)
        self.slot = slot
        self.stat = stat
        self.min_stat_req = min_stat_req
    
    def equippable(self):
        pass

if __name__ == "__main__":
    player = Combatant("bob", 1, 0, "Warrior")
    dd = Item("dagger", 1, 1.5)
    dd.add_to_inventory(player)
    print(player.inventory)