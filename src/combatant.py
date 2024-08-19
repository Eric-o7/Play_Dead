from graphics import *
from maps import *
from items import *
from random import randint


class Combatant():
    def __init__(self, name: str, level: int, health: int,
                 player_class: str = None, strength: int = None, 
                 agility: int = None, acuity: int = None, 
                 primary_stat: str = None, avoidance: int = None,
                 resistance: int = None, deflection: int = None,  
                 map: str = None, coordinate: tuple = None,
                 spells = None, styles = None, 
                 inventory: dict = None, status: dict = None):
        self.name = name
        self.level = level
        self.health = health
        self.player_class = player_class
        self.strength = strength
        self.agility = agility
        self.acuity = acuity
        self.primary_stat = primary_stat
        self.avoidance = avoidance
        self.resistance = resistance
        self.deflection = deflection
        self.map = tutorial.name
        self.coordinate = coordinate
        self.spells = spells
        self.styles = styles
        self.style_list = []
        self.spell_list = []
        self.inventory = {}
        self.status = {}
        self.equipment = {"Mhand": None, "Ohand": None, "Armor": None}
    
    def set_playerclass(self, player_class):
        if player_class == "Warrior":
            self.strength = 10
            self.acuity = 6
            self.agility = 6
            self.primary_stat = self.strength
        if player_class == "Wizard":
            self.strength = 6
            self.acuity = 10
            self.agility = 6
            self.primary_stat = self.acuity
        if player_class == "Ninja":
            self.strength = 6
            self.acuity = 6
            self.agility = 10
            self.primary_stat = self.agility
        self.set_health()
        self.set_mana()
        self.set_endurance()
        self.set_speed()
        self.set_avoidance()
        self.set_resistance()
    
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
    
    def equip_item(self, Item):
        if isinstance(Item.slot, tuple):
            equipment_slot = Item.slot[0]
        else:
            equipment_slot = Item.slot
        stat_check = Item.stat
        #checks highest stat(str/acu/agi) of all possible options from the item
        #if item can be worn with a min 6 in str or agi, this will check the player for which is highest
        if isinstance(stat_check, tuple):
            max_stat = stat_check[0]
            for stat in stat_check:
                if self.__getattribute__(stat) >= self.__getattribute__(max_stat):
                    max_stat = stat
            stat_check = max_stat
        if self.__getattribute__(stat_check) < Item.min_stat_req:
            game_out(f"You need {Item.min_stat_req} {stat_check} to equip this item")
        elif self.equipment[equipment_slot] != None:
            game_out(f"You currently have {self.equipment[Item.slot[0]]} equipped!")
            self.unequip_item(self.equipment[Item.slot[0]])
        else:
            if isinstance(Item.slot, tuple):
                self.equipment[Item.slot[0]], self.equipment[Item.slot[1]] = Item, Item
            else:
                self.equipment[equipment_slot] = Item
            game_out(f"{Item.name} equipped!", "purple")
        if isinstance (Item, Armor):
            self.set_deflection()
            
    def unequip_item(self, Item):
        game_out(f"Would you like to replace {self.equipment[Item.slot[0]]} with {Item.name}?")
        # need to record gstate, change to a different gstate, then revert back
        # if answer is yes:
        #     self.add_to_inventory(Item)
        
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

    def set_avoidance(self):
        self.avoidance = self.agility + self.level + 4
    
    def set_resistance(self):
        self.resistance = self.acuity + self.level + 4
    
    def set_deflection(self):
        self.deflection = (self.equipment["Armor"].armor_class) / 2
    
    def attack_roll(self):
        first_die, second_die = randint(1,6), randint(1,6)
        game_out(f"Rolling 2d6 to hit:")
        game_out(f"First die rolls {first_die}")
        game_out(f"Second die rolls {second_die}")
        #2d6 plus primary stat -4 plus level
        attack_roll_result = first_die + second_die + (self.primary_stat - 5) + self.level
        return attack_roll_result
        
    def avoidance_check(self, Combatant):
        attack_roll_result = self.attack_roll()
        if attack_roll_result >= Combatant.avoidance:
            game_out(f"You hit with a {attack_roll_result}!")
            return True
        game_out(f"You miss with a {attack_roll_result}.")
        return False        
    
    def resistance_check(self, Combatant):
        attack_roll_result = self.attack_roll()
        if attack_roll_result >= Combatant.resistance:
            game_out(f"You hit with a {attack_roll_result}!")
            return True
        game_out(f"You miss with a {attack_roll_result}.")
        return False
                        
    def take_damage(self, damage, ability = None):
        if self.status[ability.effect] == "vulnerability":
            self.health -= (damage + self.status[ability.effect_int])
        else:    
            self.health -= damage

    def use_mana(self, mana_cost):
        self.mana -= mana_cost
    
    def use_endurance(self, endurance_cost):
        self.endurance -= endurance_cost
    
    def add_spell(self, spell):
        self.spell_list.append(spell)
    
    def add_style(self, style):
        self.style_list.append(style)
    
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
    
earth_golem = Combatant("Earth Golem", 1, 20, None)