from Utils.ProjectApp import ProjectApp
import numpy as np


xAxis = np.array([[-10.0, 0.0], [10.0, 0.0]], dtype= np.float32)
yAxis = np.array([[0.0, 10.0], [0.0, -10.0]], dtype= np.float32) 

xCoords = np.linspace(-10.0,10.0, 1500).astype(dtype=np.float32)
g1YCoords = np.sin(5* np.pi * xCoords) * xCoords
g1 = np.column_stack([xCoords,g1YCoords])

gridData = []
for i in range(-10,10):
    gridData.append([-10.0, i])
    gridData.append([10.0, i])
    gridData.append([i, -10.0])
    gridData.append([i, 10.0])

grid = np.array(gridData, dtype=np.float32)

class RungeKutta(ProjectApp):
    def __init__(self, width, height):
        super().__init__(width, height, "Runge-Kutta Demos")

    def setup(self):
        #Initial settings
        self.addLine(xAxis)
        self.addLine(yAxis)
        self.addLines(grid)
        self.addGraph(g1)


if __name__=="__main__":
    rkApp = RungeKutta(1000, 800)
    rkApp.initialize()
    rkApp.run()