#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt
from functions import easom, griewank, rosenbrock

np.seterr(all='ignore')

particles_count = 3000
problem_size = 5
epochs = 500

objective_function = rosenbrock
# search_ranges = [ (-100, 100) for _ in xrange(problem_size) ] # Easom
# search_ranges = [ (-600, 600) for _ in xrange(problem_size) ] # Griewank
search_ranges = [ (-5, 10) for _ in xrange(problem_size) ] # Rosenbrock


class Swarm(object):
    def __init__(self, problem_size, search_ranges, obj_f, particles_count, c1=2, c2=2):
        self.problem_size = problem_size
        self.search_ranges = search_ranges
        self.obj_f = obj_f
        self.c1 = c1
        self.c2 = c2
        self.global_best = None
        self.global_best_obj_f_val = None
        self.particles = []
        for _ in xrange(particles_count):
            new_particle = Particle.random(self)
            new_value = new_particle.obj_f_value()
            if self.global_best_obj_f_val is None \
                    or new_value < self.global_best_obj_f_val:
                self.global_best_obj_f_val = new_value
                self.global_best = new_particle.position[:]
            self.particles.append(new_particle)

    def update_all(self):
        for particle in self.particles:
            particle.update()
            try:
                new_value = particle.obj_f_value()
                if new_value < self.global_best_obj_f_val:
                    self.global_best_obj_f_val = new_value
                    self.global_best = particle.position[:]
            except ValueError:
                pass

class Particle(object):
    def __init__(self, swarm, speed, position, particle_best, r1, r2):
        self.swarm = swarm
        self.speed = speed
        self.position = position
        self.particle_best = particle_best
        self.r1 = r1
        self.r2 = r2

    def obj_f_value(self):
        return self.swarm.obj_f(self.position)

    @classmethod
    def random(cls, swarm):
        speed = np.ones(swarm.problem_size) * random.random() / 10
        position = np.array([ random.uniform(r[0], r[1]) for r in swarm.search_ranges ])
        particle_best = np.array(position)
        r1 = np.random.normal()
        r2 = np.random.normal()
        return cls(swarm, speed, position, particle_best, r1, r2)

    def update(self):
        new_speed = self.speed + \
            (self.swarm.c1 * self.r1 * (self.particle_best - self.position)) + \
            (self.swarm.c2 * self.r2 * (self.swarm.global_best - self.position))
        new_position = self.position + new_speed
        self.position = new_position
        self.speed = new_speed

swarm = Swarm(problem_size, search_ranges, objective_function, particles_count)
best_values = []

for _ in xrange(epochs):
    swarm.update_all()
    best_values.append(swarm.global_best_obj_f_val)

print swarm.global_best
print swarm.global_best_obj_f_val
plt.plot(best_values)
plt.show()
