from mesa import Model, Agent


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
