import random
import abilities
import main
from graphics import game_out
from items import *
import time

class Combatant():
    combatant_list = []
    def __init__(self, name: str, level: int, health: int,
                 player_class: str = None, strength: int = None, 
                 agility: int = None, acuity: int = None, 
                 primary_stat: int = None, avoidance: int = None,
                 resistance: int = None, deflection: int = None,  
                 max_mana: int = None, max_endurance: int = None,
                 max_speed: int = None, spells: list = None, styles: list = None, 
                 inventory: dict = None, status: dict = None,
                 equipment: dict = None, base_damage: int = None,
                 initiative: int = None, max_health: int = None,
                 endurance: int = None, speed: int = None,
                 mana: int = None):
        self.name = name
        self.level = level
        self.max_health = health
        self.player_class = player_class
        self.strength = strength
        self.agility = agility
        self.acuity = acuity
        self.primary_stat = primary_stat
        self.avoidance = avoidance
        self.resistance = resistance
        self.deflection = deflection
        self.max_mana = max_mana
        self.max_endurance = max_endurance
        self.max_speed = max_speed
        self.spells = spells
        self.styles = styles
        self.inventory = []
        self.status = {"ranged": [False, "status"]}
        self.equipment = {"Mhand": None, "Ohand": None, "Armor": None}
        self.base_damage = base_damage
        self.initiative = initiative
        self.health = health
        self.endurance = endurance
        self.speed = speed
        self.mana = mana
        Combatant.combatant_list.append(self)

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
        self.max_mana = (self.acuity + self.level) * 10
        self.mana = self.max_mana
    
    def set_endurance(self):
        self.max_endurance = (self.strength + self.level) * 10
        self.endurance = self.max_endurance
        
    def set_speed(self):
        self.max_speed = (self.agility + self.level) * 10
        self.speed = self.max_speed
       
    def set_health(self):
        self.max_health = 6 + (self.level*2) + self.strength
        if self.strength >= 10:
            self.max_health += int(self.level / 2)
        self.health = self.max_health
    
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
            game_out(f"You need {Item.min_stat_req} {stat_check} to equip this item", "error")
        elif self.equipment[equipment_slot]:
            game_out(f"You currently have {self.equipment[Item.slot[0]]} equipped!", "error")
            self.unequip_item(self.equipment[Item.slot[0]])
        else:
            if isinstance(Item.slot, tuple):
                self.equipment[Item.slot[0]], self.equipment[Item.slot[1]] = Item, Item
            else:
                self.equipment[equipment_slot] = Item
            game_out(f"{Item.name} equipped!\n", "purple")
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
            game_out(f"Cannot add {Item.name} to inventory, not enough space", "error")
            
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
        if "raise_avoidance" in self.status:
            self.avoidance += self.status["raise_avoidance"][1]
        if self.equipment["Ohand"] and self.equipment["Ohand"].name == "Shield":
            self.avoidance += 1
    
    def set_resistance(self):
        self.resistance = self.acuity + self.level + 4
    
    def set_deflection(self):
        self.deflection = int((self.equipment["Armor"].deflection_rating) / 2)
        if self.status["ranged"][0] == True:
            self.deflection += 1
        if "raise_deflection" in self.status:
            self.deflection += self.status["raise_deflection"][1]
        main.set_char_stats()

#2d6 plus primary stat -4 plus level
    def attack_roll(self):
        first_die, second_die = random.randint(1,6), random.randint(1,6)
        attack_roll_result = first_die + second_die + (self.primary_stat - 5) + self.level
        return attack_roll_result
    

        
    def avoidance_check(self, Combatant):
        temp_avoidance = Combatant.avoidance
        if "stealth" in self.status and self.player_class:
            game_out(f"{self.name} automatically hits {Combatant.name} from Stealth!", "effects")
            del self.status["stealth"]
            return True
        elif "Stealth" in Combatant.status:
            game_out(f"{self.name} tries to attack but cannot see!", "error")
            return False
        if "raise_avoidance" in Combatant.status:
            Combatant.status["raise_avoidance"][0] -= 1
            if Combatant.status["raise_avoidance"][0] == 0:
                game_out(f"Bonus avoidance from {Combatant.status['raise_avoidance'][2]} ends after next attack.")
                del Combatant.status["raise_avoidance"]
                Combatant.set_avoidance()
        attack_roll_result = self.attack_roll()    
        if attack_roll_result >= temp_avoidance:
            game_out(f"{self.name} hit with a roll of {attack_roll_result} beating {Combatant.name}'s avoidance score of {Combatant.avoidance}!", "styles")
            return True
        game_out(f"{self.name} missed with a roll of {attack_roll_result} against {Combatant.name}'s avoidance score of {Combatant.avoidance}.","styles")
        return False        
    
    def resistance_check(self, Combatant):
        attack_roll_result = self.attack_roll()
        if "stealth" in self.status and self.player_class:
            game_out(f"{self.name} has come out of Stealth!", "effects")
            del self.status["stealth"]
        elif "stealth" in Combatant.status:
            game_out(f"{self.name} cannot see you!")
            return False
        if "reflect" in Combatant.status:
            pass
        if attack_roll_result >= Combatant.resistance:
            game_out(f"{self.name} hit with a roll of {attack_roll_result} beating {Combatant.name}'s resistance score of {Combatant.resistance}!", "spells")
            return True
        game_out(f"{self.name} missed with a roll of {attack_roll_result} against {Combatant.name}'s resistance score of {Combatant.resistance}.", "spells")
        return False
                        
    def take_damage(self, damage):
        from main import player, set_char_stats
        temp_deflection = self.deflection
        
        if "raise_deflection" in self.status:
            self.status["raise_deflection"][0] -= 1
            if self.status["raise_deflection"][0] == 0:
                game_out(f"Bonus deflection from {self.status['raise_deflection'][2]} has ended", "effects")
                del self.status["raise_deflection"]
                self.set_deflection()
        
        damage = damage - temp_deflection
        
        if damage < 1: damage = 0
        
        if "vulnerability" in self.status:
            self.health -= damage + player.level
            # print(f"vulnerability counter currently at {self.status['vulnerability'][1]}")
            self.status["vulnerability"][1] -= 1
            game_out(f"{self.name} takes {damage} plus {player.level} vulnerability damage for a total of {damage + player.level} damage! ({self.deflection} damage was deflected)", "damage")
            self.check_death(self.health)
            if self.status["vulnerability"][1] == 0:
                del self.status["vulnerability"]
                game_out(f"{self.name}'s vulnerability condition has ended.")
        else:
            self.health -= damage
            game_out(f"{self.name} takes {damage} damage! ({temp_deflection} damage was deflected)", "damage")
            self.check_death(self.health)
        
        if self.player_class:
            set_char_stats()
        
    def basic_attack(self, Combatant, style_damage = None):
        if style_damage:
            damage = style_damage
        elif self.player_class:
            damage = random.randint(1,(self.equipment["Mhand"].damage)) + self.level
        else:
            damage = random.randint(1,self.base_damage) + self.level
        if self.avoidance_check(Combatant):
            game_out(f"{self.name} rolled {damage} for damage", "damage")
            if "augment_attack" in self.status:
                damage += self.status["augment_attack"][1]
                game_out(f"{self.status['augment_attack'][2]} adds {self.status['augment_attack'][1]} to your damage!", "effects")
                Combatant.take_damage(damage + self.status["augment_attack"][1])
                self.status["augment_attack"][0] -= 1
                if self.status["augment_attack"][0] == 0:
                    del self.status["augment_attack"]
                    game_out(f"{self.name}'s weapon returns to its normal state.")
                return
            Combatant.take_damage(damage)
            
    def check_death(self, damage = None):
        from main import enemies
        if self.health <= 0:
            game_out(f"{self.name} was defeated!", "effects")
            if self in enemies:
                enemies.remove(self)
                main.target = None
            return True
        if self.health <= 0 and self.player_class:
            game_out(f"You're critically wounded and play dead until the threat has passed.", "blue")
            game_out(f"RESTART to try again", "blue_bold")
        
    def use_mana(self, mana_cost):
        self.mana -= mana_cost
        
    def use_speed(self, speed_cost):
        if self.speed >= speed_cost:
            self.speed -= speed_cost

    def use_endurance(self, endurance_cost):
        if self.endurance >= endurance_cost:
            self.endurance -= endurance_cost
            return True
            
    def add_spell(self, spell):
        self.spell_list.append(spell)
    
    def add_style(self, style):
        self.style_list.append(style)
    
    def get_spell_list(self):   
        return self.spells
    
    def get_styles(self):
        return self.styles
    
    def level_up(self):
        self.level+=1
        self.set_health()
        self.set_mana()
        self.set_speed()
        self.set_endurance()
        self.set_avoidance()
        self.set_resistance()
        self.primary_stat += 1
        main.set_char_stats()
        game_out(f"\nYou level up! Your primary stat and resources have increased.", "effects")

    def __repr__(self):
        print(f"Name {self.name}, max_speed {self.max_speed}, status {self.status}")
#avoidance = agility + level + 4 (2d6 + primary stat - 5 + level) 11/15
#resistance = acuity + level + 4 (2d6 + primary stat - 5 + level) to hit

#NPC MONSTERS

#Template Combatant(name= , level= , health= , player_class=None, strength= , agility= , acuity= , 
# primary_stat= , avoidance= , resistance= , deflection= , map=None, coordinate=None, max_mana= , max_endurance= , 
# max_speed= , spells=[], styles=[], inventory= , status= , equipment= , base_damage= , initiative= , max_health= , 
# endurance= , speed= , mana= , )

#max end/speed/mana = (level+stat)*10  (divide in 2 for NPC's because they will use it right away?)

snakey = Combatant(name="Snakey", level=3, health=18, player_class=None, strength=6, agility=7, acuity=10, 
primary_stat=10 , avoidance=11, resistance=15, deflection=1, max_mana=130, max_endurance=90, 
max_speed=60, spells=[abilities.comet, abilities.missile_barrage, abilities.spell_reflect], styles=[abilities.arcane_pulse, abilities.tear_flesh, abilities.envenom], inventory={}, status={"Ranged": [False, "status"]}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=4, initiative=None, max_health=18, 
endurance=90, speed=60, mana=130)

lilsnake1 = Combatant(name="Red Snake", level=1, health=6, player_class=None, strength=3, agility=7, acuity=3, 
primary_stat=7, avoidance=10, resistance=9, deflection=1, max_mana=0, max_endurance=30, 
max_speed=30, spells=[], styles=[abilities.tear_flesh, abilities.envenom], inventory={}, status={"ranged": [False, "status"]}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=2, initiative=None, max_health=6, 
endurance=30, speed=30, mana=0)

lilsnake2 = Combatant(name="Brown Snake", level=1, health=6, player_class=None, strength=3, agility=7, acuity=3, 
primary_stat=7, avoidance=10, resistance=9, deflection=1, max_mana=0, max_endurance=30, 
max_speed=30, spells=[], styles=[abilities.tear_flesh, abilities.envenom], inventory={}, status={"ranged": [False, "status"]}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=2, initiative=None, max_health=6, 
endurance=30, speed=30, mana=0)

lilsnake3 = Combatant(name="Orange Snake", level=1, health=6, player_class=None, strength=3, agility=7, acuity=3, 
primary_stat=7, avoidance=10, resistance=9, deflection=1, max_mana=0, max_endurance=30, 
max_speed=30, spells=[], styles=[abilities.tear_flesh, abilities.envenom], inventory={}, status={"ranged": [False, "status"]}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=2, initiative=None, max_health=6, 
endurance=30, speed=30, mana=0)

dire_beetle = Combatant(name="Dire Beetle", level=1, health=12, player_class=None, strength=10, agility=5, acuity=3, 
primary_stat=10, avoidance=8, resistance=12, deflection=2, max_mana=0, max_endurance=60, 
max_speed=30, spells=[], styles=[abilities.heavy_strike], inventory={}, status={"ranged": [False, "status"]}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=4, initiative=None, max_health=12, 
endurance=60, speed=30, mana=0)

fox = Combatant(name="Fox", level=3, health=30, player_class=None, strength=7, agility=12, acuity=7, 
primary_stat=12 , avoidance=14, resistance=10, deflection=2, max_mana=0, max_endurance=90, 
max_speed=120, spells=[], styles=[abilities.bloody_strike, abilities.defensive_strike], inventory={}, status={"Ranged": [False, "status"]}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=5, initiative=None, max_health=30, 
endurance=90, speed=120, mana=0)


if __name__ == "__main__":
    def print_slow(text):
        for char in text:
            print(char)
            time.sleep(.5)
    print_slow(abilities.comet.name)
    # print([style.name for style in dire_beetle.styles])