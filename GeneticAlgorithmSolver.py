from RouteManager import RouteManager
from Route import Route

import numpy as np
import random


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.2, tournament_size=10, elitism=False):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def solve(self, rm):
        rm = self.evolve(rm)
        for i in range(100):
            rm = self.evolve(rm)
        return rm

    def evolve(self, routes):
        # YOUR CODE HERE
        # population_size == 10
        bb = 0
        while bb < self.population_size:
            aa, cc = 0, 0
            rot1, rot2, index, fit = [], [], [], []
            while cc < 2:
                for aa in range(0, self.tournament_size):
                    ind = random.randint(0, self.population_size - 1)
                    check = (ind in index)
                    if check:
                        continue
                    index.append(ind)
                    route = routes.get_route(ind)
                    fit.append(route)
                    aa += 1
                if cc == 0:
                    rot1 = self.tournament(fit)
                elif cc == 1:
                    rot2 = self.tournament(fit)
                cc += 1
            update = self.crossover(rot1, rot2)
            routes.set_route(bb, update)
            bb += 1
        return routes

    def crossover(self, route_1, route_2):
        # YOUR CODE HERE
        newChild = Route(self.cities)
        randNum1 = random.randint(0, len(self.cities) - 2)
        randNum2 = random.randint(randNum1 + 1, len(self.cities) - 1)

        for target in range(randNum1, randNum2):
            newChild.assign_city(target, route_1.get_city(target))

        # we can write 20 instead of "len(self.cities)" because
        # we know that we have 20 cities, I obtain this  from CityManager class

        for target in range(randNum2, len(self.cities)):
            if newChild.get_city(target) is None:
                a = 0
                while a < randNum2:
                    value = route_2.get_city(a)
                    if value not in newChild:
                        newChild.assign_city(target, value)
                        break
                    a += 1

        # here I am using "20" because it will occur same results
        for target in range(randNum2, 20):
            if newChild.get_city(target) is None:
                a = 0
                while a < randNum2:
                    value = route_2.get_city(a)
                    if value not in newChild:
                        newChild.assign_city(target, value)
                        break
                    a += 1
        # we can either use FOR or WHILE loops, thats why I used them both
        # to proof it
        for target in range(0, len(self.cities)):
            if newChild.get_city(target) is None:
                for a in range(0, 20):
                    value = route_2.get_city(a)
                    if value not in newChild:
                        newChild.assign_city(target, value)
                        break

        potentialChange = random.random()
        if potentialChange <= self.mutation_rate:
           self.mutate(newChild)

        return newChild

    def mutate(self, route):
        # YOUR CODE HERE
        factor_1 = random.randint(0, route.__len__() - 1)
        factor_2 = random.randint(0, route.__len__() - 1)
        aa = route.get_city(factor_1)
        bb = route.get_city(factor_2)
        # basically what we are doing is swap operation
        route.assign_city(factor_1, bb)
        route.assign_city(factor_2, aa)

    def tournament(self, routes):
        # YOUR CODE HERE
        champ = None
        for a in range(0, len(routes)):
            aa = (champ is None)
            if aa or routes[a].calc_fitness() > champ.calc_fitness():
                champ = routes[a]
        # we are trying to find more fitter route in here
        return champ

