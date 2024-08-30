from main import *

class Ability():
    def __init__(self, name, effect: str, effect_int:int, damage: range, duration: int):
        self.name = name
        self.effect = effect #identified using ability_effect() method
        self.effect_int = effect_int
        self.damage = damage #max damage or range
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
            case "stealth":
                self.stealth(user, victim)   
            case "lifedraw":
                self.lifedraw(user, victim)  
            case "reflect":
                self.reflect(user, victim)
            case "resource_recover":
                self.recover_resource(user, victim)
            case "multi_target_damage":
                self.multi_target_damage(user, victim)
            case "entangle":
                self.entangle(user, victim)   
            case "augment_attack":
                self.augment_attack(user, victim)
            case "automatic_hit":
                self.automatic_hit(user, victim)
    
    #damage_over_time set up is Combatant.status = {"damage_over_time":{dot1:[duration,effect_int]}, {dot2:[duration, effect_int]}}
        
    def set_damage_over_time(self, user, victim): #warrior bloody
        if self.effect in victim.status:
            dot_key = f"dot{len(victim.status['damage_over_time'])+1}"
            victim.status[self.effect][dot_key] = [self.duration, self.effect_int, self.name]
        else:
            victim.status[self.effect] = {"dot1": [self.duration, self.effect_int, self.name]}
        game_out(f"Damage over time effect applied to {victim.name}")
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
        if self.damage:
            user.basic_attack(victim, self.damage)
    
    def raise_deflection(self, user, victim): #ninja shadow guise
        user.status["raise_deflection"] = [self.duration, self.effect_int, self.name]
        user.set_deflection()
        if self.damage:
            user.basic_attack(victim, self.damage)
    
    def direct_damage(self, user, victim): #effect int 1 is physical, effect int 2 is spell damage
        if self.effect_int == 2 and user.resistance_check(victim):
            victim.take_damage(self.damage)
        elif self.effect_int == 1 and user.avoidance_check(victim):
            victim.take_damage(self.damage)
        if self.name == "Comet":
            self.multi_target_damage(user, victim)
    
    def stealth(self, user, victim): #ninja stealth, wizard missile barrage
        user.status[self.effect] = True
        game_out(f"You are stealthed! Enemies cannot see you! Stealth will break if you attack, use a spell, or use a style to harm an enemy", "blue")
        game_out(f"Your next attack or style is guaranteed to hit", "blue")
    
    def lifedraw(self, user, victim): #warrior transfusion
        total_life = randint(1, 6) + player.level
        if user.resistance_check(victim):
            game_out(f"{user.name} stole {total_life} health from {victim.name}!", "blue")
        else:
            total_life //= 2
            game_out(f"{self.name} was partially resisted. {user.name} stole {total_life} health from {victim.name}!", "blue")
        user.health += total_life
        victim.health -= total_life

    
    
    def reflect(self, user, victim):
        user.status["reflect"] = True
        #when building NPC action logic, find out where to put this
    
    def leave_combat(self, user, victim):
        pass
    
    def recover_resource(self, user, victim):
        #effect int key: 0-speed, 1-mana, 2-endurance
        if self.effect_int == 0:
            user.speed += 60
    
    def multi_target_damage(self, user, victim):
        from main import enemies
        aoe_damage = self.damage
        if self.name == "Comet":
            aoe_damage == 3
        print([e.health for e in enemies])
        for e in enemies:
            e.take_damage(self.damage)
        print([e.health for e in enemies])
            
    
    def entangle(self, user, victim):
        victim.status["entangled"] == [self.duration, self.effect_int, self.name]
        game_out(f"{victim.name} is entangled! They are unable to move!")
    
    def augment_attack(self, user, victim):
        user.status["augment_attack"] = [self.duration, self.effect_int, self.name]
        user.basic_attack(victim)
    
    def automatic_hit(self, user, victim):
        victim.health -= self.damage
        game_out(f"You hit {victim.name} automatically for {self.damage} damage!")
        

class Style(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, duration: int, endurance_cost: int):
        super().__init__(name, effect, effect_int, damage, duration)
        self.endurance_cost = endurance_cost
    
    def use_style(self, user, victim):
        print(user.name, self.name, victim.name)
        print(self.endurance_cost, user.endurance)
        if self.effect in user.status:
            game_out(f"You already benefit from {self.name}! Choose a different action.", "error")
            wait_player_input()
            return
        if self.endurance_cost <= user.endurance:
            user.use_endurance(self.endurance_cost)
            self.ability_effect(user, victim)
            ask_extra_attack()
        else:
            game_out(f"Not enough endurance to use this style", "error")
            wait_player_input()
    
#Styles
firebolt = Style("Fire Bolt", "direct_damage", effect_int=2, damage=8, duration=1, endurance_cost=25)
tear_flesh = Style("Tear Flesh", "vulnerability", effect_int=0, damage=3, duration=2, endurance_cost=25)
lotus_bloom = Style("Lotus Bloom", "multi_target_damage", effect_int=0, damage=3, duration=1, endurance_cost=25)
arcane_pulse = Style("Arcane Pulse", "multi_target_damage", effect_int=0, damage=3, duration=2, endurance_cost=25)
sweeping_strike = Style("Sweeping Strike", "multi_target_damage", effect_int=0, damage=5, duration=1, endurance_cost=25)
defensive_strike = Style("Defensive Strike", "raise_avoidance", effect_int=1, damage=4, duration=2, endurance_cost=25)
stealth = Style("Stealth", "stealth", effect_int=0, damage=0, duration=0, endurance_cost=25)
heavy_strike = Style("Heavy Strike", "direct_damage", effect_int=0, damage=8, duration=1, endurance_cost=25)
bloody_strike = Style("Bloody Strike", "damage_over_time", effect_int=1, damage=6, duration=3, endurance_cost=25)
fade = Style("Fade", "raise_deflection", effect_int=2, damage=0, duration=3, endurance_cost=25)

starting_styles = {"Fire Bolt": firebolt, "Tear Flesh": tear_flesh,
                   "Lotus Bloom": lotus_bloom, "Arcane Pulse": arcane_pulse,
                   "Sweeping Strike": sweeping_strike, "Defensive Strike": defensive_strike,
                   "Stealth": stealth, "Heavy Strike": heavy_strike,
                   "Bloody Strike": bloody_strike, "Fade": fade}

class Spell(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, duration: int, mana_cost: int):
        super().__init__(name, effect, effect_int, damage, duration)
        self.mana_cost = mana_cost 
        
    def use_spell(self, user, victim):
        print(user.name, self.name, victim.name)
        print(self.endurance_cost, user.endurance)
        if self.effect in user.status:
            game_out(f"You already benefit from {self.name}! Choose a different action.", "error")
            wait_player_input()
            return
        if self.mana_cost <= user.mana:
            user.use_mana(self.mana_cost)
            self.ability_effect(user, victim)
            ask_extra_attack()
        else:
            game_out(f"Not enough mana to use this spell", "error")
            wait_player_input()
        
#Spells
transfusion = Spell("Transfusion", "lifedraw", effect_int=0, damage=6, duration=0, mana_cost=50) #use player.level as effect int to modify damage
spell_reflect = Spell("Spell Reflect", "reflect", effect_int=0, damage=0, duration=0, mana_cost=25)
inflame_weapon = Spell("Inflame Weapon", "augment_attack", effect_int=0, damage=4, duration=2, mana_cost=50)
shadow_guise = Spell("Shadow Guise", "raise_deflection", effect_int=2, damage=0, duration=2, mana_cost=25) #effect int used for status counter
second_wind = Spell("Second Wind", "recover_resource", effect_int=0, damage=0, duration=0, mana_cost=50) #effect int will indicate which resource to recover
vanish = Spell("Vanish", "leave_combat", effect_int=0, damage=0, duration=0, mana_cost=30)
entangle = Spell("Entangle", "entangle", effect_int=3, damage=0, duration=3, mana_cost=25)
comet = Spell("Comet", "direct_damage", effect_int=3, damage=12, duration=0, mana_cost=50) #effect int used for area of effect damage
missile_barrage = Spell("Missile Barrage", "automatic_hit", effect_int=0, damage=6, duration=0, mana_cost=40)

starting_spells = {"Transfusion": transfusion, "Spell Reflect": spell_reflect,
                   "Inflame Weapon": inflame_weapon, "Shadow Guise": shadow_guise,
                   "Second Wind": second_wind, "Entangle": entangle, "Comet": comet, "Missile Barrage": missile_barrage}


if __name__ == "__main__":
    Ability.set_damage_over_time()












