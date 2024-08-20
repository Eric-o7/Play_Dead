from graphics import *
from combatant import *
from items import *
from main import player

class Ability():
    def __init__(self, name, effect: str, effect_int:int, damage: range, targets: int, duration: int):
        self.name = name
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
            case "lifedraw":
                self.automatic_hit(player, Combatant)  
            case "reflect":
                self.automatic_hit(player, Combatant)
            case "resource_recover":
                self.automatic_hit(player, Combatant)   
    
    #damage_over_time set up is Combatant.status = {"damage_over_time":{dot1:[duration,effect_int]}, {dot2:[duration, effect_int]}}
        
    def set_damage_over_time(self, victim: Combatant): #warrior bloody
        print(victim.status)
        if victim.status["damage_over_time"]:
            dot_key = f"dot{len(victim.status['damage_over_time'])+1}"
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
    
    def lifedraw(self, user: Combatant, vistim: Combatant): #warrior lifedraw
        pass
    
    def reflect(self, user: Combatant, vistim: Combatant):
        pass
    
    def leave_combat(self, user: Combatant, vistim: Combatant):
        pass
    
    def recover_resource(self, user: Combatant, vistim: Combatant):
        #effect int key: 0-speed, 1-mana, 2-endurance
        pass
        

class Style(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, targets: int, duration: int, endurance_cost: int,  weapon_type: Item = None):
        super().__init__(name, effect, effect_int, damage, targets, duration)
        self.endurance_cost = endurance_cost
        self.weapon_type = weapon_type
    
    def use_style(self, Combatant):
        if self.endurance_cost >= Combatant.endurance:
            Combatant.use_endurance(self.endurance_cost)
            self.ability_effect()
        else:
            game_out(f"You need {self.endurance_cost} to use that style")
    
#Styles
firebolt = Style("Fire Bolt", "direct_damage", 0, 6, 1, 2, 25, staff)
tear_flesh = Style("Tear Flesh", "vulnerability", player.level, 3, 1, 2, 25,claws)
lotus_bloom = Style("Lotus Bloom", "direct_damage", 0, 3, 3, 1, 25, shurikens)
arcane_pulse = Style("Arcane Pulse", "direct_damage", 0, 3, 3, 2, 25, rod)
sweeping_strike = Style("Sweeping Strike", "direct_damage", 0, 3, 3, 1, 25, zweihander)
defensive_strike = Style("Defensive Strike", "raise_avoidance", 1, 3, 1, 1, 25, sword)
stealth = Style("Stealth", "automatic_hit", 0, 0, 0, 25, 1)
heavy_strike = Style("Heavy Strike", "direct_damage", 0, 8, 1, 1, 5, zweihander)
bloody_strike = Style("Bloody Strike", "damage_over_time", 1, 6, 1, player.level, 25)
fade = Style("Fade", "raise_deflection", 0, 0, 0, 2, 25)

starting_styles = {"Fire Bolt": firebolt, "Tear Flesh": tear_flesh,
                   "Lotus Bloom": lotus_bloom, "Arcane Pulse": arcane_pulse,
                   "Sweeping Strike": sweeping_strike, "Defensive Strike": defensive_strike,
                   "Stealth": stealth, "Heavy Strike": heavy_strike,
                   "Bloody Strike": bloody_strike, "Fade": fade}

class Spell(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, targets: int, duration: int, mana_cost: int, player_class: str = None):
        super().__init__(name, effect, effect_int, damage, targets, duration)
        self.mana_cost = mana_cost 
        
#Spells
transfusion = Spell("Transfusion", "lifedraw", player.level, 6, 1, 0, 50) #use player.level as effect int to modify damage
spell_reflect = Spell("Spell Reflect", "reflect", 0, 0, 1, 0, 25, "Warrior")
inflame_weapon = Spell("Inflame Weapon", "augment_attack", 0, 4, 1, 2, 50)
shadow_guise = Spell("Shadow Guise", "raise_deflection", 2, 0, 0, 2, 25, "Ninja") #effect int used for status counter
second_wind = Spell("Second Wind", "recover_resource", 0, 0, 0, 0, 50, "Ninja") #effect int will indicate which resource to recover
vanish = Spell("Vanish", "leave_combat", 0, 0, 0, 0, 30, "Ninja")
root = Spell("Root", "root", 0, 0, 1, 2, 25, "Wizard")
comet = Spell("Comet", "direct_damage", 3, 12, 4, 0, 50, "Wizard") #effect int used for area of effect damage
missile_barrage = Spell("Missile Barrage", "automatic_hit", 0, (6 + player.level), 1, 0, 40, "Wizard")

starting_spells = {"Transfusion": transfusion, "Spell Reflect": spell_reflect,
                   "Inflame Weapon": inflame_weapon, "Shadow Guise": shadow_guise,
                   "Second Wind": second_wind, "Root": root, "Comet": comet, "Missile Barrage": missile_barrage}


if __name__ == "__main__":
    Ability.set_damage_over_time()












