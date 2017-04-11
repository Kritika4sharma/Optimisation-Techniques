import math
import random
import numpy as np
from math import radians, cos, sin, asin, sqrt
import sys

old = sys.stdout      # required if we need to print output in a file

cities = []           # storage for cities
curr_pop = []         # current population
num_of_cities = 0     # number of cities

INF = 9999999
POP_SIZE = 50         # size of population
NUM_OF_GEN = 1500     # number of iterations for evolution


# to calculate distance from geometrical coordinates using haversine formula
def haversine(lat1, lat2, lon1, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

# selection using roulette wheel algorithm
def selection_by_roulette_wheel(pop):
	wt_sum = sum((ind[1] for ind in pop))
	n = random.uniform(0,wt_sum)
	su = 0
	for ind,wt in pop:
		su = su + wt
		if(n<su):
			return ind
	return ind

# selection using tournament selection algoriithm
def tournamentSelection(pop):
	tournament_size = 5          # tournament size to be assumed
	fittest = []
	maxi = INF

    # randomly generate 5 candidates and taking fittest of those 
	for i in range(0,tournament_size):
		ind = (int)(random.random()*len(pop))   
		if(pop[ind][1]<maxi):
			maxi = pop[ind][1]
			fittest = pop[ind][0]
	return fittest

# class for storing city
class City:
	x = 0.0     # x coordinate 
	y = 0.0     # y coordinate
	index = 0   # index to refer to a city (in this code not so useful, can ignore)
	
	def __init__(self,index,x=None,y=None):
		self.x = x
		self.y = y
		self.index = index
			
	def getIndex(self):
		return self.index	

	def getCoordinates(self):
		return self.x,self.y
		
# this is order crossover algorithm
def crossover(dna1,dna2): 
	child1 = [0]*len(dna1)        # child1 initialised
	child2 = [0]*len(dna2)        # child2 initialised

	# choosing two crossover points randomly
	start = int(random.random()*len(dna1))
	end = int(random.random()*len(dna2))

	if(start>end):
		temp = start
		start = end
		end = temp
	
	# generating first child
	vis = np.zeros(len(dna1)+10)    # visited array to check used elements in next step
	for i in range(start,end+1):    # copying the substring from first parent to first child
		child1[i] = dna1[i]
		vis[dna1[i]] = 1
	ini = (end+1)%len(dna1)
	
	for i in range(end+1,len(dna2)):   # copying the unused elements from second parent to first child
		if(vis[dna2[i]]==0):
			child1[ini] = dna2[i]
			ini = (ini+1)%len(dna2)
			vis[dna2[i]] = 1

	for i in range(0,end+1):
		if(vis[dna2[i]]==0):
			child1[ini] = dna2[i]
			ini = (ini+1)%len(dna2)
			vis[dna2[i]] = 1

    # generating second child
	vis2 = np.zeros(len(dna2)+10)
	for i in range(start,end+1):    # copying the substring from second parent to second child
		child2[i] = dna2[i]
		vis2[dna2[i]] = 1
	ini = (end+1)%len(dna2)
	
	for i in range(end+1,len(dna1)):    # copying the unused elements from first parent to second child
		if(vis2[dna1[i]]==0):
			child2[ini] = dna1[i]
			ini = (ini+1)%len(dna1)
			vis2[dna1[i]] = 1
	for i in range(0,end+1):
		if(vis2[dna1[i]]==0):
			child2[ini] = dna1[i]
			ini = (ini+1)%len(dna1)
			vis2[dna1[i]] = 1

	return child1,child2


# swap mutation method 
def mutation(path):
	chance = 9
	for pos1 in range(0,len(path)):
		if int(random.random()*chance)==1:           # only swap if a probability is satisfied
			pos2 = (int)(len(path)*random.random())  # getting second random position in path 
            # swaping pos1 gene with the gene at pos2
			temp = path[pos1]
			path[pos1] = path[pos2]
			path[pos2] = temp
		
	return path


# this is fitness value calculating hamiltonian distance of path
def fitness(path):
	su = 0
	l1 = len(path)
	for i in range(1,l1):
		c1 = cities[path[i]]
		c2 = cities[path[i-1]]
		c1x,c1y = c1.getCoordinates()
		c2x,c2y = c2.getCoordinates()
		su = su + haversine(c1x,c2x,c1y,c2y)

	c1 = cities[path[len(path)-1]]
	c2 = cities[path[0]]
	c1x,c1y = c1.getCoordinates()
	c2x,c2y = c2.getCoordinates()
	su = su + haversine(c1x,c2x,c1y,c2y)
	return su


# print the path
def print_path(path):
	for i in range(0,len(path)):
		print path[i],
	print fitness(path)," "
	
	
# print all the paths present in the current population
def print_population(pop):
	for i in range(0,len(pop)):
		print_path(pop[i])


# printing data for all the cities present in dataset 
def print_cities():
	for city in cities:
		print city.index, " ",city.x," ",city.y
	print ""

	
if __name__ == '__main__':
	
	print "Creating the cities :"

	ind  = 0
	initial = []    # initial dna (encoded using permutation representation) 

	# creating the cities
	with open("burma14.txt") as input_file:             # reading the datasetfile "burma14" whose optimal value is : 3323 
		for line in input_file:
			line = line.strip()
			coord =  line.split()
			city = City(ind,float(coord[0]),float(coord[1]))
			cities.append(city)                         # add city to the collection of cities 
			initial.append(ind)                         # add entry of city to the initial permutation
			ind  = ind + 1
			
	num_of_cities = len(cities)                         # number of cities present in dataset

	print "Length of initial parent taken",fitness(initial)

	curr_pop.append(initial)
	for i in range(0,POP_SIZE-1):                       # generation of random population
		temp = []
		for j in range(0,len(initial)):
			temp.append(initial[j])
		random.shuffle(temp)                            # shuffle initial path to get different permutations
		curr_pop.append(temp)

	print "Iterating over the generations :"
	
	#sys.stdout = open("generations.txt", "w")          # required if need to print output in a file

	for generation in xrange(NUM_OF_GEN):               # iteration over generations
		weighted_pop = []                               # population along with their fitness
		print "Generation ",generation                  # printing the generation number
	       	for individual in curr_pop:
	       		value = fitness(individual)
	       		pair = (individual,float(value))        # making the pair of path and its fitness value
	       		weighted_pop.append(pair)

		popu = []

		for i in xrange(POP_SIZE/2):
			# selection of two random individuals using any selection algorithm
			ind1 = tournamentSelection(weighted_pop)
			ind2 = tournamentSelection(weighted_pop)
			
			# Crossover of the obtained individuals
			ind1, ind2 = crossover(ind1, ind2)

			# Mutate and add back into the population.
			popu.append(mutation(ind1))
			popu.append(mutation(ind2))
			
		curr_pop = popu                                # updating the current population to the newly obtained one

	#Now find out the most optimal string among the remaining individuals in the population
	fittest_string = curr_pop[0]
	minimum_fitness = fitness(curr_pop[0])

	for individual in curr_pop:
		ind_fitness = fitness(individual)
		if ind_fitness <= minimum_fitness:
			fittest_string = individual
			minimum_fitness = ind_fitness

	print "Optimal value of the given function: %d" % minimum_fitness 
	print "Optimal value is at : ",
	print_path(fittest_string)

