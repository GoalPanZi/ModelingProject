import enum

class CreatureType(enum.Enum):
    PLANT = 0
    ANIMAL = 1

class Creature:
    def __init__(self, creature_type: CreatureType, name: str):
        self.creature_type = creature_type
        self.name = name
        self.health = 100
        self.nutrition = 0
        self.age = 0
        self.is_alive = True
        self.energy_efficiency = 0.5
        self.growth_rate = 0.1
        self.reproduction_rate = 0.1
        self.mutation_rate = 0.1
        self.mutation_amount = 0.1
        self.mutation_chance = 0.1

    def __str__(self):
        return f"{self.name} ({self.creature_type.name})"
    
class Plant(Creature):
    def __init__(self, name: str):
        super().__init__(CreatureType.PLANT, name)

class Animal(Creature):
    def __init__(self, name: str):
        super().__init__(CreatureType.ANIMAL, name)
    
