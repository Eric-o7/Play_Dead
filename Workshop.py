from combatant import *

snakey = Combatant(name="Snakey", level=3 , health=18 , player_class=None, strength=6 , agility=7 , acuity=10 , 
primary_stat=10 , avoidance=11 , resistance=15 , deflection=1 , map=None, coordinate=None, max_mana=130 , max_endurance=90 , 
max_speed=100 , spells=[comet, missile_barrage, spell_reflect], styles=[arcane_pulse, tear_flesh], inventory={} , status={"Ranged": [False, "status"], "Extra Attack": 0}, 
equipment={"Mhand": None, "Ohand": None, "Armor": None}, base_damage=6 , initiative=None , max_health=18 , 
endurance=90 , speed=100 , mana=130)

def __repr__(self):
    print(f"Status {self.status}")

snakey.__repr__()