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
                self.automatic_hit(user, victim)
            case "resource_recover":
                self.recover_resource(user, victim)
            case "multi_target_damage":
                self.multi_target_damage(user, victim)   
            case "augment_attack":
                pass
    
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
    
    def stealth(self, user, victim): #ninja stealth, wizard missile barrage
        user.status[self.effect] = True
        game_out(f"You are stealthed! Enemies cannot see you! Stealth will break if you attack, use a spell, or use a style to harm an enemy", "blue")
        game_out(f"Your next attack or style is guaranteed to hit", "blue")
    
    def lifedraw(self, user, victim): #warrior transfusion
        total_life = randint(1, 6) + player.level
        user.health += total_life
        victim.health -= total_life
        game_out(f"{user.name} stole {total_life} health from {victim.name}!", "blue")
    
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
        for e in enemies:
            e.take_damage(self.damage)
    
    def entangle(self, user, victim):
        victim.status["entangled"] == [self.duration, self.effect_int, self.name]
        game_out(f"{victim.name} is entangled! They are unable to move!")
        

class Style(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, duration: int, endurance_cost: int):
        super().__init__(name, effect, effect_int, damage, duration)
        self.endurance_cost = endurance_cost
    
    def use_style(self, user, victim):
        print(user.name, self.name, victim.name)
        print(self.endurance_cost, user.endurance)
        if self.effect in user.status:
            game_out(f"You already benefit from {user.name}! Choose a different action.", "error")
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
firebolt = Style("Fire Bolt", "direct_damage", 2, 8, 1, 2, 25)
tear_flesh = Style("Tear Flesh", "vulnerability", 0, 3, 1, 2, 25)
lotus_bloom = Style("Lotus Bloom", "multi_target_damage", 0, 3, 3, 1, 25)
arcane_pulse = Style("Arcane Pulse", "multi_target_damage", 0, 3, 3, 2, 25)
sweeping_strike = Style("Sweeping Strike", "multi_target_damage", 0, 3, 3, 1, 25)
defensive_strike = Style("Defensive Strike", "raise_avoidance", 1, 4, 1, 2, 25)
stealth = Style("Stealth", "stealth", 0, 0, 0, 25, 1)
heavy_strike = Style("Heavy Strike", "direct_damage", 0, 8, 1, 1, 5)
bloody_strike = Style("Bloody Strike", "damage_over_time", 1, 6, 1, 3, 25)
fade = Style("Fade", "raise_deflection", 2, 0, 0, 3, 25)

starting_styles = {"Fire Bolt": firebolt, "Tear Flesh": tear_flesh,
                   "Lotus Bloom": lotus_bloom, "Arcane Pulse": arcane_pulse,
                   "Sweeping Strike": sweeping_strike, "Defensive Strike": defensive_strike,
                   "Stealth": stealth, "Heavy Strike": heavy_strike,
                   "Bloody Strike": bloody_strike, "Fade": fade}

class Spell(Ability):
    def __init__ (self, name, effect: str, effect_int:int, damage: int, duration: int, mana_cost: int, player_class: str = None):
        super().__init__(name, effect, effect_int, damage, duration)
        self.mana_cost = mana_cost 
        
    def use_spell(self, user, victim):
        print(user.name, self.name, victim.name)
        print(self.endurance_cost, user.endurance)
        if self.effect in user.status:
            game_out(f"You already benefit from {user.name}! Choose a different action.", "error")
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
transfusion = Spell("Transfusion", "lifedraw", 0, 6, 1, 0, 50) #use player.level as effect int to modify damage
spell_reflect = Spell("Spell Reflect", "reflect", 0, 0, 1, 0, 25, "Warrior")
inflame_weapon = Spell("Inflame Weapon", "augment_attack", 0, 4, 1, 2, 50)
shadow_guise = Spell("Shadow Guise", "raise_deflection", 2, 0, 0, 2, 25, "Ninja") #effect int used for status counter
second_wind = Spell("Second Wind", "recover_resource", 0, 0, 0, 0, 50, "Ninja") #effect int will indicate which resource to recover
vanish = Spell("Vanish", "leave_combat", 0, 0, 0, 0, 30, "Ninja")
entangle = Spell("Entangle", "entangle", 3, 0, 1, 2, 25, "Wizard")
comet = Spell("Comet", "direct_damage", 3, 12, 4, 0, 50, "Wizard") #effect int used for area of effect damage
missile_barrage = Spell("Missile Barrage", "automatic_hit", 0, 6, 1, 0, 40, "Wizard")

starting_spells = {"Transfusion": transfusion, "Spell Reflect": spell_reflect,
                   "Inflame Weapon": inflame_weapon, "Shadow Guise": shadow_guise,
                   "Second Wind": second_wind, "Entangle": entangle, "Comet": comet, "Missile Barrage": missile_barrage}


if __name__ == "__main__":
    Ability.set_damage_over_time()












