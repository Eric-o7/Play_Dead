from graphics import *
from combatant import *
from items import *

class Ability():
    def __init__(self, name, effect: str, effect_int:int, damage: range, targets: int, duration: int):
        self.effect = effect #link to a method
        self.effect_int = effect_int
        self.damage = damage #max damage or range
        self.area = targets
        self.duration = duration
    
    # def starting_abilities(self, Combatant):
    #     match Combatant.equipment["Mhand"]:
    #         case zweihander:
    #             Combatant.style_list.append(bloody_strike)
    #             Combatant.style_list.append(heavy_strike)
    #         case sword:
    #             pass
    #         case rod:
    #             pass
    #         case staff:
    #             pass
    #         case shurikens:
    #             pass
    #         case claws:
    #             pass
    
    
        
            
    def ability_effect(self):
        match Ability.effect:
            case "damage_over_time":
                self.set_damage_over_time(player, Combatant)
            case "vulnerability":
                self.vulnerability(player, Combatant)
            case "raise_avoidance":
                self.raise_avoidance(player, Combatant)
            case "raise_deflection":
                self.raise_deflection(player, Combatant)
            case "direct_damage":
                self.direct_damage(player, Combatant)
            case "automatic_hit":
                self.automatic_hit(player, Combatant)    
    
    #damage_over_time set up is Combatant.status = {"damage_over_time":{dot1:[duration,effect_int]}, {dot2:[duration, effect_int]}}
        
    def set_damage_over_time(self, victim: Combatant): #warrior bloody
        if victim.status["damage_over_time"]:
            dot_key = f"dot{len(victim.status["damage_over_time"])+1}"
            victim.status["damage_over_time"][dot_key] = [self.duration, self.effect_int]
        else:
            victim.status["damage_over_time"] = {"dot1": [self.duration, self.effect_int]}
        
    def damage_over_time(self, victim: Combatant):
        for dot in victim.status["damage_over_time"]:
            if victim.status["damage_over_time"][dot][0] > 0:
                victim.status["damage_over_time"][dot][0] -= 1
                victim.take_damage(victim.status["damage_over_time"][dot][1])
            else:
                del victim.status["damage_over_time"][dot]
        
    def vulnerability(self, user: Combatant, victim: Combatant): #ninja tear flesh
        if victim.status[self.name]:
            victim.status[self.name] -= 1
            
        victim.status[self.name] = self.duration
        
        
    def raise_avoidance(self, user: Combatant, victim: Combatant): #wizard fade, warrior defensive strike
        pass
    
    def raise_deflection(self, user: Combatant, victim: Combatant): #ninja shadow guise
        pass
    
    def direct_damage(self, user: Combatant, victim: Combatant): #firebolt #type 1 is physical, type 2 is spell damage
        pass
    
    def automatic_hit(self, user: Combatant, victim: Combatant): #ninja stealth, wizard missile barrage
        pass

class Style(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, targets: int, endurance_cost: int, duration: int, weapon_type: Item = None):
        super().__init__(name, effect, damage, targets, duration)
        self.endurance_cost = endurance_cost
    
    def use_style(self, Combatant):
        if self.endurance_cost >= Combatant.endurance:
            Combatant.use_endurance(self.endurance_cost)
            self.ability_effect()
        else:
            game_out(f"You need {self.endurance_cost} to use that style")
    
#Styles
firebolt = Style("Fire Bolt", "direct_damage", 0, 6, 1, 25, 2, staff)
tear_flesh = Style("Tear Flesh", "vulnerability", Combatant.level, 3, 1, 25, 2, claws)
lotus_bloom = Style("Lotus Bloom", "direct_damage", 0, 3, 3, 25, 1, shurikens)
arcane_pulse = Style("Arcane Pulse", "direct_damage", 0, 3, 3, 25, 2, rod)
sweeping_strike = Style("Sweeping Strike", "direct_damage", 0, 3, 3, 25, 1, zweihander)
defensive_strike = Style("Defensive Strike", "raise_avoidance", 1, 3, 1, 25, 1, sword)
stealth = Style("Stealth", "automatic_hit", 0, 0, 0, 25, 1)
heavy_strike = Style("Heavy Strike", "direct_damage", 0, 8, 1, 25, 1, zweihander)
bloody_strike = Style("Bloody Strike", "damage_over_time", 1, 6, 1, 25, Combatant.level)
fade = Style("Fade", "raise_deflection", 0, 0, 0, 25, 2)

starting_styles = {"Fire Bolt": firebolt, "Tear Flesh": tear_flesh,
                   "Lotus Bloom": lotus_bloom, "Arcane Pulse": arcane_pulse,
                   "Sweeping Strike": sweeping_strike, "Defensive Strike": defensive_strike,
                   "Stealth": stealth, "Heavy Strike": heavy_strike,
                   "Bloody Strike": bloody_strike, "Fade": fade}

class Spells(Ability):
    def __init__ (self, effect: str, maxdamage: int, targets: int, mana_cost: int):
        super().__init__(effect, maxdamage, targets)
        self.mana_cost = mana_cost     
        
#Spells

if __name__ == "__main__":
    Ability.set_damage_over_time()












