# -*- coding: utf-8 -*-

from GeneticAlgorithm import GeneticAlgorithm
from multiprocessing import Process
from operator import itemgetter
from SIRModel import SIRModel

from igraph import *
import argparse
import random

ag = None
graph = None
beta = None
gamma = None
infected_list = None
vaccinated_list = None

id_name_dict = {}
name_id_dict = {}

def evaluate_population(process_id, num_process):
    # realiza avaliação dos filhos

    ini = ((ag.population_size / num_process) * process_id)
    fim = 0

    if(process_id == (num_process - 1)):
        fim = ((ag.population_size / num_process) * process_id) + (ag.population_size / num_process) + (ag.population_size % num_process)
    else:
        fim = ((ag.population_size / num_process) * process_id) + (ag.population_size / num_process)

    for index in range(ini, fim):

        #olhar como é feita a contagem

        sirmodel = SIRModel(graph, beta, gamma)
        sirmodel.infect(infected_list)
        sirmodel.recover(ag.population[index])

        infecteds = 0
        for i in range(100):
            iteration = sirmodel.iterate()
            # infecteds += iteration[1] + iteration[2]

        # ag.individual_performance[index] = infecteds
        ag.individual_performance[index] = sirmodel.total_infecteds

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    #required args
    parser.add_argument("graph", help = "Network graph representing community interactions")
    parser.add_argument("population_size", help = "Genetic algorithm population size", type = int)
    parser.add_argument("chromosome_size", help = "Number of available vaccines", type = int)

    #optional args
    parser.add_argument("--infecteds", help = "Initial infecteds", type = int, nargs='*')
    parser.add_argument("--vaccinateds", help="Initial vaccinated", type=int, nargs='*')
    # parser.add_argument("--selection_mode", help = "GA's parents select mode", type = int)
    parser.add_argument("--cross_points", help = "Crossover cross points number", type = int)
    parser.add_argument("--mutation", help = "Crossover mutation level", type = float)
    parser.add_argument("--cross_l", help = "Crossover cross probability", type = float)
    parser.add_argument("--generations", help = "Number of generations(ag's iterations)", type = int)
    parser.add_argument("-p", "--percentage_infected", help = "Initial number of infections", type = float)
    parser.add_argument("-b", "--beta", help = "Disease tranmission rate", type = float)
    parser.add_argument("-g", "--gamma", help = "Disease recovery rate", type = float)
    # parser.add_argument("-r", "--result", help = "File with the best individual of the genetic algorithm", type = float)
    parser.add_argument("-e", "--execution", help = "Execution number", type = int)

    args = parser.parse_args()

    graph = Graph.Read_Ncol(sys.argv[1])
    graph.to_undirected(mode="collapse", combine_edges=None)

    for vertex in graph.vs:
        id_name_dict.update({vertex.index : int(vertex['name'])})
        name_id_dict.update({int(vertex['name']) : vertex.index})

    #population_size
    population_size = args.population_size

    #gene_size
    chromosome_size = args.chromosome_size

    # #selecion mode
    # selection_mode = 2

    #cross points
    cross_points = 2

    #mutation
    mutation = 0.05

    #cross level
    cross_l = 0.9

    #generations
    generations = 200

    #percentage_infected
    percentage_infected = 0.05

    #transmission parameters (daily rates scaled to hourly rates)
    beta = 0.2857
    gamma = 0.1428

    execution_number = 0

    fixed = False

    # #arquivo de resultado
    # result = None
    # result_detailed = None
    # result_generation_detailed = None
    # result_conv = None

    # #selection_mode check
    # if(args.selection_mode):
    #     selection_mode = args.selection_mode
    # else:
    #     print " - Assumindo modo de seleção como 2"

    #cross_points check
    if(args.cross_points):
        cross_points = args.cross_points
    else:
        print " - Assumindo pontos de cruzamento como 2"

    #mutation check
    if(args.mutation):
        mutation = args.mutation
    else:
        print " - Assumindo probabilidade de mutação como 5%"

    #generations check
    if(args.cross_l):
        cross_l = args.cross_l
    else:
        print " - Assumindo probabilidade de cruzamento como 90%"

    #generations check
    if(args.generations):
        generations = args.generations
    else:
        print " - Assumindo número de gerações como 200"

    #percentage infected check
    if(args.percentage_infected):
        percentage_infected = args.percentage_infected
    else:
        print " - Assumindo Porcentagem inicial de infectados como 0.5%"

    #beta check
    if(args.beta):
        beta = args.beta
    else:
        print " - Assumindo beta como 0.2857"

    #gamma check
    if(args.gamma):
        gamma = args.gamma
    else:
        print " - Assumindo gamma como 0.1428"

    if(args.execution):
        execution_number = args.execution
    else:
        execution_number = 0

    #result check
    # if(args.result):
    #     result = open(args.result, "a+")
    #     result_detailed = open(args.result.split(".")[0] + "_detailed" + args.result.split(".")[1], "a+")
    #     result_generation_detailed = open(args.result.split(".")[0] + "_generation_detailed" + args.result.split(".")[1], "a+")
    #     result_conv = open(args.result.split(".")[0] + "_average" + args.result.split(".")[1], "a+")
    # else:
    #     print " - Assumindo arquivo de saída como ", args.graph.split(".")[0] + ".result"
    #     result = open(str(args.graph.split(".")[0] + ".result"), "a+")
    #     result_detailed = open(str(args.graph.split(".")[0] + "_detailed.result"), "a+")
    #     result_generation_detailed = open(str(args.graph.split(".")[0] + "_generation_detailed.result"), "a+")
    #     result_conv = open(str(args.graph.split(".")[0] + "_average.result"), "a+")


    # ---------- Início -----------

    #lista de infectados
    infected_list = []
    if(args.infecteds):
        infected_list = args.infecteds[:]
        for i in range(len(infected_list)):
            infected_list[i] = name_id_dict[infected_list[i]]
    else:
        infected_list = random.sample(range(graph.vcount()), int(graph.vcount() * percentage_infected))

    if(args.vaccinateds):
        vaccinated_list = args.vaccinateds[:]

    #cria o ag
    ag = GeneticAlgorithm(population_size, chromosome_size, cross_points, cross_l, mutation, graph.vcount(), infected_list, vaccinated_list)

    print "- GASIR -"
    print "Tamanho da população: ", ag.population_size
    print "Tamanho do gene: ", chromosome_size
    print "Número de infectados: ", len(infected_list), ": ", infected_list
    print "Tamanho da rede:", graph.vcount()

    # #iteração inicial
    # process_list_init = []
    # for pid in range(8):
    #     p0 = Process(target=initial_evaluation, args=(pid, 8))
    #     process_list_init.append(p0)
    #     p0.start()
    #
    # for pid in range(8):
    #     process_list_init[pid].join()


    convergence = open(sys.argv[1] + "_convergence.txt",'a')

    while ag.generation < generations:
        best = 0

        # result_generation_detailed.write(str(ag.generation) + " " + str(ag.best_performance) + " " + str(ag.best) + "\n")

        #realiza seleção dos pais
        ag.parents_select()

        process_list = []
        for pid in range(8):
            p = Process(target=evaluate_population, args=(pid, 8))
            process_list.append(p)
            p.start()

        for pid in range(8):
            process_list[pid].join()

        # print "\nGeração: ", ag.generation
        # print "Melhor: ", ag.best
        # print "Infectados: ", ag.best_performance
        # print " ------------------------ "

        performance_average = 0.0
        for perf in ag.individual_performance:
            performance_average += perf

        # print performance_average/ag.population_size
        convergence.write(str(performance_average/ag.population_size) + "\n")

        # print ag.global_best_performance

    convergence.close()

    best_individuals = []
    for i, fitness in enumerate(ag.individual_performance):
        best_individuals.append([i,fitness])

    best_individuals.sort(key=itemgetter(1))

    best_range = int(population_size * 0.1)

    with open(sys.argv[1] + "_result.txt",'a') as file:
        for i in range(best_range):
            individual = ag.population[best_individuals[i][0]]

            for j in range(len(individual)):
                individual[j] = id_name_dict[individual[j]]

            file.write(str(individual).replace('[','').replace(']','') + '\n')

    # for fitness in best_individuals:
    #     print fitness