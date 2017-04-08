import math
import random
import numpy as np
from math import radians, cos, sin, asin, sqrt

cities = []
city_to_index = {}

POP_SIZE = 200
NUM_OF_GEN = 100000

# to calculate distance from geometrical coordinates
def haversine(lat1, lat2, lon1, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


def selection_by_roulette_wheel(pop):
	wt_sum = sum((ind[1] for ind in pop))
	n = random.uniform(0,wt_sum)
	su = 0
	for ind,wt in pop:
		su = su + wt
		if(n<su):
			return ind
	return ind


class City:
	x = 0.0     # x coordinate 
	y = 0.0     # y coordinate
	index = 0
	
	def __init__(self,index,x=None,y=None):
		if(x==None):
			self.x = random.random()*100	
		else:
			self.x = x
		if(y==None):
			self.y = random.random()*100	
		else:
			self.y = y

		self.index = index
			
	def getIndex(self):
		return self.index	

	def getCoordinates(self):
		return self.x,self.y
		
	def distanceTo(self,city):	
		x1,y1 = self.getCoordinates()
		x2,y2 = city.getCoordinates()
		xdiff = (int)(abs(x1-x2))
		ydiff = (int)(abs(y1-y2))
		return sqrt(xdiff*xdiff + ydiff*ydiff)
	
	
class Tour:
	path = []
	distance = 0

	def __init__(self,path):
		self.path = path
	
	# to calculate the tsp distance of the current tour
	def getDistance(self):
		su = 0
		l1 = len(self.path)
		for i in range(1,l1):
			c1 = cities[self.path[i]]
			c2 = cities[self.path[i-1]]
			c1x,c1y = c1.getCoordinates()
			c2x,c2y = c2.getCoordinates()
			su = su + haversine(c1x,c2x,c1y,c2y)

		c1 = cities[self.path[len(self.path)-1]]
		c2 = cities[self.path[0]]
		c1x,c1y = c1.getCoordinates()
		c2x,c2y = c2.getCoordinates()
		su = su + haversine(c1x,c2x,c1y,c2y)
		return su


class Population:

	def __init__(self):
		self.population = []

	def save_path(self,path):
		#print_path(path)
		self.population.append(path)

	def print_population(self):
		for i in range(0,len(self.population)):
			print_path(self.population[i])
	

# order crossover used
def crossover(dna1,dna2):
	child1 = dna1
	child2 = dna2
	# choosing two crossover points randomly
	start = int(random.random()*len(dna1))
	end = int(random.random()*len(dna2))

	#print len(dna1)," -- ",len(dna2)

	vis = np.zeros(len(dna1)+10)
	for i in range(start,end+1):    # copying the substring from first parent to first child
		child1[i] = dna1[i]
		vis[dna1[i]] = 1
	ini = (end+1)%len(dna1)
	for i in range(end+1,len(dna2)):   # copying the unused elements from second parent to first child
		if(vis[dna2[i]]==0):
			child1[ini] = dna2[i]
			#print "entere ",ini
			ini = (ini+1)%len(dna2)
			#print "exit ",ini
			vis[dna2[i]] = 1

	for i in range(0,end+1):
		if(vis[dna2[i]]==0):
			child1[ini] = dna2[i]
			#print "entere2 ",ini
			ini = (ini+1)%len(dna2)
			#print "exit2 ",ini
			vis[dna2[i]] = 1


	vis = np.zeros(len(dna1)+10)
	for i in range(start,end+1):    # copying the substring from second parent to second child
		child2[i] = dna2[i]
		vis[dna2[i]] = 1
	ini = (end+1)%len(dna1)
	for i in range(end+1,len(dna1)):    # copying the unused elements from first parent to second child
		if(vis[dna1[i]]==0):
			child2[ini] = dna1[i]
			ini = (ini+1)%len(dna1)
			vis[dna1[i]] = 1
	for i in range(0,end+1):
		if(vis[dna1[i]]==0):
			child2[ini] = dna1[i]
			ini = (ini+1)%len(dna1)
			vis[dna1[i]] = 1

	return child1,child2


# swap mutation method is used
def mutation(path):
	chance = 30
	for pos1 in range(0,len(path)):
		if int(random.random()*chance)==1:
			#print "yy"
			pos2 = (int)(len(path)*random.random())  # getting second randome position in path 
			
			temp = path[pos1]
			path[pos1] = path[pos2]
			path[pos2] = temp

	return path


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


def print_tour(tour):
	for i in range(0,len(tour.path)):
		print tour.path[i],
	print ""

def print_path(path):
	for i in range(0,len(path)):
		print path[i],
	print " "

	
if __name__ == '__main__':
	
	print "Creating the cities :"

	ind  = 0
	
	initial = []    # initial dna (encoded using permutation representation) 

	# creating the cities
	with open("burma14.txt") as input_file:
		for line in input_file:
			line = line.strip()
			coord =  line.split()
			#print len(coord),#" ",coord[1]

			city = City(ind,float(coord[0]),float(coord[1]))
			cities.append(city)
			initial.append(ind)
			city_to_index[city] = ind
			ind  = ind + 1

	print "length of cities : ",len(cities)

	# printing the cities along with coordinates
	for i in range(0,len(cities)):
		ind  = cities[i].getIndex()
		cx,cy = cities[i].getCoordinates()
		print ind,"--> ",cx," ",cy

	print "\n"

	tour = Tour(initial)
	print "Total distance for the current tour : ",tour.getDistance()

	pop = Population()

	for i in range(0,POP_SIZE):
		temp = []
		for j in range(0,len(tour.path)):
			temp.append(tour.path[j])
		random.shuffle(temp)
		pop.save_path(temp)

	print "Size of population is :",len(pop.population)

	print "Population individuals are :"
	pop.print_population()

	'''print "Testing mutation :"
	for i in range(0,len(pop.population)):
		pp = pop.population[i]
		print_path(pp)
		pp = mutation(pp)
		print_path(pp)
		print ""'''

	'''print "Testing Crossover :"
	pp = pop.population[0]
	pp2 = pop.population[1]
	print_path(pp)
	print_path(pp2)
	print ""
	pp,pp2 = crossover(pp,pp2)
	print_path(pp)
	print_path(pp2)'''
	

	print "Iterating over the generations :"

	for generation in xrange(NUM_OF_GEN):               # iteration over generations
		weighted_pop = []         # population along with their fitness
		print "Generation ",generation
       
       	for individual in pop.population:
       		value = fitness(individual)
       		if value == 0:
       			pair = (individual, 1.0)
       		elif value<0:
       			pair = (individual,(-1)*value)	
       		else:
       			pair = (individual,1/float(value))

			weighted_pop.append(pair)

		popu = []

		for i in xrange(POP_SIZE/2):

			# selection of two random individuals using any selection algorithm
			ind1 = selection_by_roulette_wheel(weighted_pop)
			ind2 = selection_by_roulette_wheel(weighted_pop)

			# Crossover of the obtained individuals
			ind1, ind2 = crossover(ind1, ind2)

			# Mutate and add back into the population.
			popu.append(mutation(ind1))
			popu.append(mutation(ind2))

		pop.population = popu


	#Now find out the most optimal string among the remaining individuals in the population
	fittest_string = pop.population[0]
	minimum_fitness = fitness(pop.population[0])

	for individual in pop.population:
		ind_fitness = fitness(individual)
		if ind_fitness <= minimum_fitness:
			fittest_string = individual
			minimum_fitness = ind_fitness

	print "Optimal value of the given function: %d" % minimum_fitness 
	print "Optimal value is at : %s" % print_path(fittest_string)

