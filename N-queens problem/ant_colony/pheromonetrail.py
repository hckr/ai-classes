from __future__ import division

class PheromoneTrail(object):
    INITIAL_PHEROMONE = None

    def __init__(self, old_trail=None, evaporation_factor=1):
        if old_trail is not None:
            self.data = dict(old_trail.data)
            self.evaporate(evaporation_factor)
        else:
            self.data = {}

    def evaporate(self, factor):
        self.data.update(
            (k, v * factor) for k, v in self.data.items()
        )

    def mark_trail(self, rows, amount):
        columns = range(len(rows))
        for column1, column2 in zip(columns[:-1], columns[1:]):
            row1 = rows[column1]
            row2 = rows[column2]
            index = (column1, column2, row1, row2)
            self.data[index] = self.get_value(index) + amount

    def get_value(self, *index):
        return self.data.get(index, self.INITIAL_PHEROMONE)


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_pheromone_trails(pheromone_trails, problem_size, best_ant=None, interval=100):
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, problem_size), ylim=(-1, problem_size))
    ax.set_xticklabels([''] + [ chr(c) for c in range(ord('a'), ord('a') + problem_size)] + [''])
    ax.set_yticklabels([''] + [ str(n) for n in range(1, problem_size + 1) ] + [''])
    ax.invert_yaxis()
    ax.grid()

    lines_dict = {}
    columns = range(problem_size)
    for column1, column2 in zip(columns[:-1], columns[1:]):
        for row1 in range(problem_size):
            for row2 in range(problem_size):
                index = (column1, column2, row1, row2)
                lines_dict[index], = ax.plot([column1, column2], [row1, row2], 'b', linewidth=5, alpha=0)
    
    fields_x, fields_y = np.meshgrid(range(problem_size), range(problem_size))
    ax.plot(fields_x, fields_y, 'om')

    caption = ax.text(0.05, 0.95, '', transform=ax.transAxes)

    max_value = max([ max(ft.data.values()) for ft in pheromone_trails ])

    def animate(i):
        caption.set_text('Epoch: %d' % i)
        if i >= len(pheromone_trails) - 1:
            caption.set_text('Best solution')
            i = len(pheromone_trails) - 1
        for index, line in lines_dict.iteritems():
            line.set_alpha(pheromone_trails[i].get_value(*index) / max_value)
        if i+1 == len(pheromone_trails) and best_ant is not None:
            not_beating = best_ant.get_not_beating()
            for x, y in enumerate(best_ant.queens_rows):
                color = 'hotpink'
                if x in not_beating:
                    color = 'deepskyblue'
                ax.plot(x, y, '*', color=color, markersize=25)
        return caption, lines_dict.values()

    return animation.FuncAnimation(fig, animate, range(len(pheromone_trails) + 10), interval=interval, repeat=False)