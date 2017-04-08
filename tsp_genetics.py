import math
import random
from math import radians, cos, sin, asin, sqrt

cities = []

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
	
#def crossover(dna):


#def mutation(dna):
	
	
	
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


	print "Iterating over the generations :"
	
