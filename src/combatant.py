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
        self.inventory = {}
        self.equipment = {"Lhand": None, "Rhand": None, "Armor": None, }
    
    def set_playerclass(self, player_class):
        if player_class == "Warrior" or "warrior":
            self.strength = 10
            self.acuity = 3
            self.agility = 3
        if player_class == "Wizard" or "wizard":
            self.strength = 3
            self.acuity = 10
            self.agility = 3
        if player_class == "Ninja" or "ninja":
            self.strength = 3
            self.acuity = 3
            self.agility = 10
        else:
            game_out(f"That is not a valid option, please try entering the name of your class again!")
        self.set_health()
        self.set_mana()
        self.set_endurance()
        self.set_speed()
    
    def set_mana(self):
        self.mana = (self.acuity + self.level) * 10
    
    def set_endurance(self):
        self.endurance = (self.strength + self.level) * 10
        
    def set_speed(self):
        self.speed = (self.agility + self.level) * 10
       
    def set_health(self):
        self.health = 6 + (self.level*2) + self.strength
        if self.strength >= 10:
            self.health += int(self.level / 2)   

#inventory format {item.name: [item.size, item.cost, item.quantity]}
    def add_to_inventory(self, Item):
        inventory_size, space_left = self.inventory_size(Item)
        if inventory_size >= 0 and space_left == True:
            if Item.name in self.inventory.keys():
                self.inventory[Item.name][2] += 1
            else:
                self.inventory[Item.name] = [Item.size, Item.cost, 1]
            game_out(f"{Item.name} added to Inventory!")
            game_out(f"Inventory Space Remaining {inventory_size}")
        else:
            game_out(f"Cannot add {Item.name} to inventory, not enough space")
            
    def inventory_size(self, Item):
        sum = 0
        if len(self.inventory):
            for property in self.inventory.keys():
                #multiplies size[property][0] and quantity[property][2] of all items in inventory
                sum += self.inventory[property][0] * self.inventory[property][2]
        remaining_inventory = self.health - (sum + Item.size)
        if remaining_inventory < 0:
            remaining_inventory = self.health - sum
            return remaining_inventory, False
        return remaining_inventory, True

                        
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
    player = Combatant("bob", 1, 30, "Warrior")
    dd = Item("Dagger", 27, 1.5)
    ddd = Item("Dagger", 5, 1.5)
    dddd = Item("Dagger", 2, 1.5)
    twohandsword = Item("zweihander", 15, 5)
    player.add_to_inventory(dd)
    player.add_to_inventory(ddd)
    player.add_to_inventory(dddd)
    print(player.inventory)