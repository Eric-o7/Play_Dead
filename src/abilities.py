from random import randint
from graphics import game_out
import main

class Ability():
    ability_list = []
    def __init__(self, name, effect: str, effect_int:int, damage: range, duration: int, ranged:bool):
        self.name = name
        self.effect = effect #identified using ability_effect() method
        self.effect_int = effect_int
        self.damage = damage #max damage or range
        self.duration = duration
        self.ranged = ranged
        Ability.ability_list.append(self)    
            
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
            case "stealth":
                self.stealth(user, victim)   
            case "lifedraw":
                self.lifedraw(user, victim)  
            case "recover_resource":
                self.recover_resource(user, victim)
            case "multi_target_damage":
                self.multi_target_damage(user, victim)
            case "entangle":
                self.entangle(user, victim)   
            case "augment_attack":
                self.augment_attack(user, victim)
            case "guaranteed_hit":
                self.guaranteed_hit(user, victim)
    
    #damage_over_time set up is Combatant.status = {"damage_over_time":{dot1:[duration,effect_int]}, {dot2:[duration, effect_int]}}
        
    def set_damage_over_time(self, user, victim): #warrior bloody
        if self.effect in victim.status:
            dot_key = f"dot{len(victim.status['damage_over_time'])+1}"
            victim.status[self.effect][dot_key] = [self.duration, self.effect_int, self.name]
        else:
            victim.status[self.effect] = {"dot1": [self.duration, self.effect_int, self.name]}
        game_out(f"Damage over time effect applied to {victim.name}", "dot")
        if self.name == "Bloody Strike":
            user.basic_attack(victim)
        
    def vulnerability(self, user, victim): #ninja tear flesh
        if self.effect in victim.status:
            victim.status[self.effect][1] -= 1
            user.basic_attack(victim)
        else:
            victim.status[self.effect] = [self, (self.duration)]
            game_out(f"Vulnerability applied to {victim.name}")
            user.basic_attack(victim)
        
    def raise_avoidance(self, user, victim): #warrior defensive strike
        user.status["raise_avoidance"] = [self.duration, self.effect_int, self.name]
        user.set_avoidance()
        main.set_char_stats()
        game_out(f"{user.name} uses {self.name} to increase avoidance for {self.duration} attacks", "effects")
        if self.damage:
            user.basic_attack(victim, self.damage)
    
    def raise_deflection(self, user, victim): #ninja shadow guise
        user.status["raise_deflection"] = [self.duration, self.effect_int, self.name]
        user.set_deflection()
        main.set_char_stats()
        game_out(f"{user.name}'s deflection is increased for {self.duration} attacks", "effects")
        if self.damage:
            user.basic_attack(victim, self.damage)
    
    def direct_damage(self, user, victim): #effect int 1 is physical, effect int 2 is spell damage
        if self.effect_int == 2 and user.resistance_check(victim):
            victim.take_damage(self.damage)
        elif self.effect_int == 1 and user.avoidance_check(victim):
            victim.take_damage(self.damage)
        else:
            game_out(f"{self.name} missed {victim.name}!")
        if self.name == "Comet":
            self.multi_target_damage(user, victim)
    
    def stealth(self, user, victim): #ninja stealth, wizard missile barrage
        user.status[self.effect] = True
        game_out(f"You are stealthed! Enemies cannot see you! Stealth will break if you attack, use a spell, or use a style to harm an enemy", "effects")
        game_out(f"Your next attack or style is guaranteed to hit", "effects")
    
    def lifedraw(self, user, victim): #warrior transfusion
        total_life = randint(1, 6) + user.level
        if victim.health == victim.max_health and user.player_class:
            user.use_mana(-50)
            game_out(f"Your opponent must be wounded before you can draw their life.", "error")
            return main.wait_player_input()
        if user.resistance_check(victim):
            game_out(f"{user.name} stole {total_life} health from {victim.name}!", "damage")
        else:
            total_life //= 2
            game_out(f"{self.name} was partially resisted. {user.name} stole {total_life} health from {victim.name}!", "blue")
        user.health += total_life
        victim.health -= total_life
    
    def recover_resource(self, user, victim):
        #effect int key: 0-speed, 1-mana, 2-endurance
        if self.effect_int == 0:
            user.speed += 60
    
    def multi_target_damage(self, user, victim):
        from main import enemies
        aoe_damage = self.damage
        if self.name == "Comet":
            aoe_damage = 3
        if user.player_class:
            for e in enemies:
                e.take_damage(aoe_damage)
                if "stealth" in e.status:
                    game_out(f"{e.name}'s location has been revealed, they lose the stealth effect!")
                    del e.status["stealth"]
            return
        else:
            main.player.take_damage(aoe_damage)
            if "Stealth" in main.player.status:
                game_out(f"Your location has been revealed, you lose the stealth effect!")
                del main.player.status["stealth"]
            
    def entangle(self, user, victim):
        victim.status["entangled"] = [self.duration, self.effect_int, self.name]
        if not victim.player_class and user.status["ranged"][0] != True:
            user.status["ranged"] = [False, "status"]
        game_out(f"{victim.name} is entangled! They are unable to move!")
        victim.status["ranged"][0] = False
    
    def augment_attack(self, user, victim):
        user.status["augment_attack"] = [self.duration, self.effect_int, self.name]
        user.basic_attack(victim)
    
    def guaranteed_hit(self, user, victim):
        victim.health -= self.damage
        game_out(f"{victim.name} is hit for {self.damage} damage!")
        

class Style(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, duration: int, ranged:bool, endurance_cost: int):
        super().__init__(name, effect, effect_int, damage, duration, ranged)
        self.endurance_cost = endurance_cost
    
    def use_style(self, user, victim):
        # print(user.name, self.name, victim.name)
        # print(self.endurance_cost, user.endurance)
        if self.effect in user.status and user.player_class:
            game_out(f"You already benefit from {self.name}! Choose a different action.", "error")
            main.wait_player_input()
            return
        if self.endurance_cost <= user.endurance:
            user.use_endurance(self.endurance_cost)
            game_out(f"{user.name} uses {self.name}", "styles")
            self.ability_effect(user, victim)
            main.set_char_stats()
            if user.player_class:
                main.ask_extra_attack()
        else:
            game_out(f"Not enough endurance to use this style", "error")
            main.wait_player_input()
    
#Styles
firebolt = Style("Fire Bolt", "direct_damage", effect_int=2, damage=8, duration=1, ranged=True, endurance_cost=25)
tear_flesh = Style("Tear Flesh", "vulnerability", effect_int=0, damage=4, duration=2, ranged=False, endurance_cost=25)
lotus_bloom = Style("Lotus Bloom", "multi_target_damage", effect_int=0, damage=5, duration=1, ranged=True, endurance_cost=25)
arcane_pulse = Style("Arcane Pulse", "multi_target_damage", effect_int=0, damage=5, duration=2, ranged=True, endurance_cost=25)
sweeping_strike = Style("Sweeping Strike", "multi_target_damage", effect_int=0, damage=5, duration=1, ranged=True, endurance_cost=25)
defensive_strike = Style("Defensive Strike", "raise_avoidance", effect_int=1, damage=4, duration=2, ranged=False, endurance_cost=25)
stealth = Style("Stealth", "stealth", effect_int=0, damage=0, duration=0, ranged=True, endurance_cost=25)
heavy_strike = Style("Heavy Strike", "direct_damage", effect_int=1, damage=8, duration=1, ranged=False, endurance_cost=25)
bloody_strike = Style("Bloody Strike", "damage_over_time", effect_int=1, damage=6, duration=3, ranged=False, endurance_cost=25)
fade = Style("Fade", "raise_deflection", effect_int=2, damage=0, duration=3, ranged=True, endurance_cost=25)
envenom = Style("Envenom", "damage_over_time", effect_int=1, damage=3, duration=2, ranged=False, endurance_cost=30)

starting_styles = {"Fire Bolt": firebolt, "Tear Flesh": tear_flesh,
                   "Lotus Bloom": lotus_bloom, "Arcane Pulse": arcane_pulse,
                   "Sweeping Strike": sweeping_strike, "Defensive Strike": defensive_strike,
                   "Stealth": stealth, "Heavy Strike": heavy_strike,
                   "Bloody Strike": bloody_strike, "Fade": fade}

class Spell(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, duration: int, ranged:bool, mana_cost: int):
        super().__init__(name, effect, effect_int, damage, duration, ranged)
        self.mana_cost = mana_cost 
        
    def use_spell(self, user, victim):
        # print(user.name, self.name, victim.name)
        if self.effect in user.status and user.player_class:
            game_out(f"You already benefit from {self.name}! Choose a different action.", "error")
            main.wait_player_input()
            return
        if self.mana_cost <= user.mana:
            user.use_mana(self.mana_cost)
            game_out(f"{user.name} uses {self.name}", "spells")
            self.ability_effect(user, victim)
            main.set_char_stats()
            if user.player_class:
                main.ask_extra_attack()
        else:
            game_out(f"Not enough mana to use this spell", "error")
            main.wait_player_input()
        
#Spells
transfusion = Spell("Transfusion", "lifedraw", effect_int=0, damage=6, duration=0, ranged=True, mana_cost=50) #use player.level as effect int to modify damage
inflame_weapon = Spell("Inflame Weapon", "augment_attack", effect_int=2, damage=4, duration=2, ranged=True, mana_cost=50)
shadow_guise = Spell("Shadow Guise", "raise_deflection", effect_int=2, damage=0, duration=2, ranged=True, mana_cost=25) #effect int used for status counter
second_wind = Spell("Second Wind", "recover_resource", effect_int=0, damage=0, duration=0, ranged=True, mana_cost=50) #effect int will indicate which resource to recover
entangle = Spell("Entangle", "entangle", effect_int=3, damage=0, duration=3, ranged=True, mana_cost=25)
comet = Spell("Comet", "direct_damage", effect_int=2, damage=12, duration=0, ranged=True, mana_cost=50) #effect int used for area of effect damage
missile_barrage = Spell("Missile Barrage", "guaranteed_hit", effect_int=0, damage=6, duration=0, ranged=True, mana_cost=40)


starting_spells = {"Transfusion": transfusion,
                   "Inflame Weapon": inflame_weapon, "Shadow Guise": shadow_guise,
                   "Second Wind": second_wind, "Entangle": entangle, "Comet": comet, "Missile Barrage": missile_barrage}


new_ability_dict = dict({"Wizard": {"Wizard_Styles": ["Fire Bolt", "Fade"], "Wizard_Spells": ["Comet", "Entangle", "Missile Barrage"]}, 
                    "Warrior": {"Warrior_Styles": ["Sweeping Strike", "Bloody Strike", "Defensive Strike"], "Warrior_Spells": ["Transfusion", "Inflame Weapon"]},
                    "Ninja": {"Ninja_Styles": ["Tear Flesh", "Stealth", "Envenom"], "Ninja_Spells": ["Shadow Guise", "Second Wind", "Inflame Weapon"]}})

if __name__ == "__main__":
    Ability.set_damage_over_time()












