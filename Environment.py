class Environment:
    def __init__(self):
        self.time = 0
        self.temperature = 50
        self.sunlight = 5
        self.sunlight_vector = (0, 1)
        self.isRaining = False

    def update(self, delta_time: float):
        self.time += delta_time
        self.temperature += 0.01 * delta_time

    def giveSunlight(self, creature: Creature):
        if creature.creature_type == CreatureType.PLANT:
            creature.nutrition += self.sunlight_vector.dot(creature.direction) * creature.energy_efficiency
        elif creature.creature_type == CreatureType.ANIMAL:
            creature.health += self.sunlight * 0.1
