from graphics import *
from combatant import *
from items import *



class Abilities():
    def __init__(self, name, effect: str, damage: range, targets: int, targets: int = None, area_shape: str = None):
        self.effect = effect #link to a method
        self.damage = damage
        self.area = targets
    
    def starting_abilities(self, Combatant):
        match Combatant.equipment["Mhand"]:
            case zweihander:
                pass #add sweeping strikes and bloody strike
            case sword:
                pass
            case rod:
                pass
            case staff:
                pass
            case shurikens:
                pass
            case claws:
                pass
            
                 

        
        
        
    def damage_over_time(self, effect_function_arg, user: Combatant, victim: Combatant): #warrior bloody
        #set up new counter
        pass
    
    def vulnerability(self, effect_function_arg, user: Combatant, victim: Combatant): #ninja tear flesh
        #set up new counter
        #add counter to combatstate (could be a dictionary of counters?)
        pass
    def raise_avoidance(self, effect_function_arg, user: Combatant, victim: Combatant): #wizard fade, warrior defensive strike
        pass
    
    def raise_deflection(self, effect_function_arg, user: Combatant, victim: Combatant): #ninja shadow guise
        pass
    
    def direct_damage(self, effect_function_arg, user: Combatant, victim: Combatant): #firebolt #type 1 is physical, type 2 is spell damage
        pass
    
    def automatic_hit(self, effect_function_arg, user: Combatant, victim: Combatant): #ninja stealth, wizard missile barrage
        pass

class Style(Abilities):
    def __init__ (self, name, effect: str, maxdamage: int, targets: int, endurance_cost: int, effect_function_arg: int = None, weapon_type: Item = None):
        super().__init__(name, effect, maxdamage, targets)
        self.endurance_cost = endurance_cost
        
#Styles
firebolt = Style("Fire Bolt", "direct_damage", 6, 1, 25, 2, staff)
tear_flesh = Style("Tear Flesh", "vulnerability", 3, 1, 25, 2, claws)
lotus_bloom = Style("Lotus Bloom", "direct_damage", 3, 3, 25, 1, shurikens)
arcane_pulse = Style("Arcane Pulse", "direct_damage", 3, 3, 25, 2, rod)
sweeping_strike = Style("Sweeping Strike", "direct_damage", 3, 3, 25, 1, zweihander)
defensive_strike = Style("Defensive Strike", "raise_avoidance", 3, 1, 25, 1, sword)
stealth = Style("Stealth", "automatic_hit", 0, 0, 25, 1)
heavy_strike = Style("Heavy Strike", "direct_damage", 6, 1, 25, 1, zweihander)
bloody_strike = Style("Bloody Strike", "damage_over_time", 4, 1, 25, player.level)
fade = Style("Fade", "raise_deflection", 0, 0, 25, 2)

class Spells(Abilities):
    def __init__ (self, effect: str, maxdamage: int, targets: int, mana_cost: int):
        super().__init__(effect, maxdamage, targets)
        self.mana_cost = mana_cost     
        
#Spells














