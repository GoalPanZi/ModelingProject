<<<<<<< HEAD
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
=======
from Utils.ModelingAppQt import ModelingAppQt
>>>>>>> 03c31feaf1e063179142544b8dac246c25144752

if __name__=="__main__":
    testApp = ModelingAppQt(1600, 1200, "Test")
    testApp.run()
