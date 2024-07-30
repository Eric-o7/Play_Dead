class Combatant():
    def __init__(self, name, health, mana):
        self.name = name
        self.health = health
        self.mana = mana

    def take_damage(self, damage):
        self.health -= damage

    def use_mana(self, mana_cost):
        self.mana -= mana_cost

class PlayerCharacter(Combatant):
    def __init__(self, level, spells=None):
        super().__init__()
        self.level = level
        self.styles = []
        self.spell_list = []
        self.spells = spells

    def add_spell(self, spells):
        self.spell_list.append(self.spells)
    
    def get_spell_list(self):   
        return self.spell_list
    
    def get_styles(self):
        return self.styles
    
    def level_up(self):
        self.level+=1
    

class Paladin(PlayerCharacter):
    def __init__(self, holy_power):
        super().__init__()
        self.holy_power = holy_power
        
class Sorcerer(PlayerCharacter):
    def __init__(self, sorcery):
        super().__init__()
        self.sorcery = sorcery

