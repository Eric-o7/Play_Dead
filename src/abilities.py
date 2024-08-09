from graphics import *
from combatant import *
from items import *



class Abilities():
    def __init__(self, effect: str, damage: int, targets: int, area: int = None, area_shape: str = None):
        self.effect = effect #link to a method
        self.damage = damage
        self.area = area
    
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
            
                 
        
        
        
    def bleed(self): #warrior bloody
        pass
    
    def vulnerability(self): #ninja tear flesh
        pass
    
    def raise_avoidance(self): #wizard shield, warrior defensive strike, ninja shadow guise
        pass
    
    def multiple_targets(self): #ninja lotus bloom, wizard arcane pulse, warrior sweeping strike
        pass
    
    def direct_damage(self): #firebolt
        pass
       

class Spells(Abilities):
    def __init__ (self, effect: str, damage: int, area: int, mana_cost: int):
        super().__init__(effect, damage, area)
        self.mana_cost = mana_cost     
        
        
class Style(Abilities):
    def __init__ (self, effect: str, damage: int, area: int, endurance_cost: int):
        super().__init__(effect, damage, area)
        self.endurance_cost = endurance_cost
        

firebolt = Style("direct_damage", )

