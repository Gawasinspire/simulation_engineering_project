#simulation_project

#headers
from random import seed
from random import randint
from heapq import *
from numpy import random

"""
#initial conditions
simulation time 20 minutes = 1200 seconds
yellow= 5 + red =55 + green=180/= 240
1200/240= 5 for simplicity
traffic signals from yellow red green if and only if car detected 
in green then changes immediatly to yellow and continues
"""
simulation_time=5

#states:

class State:
    def __init__(self):
        self.red = True
        self.green = False
        self.yellow = False
        self.cars = 0
    def is_green(self):
        """
        True if the light is green
        """
        return self.green
    def is_red(self):
    	"""
    	True if the light is red
    	"""
    	return self.red
    def is_yellow(self):
    	"""
    	True if the light is yellow
    	"""	
    	return self.yellow
    def add_car(self):
        """
        Adds a car in the queue
        """
        self.cars = self.cars + 1
    def purge_cars(self):
        """
        Empty waiting cars
        """
        self.cars = 0
    def waiting_cars(self):
        """
        Returns the number of car waiting
        """
        return self.cars
    def turn_green(self):
        """
        The light turns green
        """
        #print("\033[0;31;40m Red\033[0;32;40m Green\033[1;33;40m Yellow\033[0;37;40m")
        print("\t\t\t\t\033[0;32;40m Green\t\t\033[0;31;40m Red\033[0;37;40m")
        self.green = True
    def turn_yellow(self):
        """
		The light turns yellow
		"""
        print("\t\t\t\t\033[1;33;40m Yellow\t\t\033[0;31;40m Red\033[0;37;40m")
        self.yellow = True
    def turn_red1(self):
        """
        The light turns red green
        """
        print("\t\t\t\t\033[0;31;40m Red\t\t\033[0;32;40m Green\033[0;37;40m")
        self.red = True
    def turn_red2(self):
        """
        The light turn red yellow
        """
        print("\t\t\t\t\033[0;31;40m Red\t\t\033[1;33;40m Yellow\033[0;37;40m")
    def __str__(self):
        """
        Displays the status of the crossroads
        """
        return "Green light =" + str(self.green) + ", cars=" + str(self.cars)
 
### EVENTS ###########################################

class Event:
    def time(self):
        """
        Returns the time at which the event will be processed
        """
        return self.t
    def __str__(self):
        """
        Displays Event
        """
        return self.name + "(" + str( self.t ) + ")"
    def __lt__(self, other):
        """
        Compares the event with another sorted by processing order priority
        """
        return self.t < other.t
    
class CAR(Event):
    def __init__(self,time):
        self.t = time
        self.name = "CAR"
    def action(self,queue,state):
        if state.is_green():
            state.add_car()
            print("Detector:car detected in green")
            queue.next()
            queue.next()
            queue.next()
            queue.insert(G2Y(self.t+5))
            queue.insert(Y2R1(self.t+55))
            queue.insert(R2G(self.t+240))

class R2G(Event):
    def __init__(self,time):
        self.t = time
        self.name = "R2G"
    def action(self,queue,state):
        state.turn_green()        

class G2Y(Event):
    def __init__(self,time):
        self.t = time
        self.name = "G2Y"
    def action(self,queue,state):
        state.turn_yellow()

class Y2R1(Event):
    def __init__(self,time):
        self.t = time
        self.name = "Y2R"
    def action(self,queue,state):
        state.turn_red1()
        queue.insert(Y2R2(self.t+5))

class Y2R2(Event):
    def __init__(self,time):
        self.t = time
        self.name = "Y2R"
    def action(self,queue,state):
        state.turn_red2()

### EVENT QUEUE ##############################################

class EventQueue:
  def __init__(self):
      self.q = []
  def notEmpty(self):
      """
      Returns true if the queue is not empty
      """
      return len(self.q) > 0
  def remaining(self):
      """
      Returns the number of events awaiting processing
      """
      return len(self.q)
  def insert(self, event):
      """ 
      Create a new event in the queue
      """
      heappush( self.q, event )
  def next(self):
      """
      Returns and removes from the queue the next event to be processed
      """
      return heappop( self.q )


### MAIN #####################################################

Q = EventQueue()

# seed random number generator

class nocar(Event):
    def __init__(self,time):
        self.t = time
        self.name = "nocar"
        
    def action(self,queue,state):    
        a=5
        b=50
        c=180
        queue.insert(CAR(961) )
        print("Defined time for car1:961")
        for i in range(0, additionalNumCarInQueue):
            tRandom = random.randint(0,100)
            print("Random time for car"+ str(i+2)+":"+str(tRandom))
            queue.insert( CAR(tRandom) )
        print("cars(EventEndTime)\tmain road signal\tsecondary road signal")
        for x in range(0, simulation_time, 1):
            self.t=self.t+a
            queue.insert(G2Y(self.t))
            self.t=self.t+b
            queue.insert(Y2R1(self.t))
            self.t=self.t+c+5
            queue.insert(R2G(self.t))
            
#randomisation part1: number of cars 
additionalNumCarInQueue = random.randint(0,5) +1
print('additionalNumCarInQueue:' + str(additionalNumCarInQueue) )

Q.insert(nocar(0))

S = State()

print("\033[0;31;40m Red\033[0;32;40m Green\033[1;33;40m Yellow\033[0;37;40m")
#Main driver
# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = Q.next()
    print( e )
    e.action(Q,S)
