# -*- coding: utf-8 -*-

from multiprocessing import Array
import random
import sys

class GeneticAlgorithm():
    def __init__(self, population_size, chromosome_size, cross_points, cross_l, mutation_l, graph_size, infecteds):
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.cross_points = cross_points
        self.cross_l = cross_l
        self.mutation_l = mutation_l
        self.graph_size = graph_size
        self.infecteds = infecteds

        self.population = []
        self.individual_performance = Array('i', range(population_size), lock=False)

        self.best = []
        self.best_performance = sys.maxint

        self.global_best = []
        self.global_best_performance = sys.maxint

        self.generation = 0

        # cria a população inicial e inicializa a lista de avaliação de indivíduos
        for i in range(self.population_size):
            temp = random.sample(range(graph_size), chromosome_size)

            # remove infectados
            for element in infecteds:
                if (element in temp):
                    temp.remove(element)

            # completa os elementos restantes
            while ((self.chromosome_size - len(temp)) > 0):
                x = random.randint(0, self.graph_size - 1)
                if ((not x in temp) and (not x in infecteds)):
                    temp.append(x)

            self.population.append(temp)


    def parents_select(self):
        # pais selecionados
        parents_list = []

        # # elitismo
        # best_pos = 0
        #
        # for i, performance in enumerate(self.individual_performance):
        #     if (performance < self.best_performance):
        #         best_pos = i
        #
        # # reserva o melhor pai
        # self.best = self.population[best_pos][:]
        # self.best_performance = self.individual_performance[best_pos]
        #
        # # print self.best_performance
        #
        # if(self.best_performance < self.global_best_performance):
        #     self.global_best_performance = self.best_performance
        #     self.global_best = self.best[:]
        #
        # #adicionar o melhor pai na lista de selecionados
        # parents_list.append(self.best)
        # parents_list.append(self.global_best)

        # realiza o torneio
        while len(parents_list) < (self.population_size / 2):
            parents = random.sample(range(self.population_size), 2)

            if (self.individual_performance[parents[0]] < self.individual_performance[parents[1]]):
                parents_list.append(self.population[parents[0]])
            else:
                parents_list.append(self.population[parents[1]])

        # realiza o crossover
        self.cross(parents_list)

    def cross(self, parents_list):
        # cria a nova população
        new_population = []

        while (len(new_population) < self.population_size):
            current_cross_l = random.random()

            if (current_cross_l < self.cross_l):
                parents = random.sample(parents_list, 2)
                parent1 = parents[0]
                parent2 = parents[1]

                points = random.sample(range(1, self.chromosome_size), self.cross_points)
                points.sort()

                child1_tmp = []
                child2_tmp = []

                for i in range(len(points)):
                    if (i == 0):
                        if ((i % 2) == 0):
                            child1_tmp += parent1[:points[i]]
                            child2_tmp += parent2[:points[i]]
                        else:
                            child1_tmp += parent2[:points[i]]
                            child2_tmp += parent1[:points[i]]
                    else:
                        if ((i % 2) == 0):
                            child1_tmp += parent1[points[i - 1]: points[i]]
                            child2_tmp += parent2[points[i - 1]: points[i]]
                        else:
                            child1_tmp += parent2[points[i - 1]: points[i]]
                            child2_tmp += parent1[points[i - 1]: points[i]]

                if ((len(points) % 2) == 0):
                    child1_tmp += parent1[points[-1]:]
                    child2_tmp += parent2[points[-1]:]
                else:
                    child1_tmp += parent2[points[-1]:]
                    child2_tmp += parent1[points[-1]:]

                child1 = list(set(child1_tmp))
                child2 = list(set(child2_tmp))

                while (len(child1) < self.chromosome_size):
                    gene = random.choice(child2)
                    if (gene not in child1):
                        child1.append(gene)

                while (len(child2) < self.chromosome_size):
                    gene = random.choice(child1)
                    if (gene not in child2):
                        child2.append(gene)

                new_population.append(child1)
                new_population.append(child2)

        # remover ultimo filho?
        self.population = new_population[:]

        # inicializa mutação
        self.mutate()

    def mutate(self):
        for i in range(1, self.population_size):
            for g in range(self.chromosome_size):
                x = random.random()
                if (x < self.mutation_l):
                    r = random.randint(0, self.graph_size - 1);
                    if ((r not in self.population[i]) and (r not in self.infecteds)):
                        self.population[i][g] = r
                    else:
                        while ((r in self.population[i]) or (r in self.infecteds)):
                            r = random.randint(0, self.graph_size - 1);
                        self.population[i][g] = r

        self.generation += 1