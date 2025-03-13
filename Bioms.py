from Environment import Environment
from Creature import Creature, CreatureType
from Utils.Object import Object
from Utils.Renderer import Renderer

class CreatureInfo:
    creature : Creature
    object : Object
    position : tuple[int, int]
    direction : tuple[int, int]
    name : str


class Biomes:
    def __init__(self, renderer: Renderer):
        self.environment = Environment()
        self.creatures : list[Creature] = []
        self.objects : dict[str, CreatureInfo] = {}
        self.renderer = renderer

    def addCreature(self, creatureType: CreatureType, name: str, position: tuple[int, int], direction: tuple[int, int]):

    def render(self):
