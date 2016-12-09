from __future__ import division
import random
import math
import numpy as np
from copy import copy

class Selection(object):
    @classmethod
    def one_plus_one(cls):

        def selection(population):
            new_entities = []
            for parent in population.entities:
                child = Entity.mutate(parent)
                if(child.get_fitness_value() <= parent.get_fitness_value()):
                    new_entities.append(child)
                else:
                    new_entities.append(parent)
            return Population(new_entities, population.problem_size, population.obj_f)

        return selection

    @classmethod
    def plus(cls, how_many_parents, how_many_children):

        def selection(population):
            new_entities = population.entities[:]
            for _ in xrange(how_many_children):
                parents = population.random_parents(how_many_parents)
                child = Entity.mutate(
                    Entity.recombine(parents)
                )
                new_entities.append(child)
            new_entities.sort(key=lambda entity: entity.get_fitness_value())
            selected_new_entites = new_entities[:population.size]
            return Population(selected_new_entites, population.problem_size, population.obj_f)

        return selection

    @classmethod
    def comma(cls, how_many_parents, how_many_children):

        def selection(population):
            new_entities = []
            for _ in xrange(how_many_children):
                parents = population.random_parents(how_many_parents)
                child = Entity.mutate(
                    Entity.recombine(parents)
                )
                new_entities.append(child)
            new_entities.sort(key=lambda entity: entity.get_fitness_value())
            selected_new_entites = new_entities[:population.size]
            return Population(selected_new_entites, population.problem_size, population.obj_f)

        return selection


class Population(object):
    def __init__(self, entities, problem_size, obj_f):
        self.entities = entities
        self.problem_size = problem_size
        self.obj_f = obj_f
        self.size = len(entities)

    def random_parents(self, how_many):
        return random.sample(self.entities, how_many)

    def best_adapted(self):
        best_val = float('inf')
        best_entity = None
        for entity in self.entities:
            value = entity.get_fitness_value()
            if value < best_val:
                best_val = value
                best_entity = entity
        return best_entity

    def best_adaptation_value(self):
        return self.best_adapted().get_fitness_value()

    def mean_adaptation_value(self):
        summed = 0
        for entity in self.entities:
            summed += entity.get_fitness_value()
        return summed / len(self.entities)

    def mean_distance(self):
        distances = []
        for entity in self.entities:
            for other_entity in self.entities:
                if entity == other_entity:
                    continue
                tmp = 0
                for i in xrange(self.problem_size):
                    tmp += (entity.coords[i] - other_entity.coords[i]) ** 2
                distances.append(math.sqrt(tmp))
        return sum(distances) / len(distances)

    @classmethod
    def random(cls, population_size, problem_size, search_ranges, obj_f):
        entities = [
            Entity.random(problem_size, search_ranges, obj_f)
            for x in xrange(population_size)
        ]
        return cls(entities, problem_size, obj_f)

    @classmethod
    def new_generation(cls, population, selection):
        return selection(population)


class Entity(object):
    def __init__(self, coords, std_devs, obj_f):
        self.problem_size = len(coords)
        self.coords = coords # Y
        self.std_devs = std_devs # S
        self.obj_f = obj_f # F

    def get_fitness_value(self):
        return self.obj_f(self.coords)

    @classmethod
    def random(cls, problem_size, search_ranges, obj_f):
        coords = [
            random.uniform(search_ranges[i][0], search_ranges[i][1])
            for i in xrange(problem_size)
        ]
        std_devs = [ random.random() for _ in xrange(problem_size) ]
        return cls(coords, std_devs, obj_f)

    @classmethod
    def mutate(cls, entity):
        new_std_devs = [ 0 for _ in xrange(entity.problem_size) ]
        new_coords = [ 0 for _ in xrange(entity.problem_size) ]
        for i in xrange(entity.problem_size):
            new_std_devs[i] = entity.std_devs[i] * 0.85
            new_coords[i] = entity.coords[i] + entity.std_devs[i] * np.random.normal()
        return cls(new_coords, new_std_devs, entity.obj_f)

    @classmethod
    def recombine(cls, parents):
        problem_size = parents[0].problem_size
        coords_summed = [ 0 for _ in xrange(problem_size) ]
        std_devs_summed = [ 0 for _ in xrange(problem_size) ]
        for parent in parents:
            for i in xrange(problem_size):
                coords_summed[i] += parent.coords[i]
                std_devs_summed[i] += parent.std_devs[i]
        avg_coords = [ x / len(parents) for x in coords_summed ]
        avg_std_devs = [ x / len(parents) for x in std_devs_summed ]
        return cls(avg_coords, avg_std_devs, parents[0].obj_f)
