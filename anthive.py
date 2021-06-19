
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
import matplotlib.pyplot as plt
from mesa.time import SimultaneousActivation
from collections import defaultdict

class Ant(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.energy = 100
        self.pos = pos
        self.state = "FORAGING"
        self.id = unique_id


    def step(self):
      self.move()
      #print(self.unique_id, self.pos)


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center= False, radius = 1)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        print("agent has moved", self.id, self.pos)


class HiveModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, random_spawn = True):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        self.random_spawn = random_spawn
        self.schedule = RandomActivation(self)
        self.mean_x_pos = []
        self.mean_y_pos = []
        self.running = True     # needed to keep simulation running


        # Create agents
        for i in range(self.num_agents):

            # print("made agent", i)
            # print(self.random_spawn)

            if self.random_spawn:
              # Get Random Cell
              x = self.random.randrange(self.grid.width)
              y = self.random.randrange(self.grid.height)
              print(x, y)
            else:
              x,y = 0,0 #start at the origin (top left)
            new_ant = Ant(i, self, (x,y))
            #add pos and schedule
            self.grid.place_agent(new_ant, (x,y))
            print("hallo")
            self.schedule.add(new_ant)


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        # Save the statistics
        self.mean_x_pos.append(sum([agent_.pos[0] for agent_ in self.schedule.agents])/self.num_agents)
        self.mean_y_pos.append(sum([agent_.pos[1] for agent_ in self.schedule.agents])/self.num_agents)
        print(self.grid)

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
agent_num = 10

# Create the server, and pass the grid and the graph
ant_slider = UserSettableParameter(
    'slider', 'Number of ants', value=10, min_value=1, max_value=100, step=1
)

# model = HiveModel(agent_num, width, height, False)
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

server.port = 8521

server.launch()
