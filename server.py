from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from agent import Ant
from model import HiveModel
from mesa.visualization.ModularVisualization import ModularServer
from collections import defaultdict

def agent_portrayal(agent):
    """Portrayal of ants and obstacles"""
    portrayal = {}
    if type(agent) == Ant:
        portrayal = {
            "Shape": "circle", "Filled": "true", "color": "blue", "Layer":1, "r": 0.9,
            "text_color": "black"
        }

    return portrayal



class CanvasGrid_ant(CanvasGrid):
    """A CanvasGrid object uses a user-provided portrayal method to generate a
    portrayal for each object. A portrayal is a JSON-ready dictionary which
    tells the relevant JavaScript code (GridDraw.js) where to draw what shape.

    The render method returns a dictionary, keyed on layers, with values as
    lists of portrayals to draw. Portrayals themselves are generated by the
    user-provided portrayal_method, which accepts an object as an input and
    produces a portrayal of it.

    Attributes:
        portrayal_method: Function which generates portrayals from objects, as
                          described above.
        grid_height, grid_width: Size of the grid to visualize, in cells.
        canvas_height, canvas_width: Size, in pixels, of the grid visualization
                                     to draw on the client.
        template: "canvas_module.html" stores the module's HTML template.

    """

    package_includes = ["GridDraw.js", "CanvasModule.js", "InteractionHandler.js"]

    def __init__(
        self,
        portrayal_method,
        grid_width,
        grid_height,
        canvas_width=500,
        canvas_height=500,
    ):
        """Instantiate a new CanvasGrid.

        Args:
            portrayal_method: function to convert each object on the grid to
                              a portrayal, as described above.
            grid_width, grid_height: Size of the grid, in cells.
            canvas_height, canvas_width: Size of the canvas to draw in the
                                         client, in pixels. (default: 500x500)

        """
        self.portrayal_method = portrayal_method
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        new_element = "new CanvasModule({}, {}, {}, {})".format(
            self.canvas_width, self.canvas_height, self.grid_width, self.grid_height
        )

        self.js_code = "elements.push(" + new_element + ");"

        def render(self, model):
            grid_state = defaultdict(list)
            for x in range(model.grid.width):
                for y in range(model.grid.height):
                    cell_objects = model.grid.get_cell_list_contents([(x, y)])

                    for obj in cell_objects:
                        portrayal = self.portrayal_method(obj)
                        if portrayal:
                            portrayal["x"] = x
                            portrayal["y"] = y
                            grid_state[portrayal["Layer"]].append(portrayal)

            return grid_state


width = 50
height = 50
agent_num = 2

# Create the server, and pass the grid and the graph
ant_slider = UserSettableParameter(
    'slider', 'Number of ants', value=10, min_value=1, max_value=100, step=1
)

# model = HiveModel(agent_num, width, height, False)
# grid = CanvasGrid(agent_portrayal, width, height, 500, 500)


grid = CanvasGrid_ant(agent_portrayal, width, height, 500, 500)
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
