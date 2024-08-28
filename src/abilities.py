from main import *



class Ability():
    def __init__(self, name, effect: str, effect_int:int, damage: range, targets: int, duration: int):
        self.name = name
        self.effect = effect #identified using ability_effect() method
        self.effect_int = effect_int
        self.damage = damage #max damage or range
        self.area = targets
        self.duration = duration    
            
    def ability_effect(self, user, victim):
        match self.effect:
            case "damage_over_time":
                self.set_damage_over_time(user, victim)
            case "vulnerability":
                self.vulnerability(user, victim)
            case "raise_avoidance":
                self.raise_avoidance(user, victim)
            case "raise_deflection":
                self.raise_deflection(user, victim)
            case "direct_damage":
                self.direct_damage(user, victim)
            case "automatic_hit":
                self.automatic_hit(user, victim)   
            case "lifedraw":
                self.automatic_hit(user, victim)  
            case "reflect":
                self.automatic_hit(user, victim)
            case "resource_recover":
                self.automatic_hit(user, victim)   
    
    #damage_over_time set up is Combatant.status = {"damage_over_time":{dot1:[duration,effect_int]}, {dot2:[duration, effect_int]}}
        
    def set_damage_over_time(self, victim): #warrior bloody
        if victim.status["damage_over_time"]:
            dot_key = f"dot{len(victim.status['damage_over_time'])+1}"
            victim.status["damage_over_time"][dot_key] = [self.duration, self.effect_int]
        else:
            victim.status["damage_over_time"] = {"dot1": [self.duration, self.effect_int]}
        
    def damage_over_time(self, victim):
        for dot in victim.status["damage_over_time"]:
            if victim.status["damage_over_time"][dot][0] > 0:
                victim.status["damage_over_time"][dot][0] -= 1
                victim.take_damage(victim.status["damage_over_time"][dot][1])
            else:
                del victim.status["damage_over_time"][dot]
        
    def vulnerability(self, user, victim): #ninja tear flesh
        from combatant import Combatant
        if self.effect in victim.status:
            victim.status[self.effect][1] -= 1
            user.basic_attack(victim)
        else:
            victim.status[self.effect] = [self, (self.duration)]
            game_out(f"Vulnerability applied to {victim.name}")
            user.basic_attack(victim)
        
        
        
    def raise_avoidance(self, user): #wizard fade, warrior defensive strike
        pass
    
    def raise_deflection(self, user): #ninja shadow guise
        pass
    
    def direct_damage(self, user, victim): #effect int 1 is physical, effect int 2 is spell damage
        if user.resistance_check(victim):
            victim.take_damage(self.damage)
    
    def automatic_hit(self, user, victim): #ninja stealth, wizard missile barrage
        pass
    
    def lifedraw(self, user, vistim): #warrior lifedraw
        pass
    
    def reflect(self, user, vistim):
        pass
    
    def leave_combat(self, user, vistim):
        pass
    
    def recover_resource(self, user, vistim):
        #effect int key: 0-speed, 1-mana, 2-endurance
        pass
        

class Style(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, targets: int, duration: int, endurance_cost: int):
        super().__init__(name, effect, effect_int, damage, targets, duration)
        self.endurance_cost = endurance_cost
    
    def use_style(self, user, victim):
        print(user.name, self.name, victim.name)
        print(self.endurance_cost, user.endurance)
        if self.endurance_cost <= user.endurance:
            user.use_endurance(self.endurance_cost)
            self.ability_effect(user, victim)
            ask_extra_attack()
        else:
            game_out(f"Not enough endurance to use this style", "error")
            wait_player_input()
    
#Styles
firebolt = Style("Fire Bolt", "direct_damage", 2, 8, 1, 2, 25)
tear_flesh = Style("Tear Flesh", "vulnerability", 0, 3, 1, 2, 25)
lotus_bloom = Style("Lotus Bloom", "direct_damage", 0, 3, 3, 1, 25)
arcane_pulse = Style("Arcane Pulse", "direct_damage", 0, 3, 3, 2, 25)
sweeping_strike = Style("Sweeping Strike", "direct_damage", 0, 3, 3, 1, 25)
defensive_strike = Style("Defensive Strike", "raise_avoidance", 1, 3, 1, 1, 25)
stealth = Style("Stealth", "automatic_hit", 0, 0, 0, 25, 1)
heavy_strike = Style("Heavy Strike", "direct_damage", 0, 8, 1, 1, 5)
bloody_strike = Style("Bloody Strike", "damage_over_time", 1, 6, 1, 0, 25)
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
transfusion = Spell("Transfusion", "lifedraw", 0, 6, 1, 0, 50) #use player.level as effect int to modify damage
spell_reflect = Spell("Spell Reflect", "reflect", 0, 0, 1, 0, 25, "Warrior")
inflame_weapon = Spell("Inflame Weapon", "augment_attack", 0, 4, 1, 2, 50)
shadow_guise = Spell("Shadow Guise", "raise_deflection", 2, 0, 0, 2, 25, "Ninja") #effect int used for status counter
second_wind = Spell("Second Wind", "recover_resource", 0, 0, 0, 0, 50, "Ninja") #effect int will indicate which resource to recover
vanish = Spell("Vanish", "leave_combat", 0, 0, 0, 0, 30, "Ninja")
entangle = Spell("Entangle", "entangle", 0, 0, 1, 2, 25, "Wizard")
comet = Spell("Comet", "direct_damage", 3, 12, 4, 0, 50, "Wizard") #effect int used for area of effect damage
missile_barrage = Spell("Missile Barrage", "automatic_hit", 0, 6, 1, 0, 40, "Wizard")

starting_spells = {"Transfusion": transfusion, "Spell Reflect": spell_reflect,
                   "Inflame Weapon": inflame_weapon, "Shadow Guise": shadow_guise,
                   "Second Wind": second_wind, "Entangle": entangle, "Comet": comet, "Missile Barrage": missile_barrage}


if __name__ == "__main__":
    Ability.set_damage_over_time()












