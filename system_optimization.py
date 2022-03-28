
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A python project for algorithmic trading in FXCM                                           -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- script: requirements.txt : text file with the required libraries for the project                    -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: MIT License                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Template repository: https://github.com/IFFranciscoME/trading-project                               -- #
# -- --------------------------------------------------------------------------------------------------- -- #
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import plot_cost_history, plot_contour, plot_surface
import matplotlib.pyplot as plt
from pyswarms.utils.plotters.formatters import Mesher, Designer
# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
# Call instance of PSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=2, options=options)
# Perform optimization
best_cost, best_pos = optimizer.optimize(fx.sphere, iters=100)
best_cost
best_pos

# Obtain the cost history
optimizer.cost_history
# Obtain the position history
optimizer.pos_history
# Obtain the velocity history
optimizer.velocity_history

# Plot the cost
plot_cost_history(optimizer.cost_history)
plt.show()

# Plot the sphere function's mesh for better plots
m = Mesher(func=fx.sphere,
           limits=[(-1,1), (-1,1)])
# Adjust figure limits
d = Designer(limits=[(-1,1), (-1,1), (-0.1,1)],
             label=['x-axis', 'y-axis', 'z-axis'])

plot_contour(pos_history=optimizer.pos_history, mesher=m, designer=d, mark=(0,0))
plt.show()