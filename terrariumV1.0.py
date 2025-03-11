import numpy as np
from Utils.ProjectApp import ProjectApp

class TerrariumApp(ProjectApp):
    def __init__(self, width, height):
        super().__init__(width, height, "Terrarium")

    def setup(self):
        self.lockZoom()
        self.lockDrag()

        LIGHT_BLUE = (165/255, 241/255, 246/255, 0.8)
        GROUND_COLOR = (84/255, 59/255, 14/255, 0.95)

        WALL_THICKNESS = 6.0

        BOTTLE_WIDTH = 1.0
        GROUND_HEIGHT = 0.4
        BOTTLE_HEIGHT = 1.2
        BOTTLE_START_Y = -0.8
        # Ground
        ground = np.array([
            [-BOTTLE_WIDTH/2, BOTTLE_START_Y],
            [BOTTLE_WIDTH/2, BOTTLE_START_Y],
            [BOTTLE_WIDTH/2, BOTTLE_START_Y + GROUND_HEIGHT],
            [-BOTTLE_WIDTH/2, BOTTLE_START_Y + GROUND_HEIGHT]
        ], dtype=np.float32)
        self.addRectangle(ground, GROUND_COLOR)

        # Glass Wall
        wall = np.array([[-BOTTLE_WIDTH/2, BOTTLE_START_Y + BOTTLE_HEIGHT],[-BOTTLE_WIDTH/2, BOTTLE_START_Y],
                        [BOTTLE_WIDTH/2, BOTTLE_START_Y], [BOTTLE_WIDTH/2, BOTTLE_START_Y + BOTTLE_HEIGHT]], dtype=np.float32)
        self.addLine(wall, LIGHT_BLUE, lineWidth=WALL_THICKNESS)
        t = np.linspace(0, np.pi, 100)
        xCoords = BOTTLE_WIDTH/2 * np.cos(t)
        yCoords = BOTTLE_START_Y + BOTTLE_HEIGHT + BOTTLE_WIDTH/2 * np.sin(t)
        g1 = np.column_stack([xCoords,yCoords]).astype(dtype=np.float32)
        self.addGraph(g1, LIGHT_BLUE, lineWidth=WALL_THICKNESS)
    
    
app = TerrariumApp(600, 800)
app.initialize()
app.run()
