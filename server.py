
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from agent import Ant
from model import HiveModel
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    """Portrayal of ants and obstacles"""
    portrayal = {}
    if type(agent) == Ant:
        portrayal = {
            "Shape": "circle", "Filled": "true", "color": "blue", "Layer":0, "r": 0.9,
            "text_color": "black"
        }

    return portrayal




width = 100
height = 100
agent_num = 50

# Create the server, and pass the grid and the graph
ant_slider = UserSettableParameter(
    'slider', 'Number of ants', value=10, min_value=1, max_value=100, step=1
)

# model = HiveModel(agent_num, width, height, False)
# grid = CanvasGrid(agent_portrayal, width, height, 500, 500)


grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
model_par = {
    "N":ant_slider,
    "width":width,
    "height":height,
    "random_spawn":True
    }

print("runserver")
server = ModularServer(HiveModel,
                       [grid],
                       "Ant random_model",
                       model_par
                       )
