# -*- coding: utf-8 -*-

from igraph import *
import random

__author__ = "Rodrigo Ferreira"
__license__ = "GPLv3"
__email__ = "rodrigoferreira001@hotmail.com"


class SIRModel:

    def __init__(self, graph, beta, gamma):
        """
            Model constructor
            :param graph: An igraph graph
            :param beta: The infection rate (float value in [0,1])
            :param gamma: The recovery rate (float value in [0,1])

        """

        random.seed(3)

        self.iteration = 0
        self.graph = graph
        self.beta = beta
        self.gamma = gamma
        self.status = []

        self.susceptibles = range(graph.vcount())
        self.infecteds = []
        self.recovereds = []

        self.total_infecteds = 0

        self.nodes_neighbors = []

        for v in self.graph.vs():
            self.nodes_neighbors.append(
                {'infected_neighbors': 0,
                 'susceptible_neighbors': self.graph.neighbors(v)})

    def reset(self):
        pass

    def iterate(self):
        """
            Infection and recovery Process
        :return: infection status
        """
        for node in reversed(self.infecteds):

            # infection
            for neighbor in reversed(self.nodes_neighbors[node]['susceptible_neighbors']):
                event = random.random()

                if event < self.beta * self.nodes_neighbors[neighbor]['infected_neighbors']:
                    self.infecteds.append(neighbor)
                    self.susceptibles.remove(neighbor)

                    self.total_infecteds += 1

                    for n in self.graph.neighbors(neighbor):
                        self.nodes_neighbors[n]['susceptible_neighbors'].remove(neighbor)
                        self.nodes_neighbors[n]['infected_neighbors'] += 1

            #recovery
            event = random.random()

            if event < self.gamma:
                self.recovereds.append(node)
                self.infecteds.remove(node)

                for neighbor in self.graph.neighbors(node):
                    self.nodes_neighbors[neighbor]['infected_neighbors'] -= 1

        self.iteration += 1
        return (len(self.susceptibles), len(self.infecteds), len(self.recovereds))

    def infect(self, infecteds):
        """
            Infect individuals by the given ids
            :param infecteds: ids list of individual to be infected:
        """

        for node in infecteds:
            self.infecteds.append(node)
            self.total_infecteds += 1

            if node in self.recovereds:
                self.recovereds.remove(node)

                for neighbor in self.graph.neighbors(node):
                    self.nodes_neighbors[neighbor]['infected_neighbors'] += 1
            else:
                self.susceptibles.remove(node)

                for neighbor in self.graph.neighbors(node):
                    self.nodes_neighbors[neighbor]['infected_neighbors'] += 1
                    self.nodes_neighbors[neighbor]['susceptible_neighbors'].remove(node)

    def recover(self, recovereds):
        """
            Recover individuals by the given ids
            :param recovereds: ids list of individual to be recovered:
        """

        for node in recovereds:
            self.recovereds.append(node)

            if node in self.infecteds:
                self.infecteds.remove(node)

                for neighbor in self.graph.neighbors(node):
                    self.nodes_neighbors[neighbor]['infected_neighbors'] -= 1
            else:
                self.susceptibles.remove(node)

                for neighbor in self.graph.neighbors(node):
                    self.nodes_neighbors[neighbor]['susceptible_neighbors'].remove(node)


