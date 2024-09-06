new_ability_dict = dict({"Wizard": {"Wizard_Styles": ["Fire Bolt", "Fade"], "Wizard_Spells": ["Comet", "Entangle", "Missile Barrage"]}, 
                    "Warrior": {"Warrior_Styles": ["Sweeping Strike", "Bloody Strike", "Defensive Strike"], "Warrior_Spells": ["Transfusion", "Inflame Weapon"]},
                    "Ninja": {"Ninja_Styles": ["Tear Flesh", "Stealth", "Envenom"], "Ninja_Spells": ["Shadow Guise", "Second Wind", "Inflame Weapon"]}})

dict1 = "Wizard"

class Potato:
    def __init__(self, weight):
        self.weight = weight

russet = Potato(10)

print(russet)

sample = ["wizard", russet, "seven"]

print([i for i in sample if isinstance(i, Potato)])

# print("potato")
