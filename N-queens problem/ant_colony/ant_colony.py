#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pheromonetrail import PheromoneTrail, animate_pheromone_trails
from ant import Ant

problem_size = 8
ants_count = 80
max_epochs = 120
PheromoneTrail.INITIAL_PHEROMONE = 0.0001
Ant.ALPHA = 0.9
Ant.BETA = 2
Ant.MAX_PHEROMONE_AMOUNT = 2
EVAPORATION_FACTOR = 0.9

###

pheromone_trails = []
best_ants = []
global_best_ant = None
last_pheromone_trail = None
for epoch in range(max_epochs):
    last_pheromone_trail = PheromoneTrail(last_pheromone_trail, EVAPORATION_FACTOR)
    pheromone_trails.append(last_pheromone_trail)
    ants = []
    for _ in range(ants_count):
        ant = Ant(problem_size, last_pheromone_trail)
        ants.append(ant)
    for ant in ants:
        ant.place_pheromone()
    best_ant = max(ants, key=lambda a: a.count_not_beating())
    best_ants.append(best_ant)
    if best_ant.count_not_beating() == problem_size:
        global_best_ant = best_ant
        break
else:
    global_best_ant = max(best_ants, key=lambda a: a.count_not_beating())

epochs_needed = len(best_ants)
print 'Epochs needed: ', epochs_needed
print 'Best solution: ', global_best_ant.queens_rows
best_non_beating = global_best_ant.count_not_beating()
print 'Non-beating queens: ', best_non_beating

import matplotlib.pyplot as plt
plt.figure()
plt.plot([a.count_not_beating() for a in best_ants], 'co-')
plt.xlabel('Epochs')
plt.ylabel('Non-beating queens')
plt.show()

if best_non_beating == problem_size:
    print '\n', 'Generating video...'
    ani = animate_pheromone_trails(pheromone_trails, problem_size, global_best_ant, interval=10)
    ani.save('pso_%d_queens_%d_ants_%d_epochs.mp4' % (problem_size, ants_count, epochs_needed), fps=1)
