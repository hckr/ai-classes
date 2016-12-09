#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
from functions import easom, griewank, rosenbrock
from summary import prepare_summary, show_summaries
from classes import Entity, Population, Selection

population_size = 200
problem_size = 2
epochs = 100

objective_function = easom
search_ranges = [ (-100, 100) for _ in xrange(problem_size) ] # Easom
# search_ranges = [ (-600, 600) for _ in xrange(problem_size) ] # Griewank
# search_ranges = [ (-5, 10) for _ in xrange(problem_size) ] # Rosenbrock

initial_population = Population.random(
    population_size, problem_size, search_ranges, objective_function
)

### 1+1 selection ###

selection = Selection.one_plus_one()
population = initial_population
best_adaptation_values = []
mean_adaptation_values = []
mean_distances = []
for epoch in range(epochs):
    population = Population.new_generation(population, selection)
    best_adaptation_values.append(population.best_adaptation_value())
    mean_adaptation_values.append(population.mean_adaptation_value())
    mean_distances.append(population.mean_distance())

results_one_plus_one = [
    ['Best adaptation', best_adaptation_values],
    ['Mean adaptation', mean_adaptation_values],
    ['Mean distance between solutions', mean_distances]
]

best_adapted = population.best_adapted()
print '%10s\t--\tcoords: %s, fitness val: %.10f' % (
    '1+1', best_adapted.coords, best_adapted.get_fitness_value()
)

prepare_summary('1+1 selection results', results_one_plus_one)

### plus selection ###

selection = Selection.plus(2, 300) # parents, children
population = initial_population
best_adaptation_values = []
mean_adaptation_values = []
mean_distances = []
for epoch in range(epochs):
    population = Population.new_generation(population, selection)
    best_adaptation_values.append(population.best_adaptation_value())
    mean_adaptation_values.append(population.mean_adaptation_value())
    mean_distances.append(population.mean_distance())

results_plus = [
    ['Best adaptation', best_adaptation_values],
    ['Mean adaptation', mean_adaptation_values],
    ['Mean distance between solutions', mean_distances]
]

best_adapted = population.best_adapted()
print '%10s\t--\tcoords: %s, fitness val: %.10f' % (
    'plus', best_adapted.coords, best_adapted.get_fitness_value()
)

prepare_summary('plus selection results', results_plus)

### comma selection ###

selection = Selection.comma(2, 500) # parents, children
population = initial_population
best_adaptation_values = []
mean_adaptation_values = []
mean_distances = []
for epoch in range(epochs):
    population = Population.new_generation(population, selection)
    best_adaptation_values.append(population.best_adaptation_value())
    mean_adaptation_values.append(population.mean_adaptation_value())
    mean_distances.append(population.mean_distance())

results_comma = [
    ['Best fitness value', best_adaptation_values],
    ['Mean fitness value', mean_adaptation_values],
    ['Mean distance between solutions', mean_distances]
]

best_adapted = population.best_adapted()
print '%10s\t--\tcoords: %s, fitness val: %.10f' % (
    'comma', best_adapted.coords, best_adapted.get_fitness_value()
)

prepare_summary('comma selection results', results_comma)

show_summaries()
