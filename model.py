from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from agent import Ant




class HiveModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, random_spawn = True):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
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
              # print(x, y)
            else:
              x,y = 0,0 #start at the origin (top left)
            new_ant = Ant(self.next_id(), self, (x,y))
            #add pos and schedule
            self.grid.place_agent(new_ant, (x,y))
            print(self.grid)
            # print("hallo")
            self.schedule.add(new_ant)


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        # Save the statistics
        self.mean_x_pos.append(sum([agent_.pos[0] for agent_ in self.schedule.agents])/self.num_agents)
        self.mean_y_pos.append(sum([agent_.pos[1] for agent_ in self.schedule.agents])/self.num_agents)
        print(self.grid)
