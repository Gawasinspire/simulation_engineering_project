#simulation_project

#headers

from heapq import *
from numpy import random


#initial conditions

#overall Functions

    #Generate cars in random 1 to 5 min 
    #timer of dt 5 seconds interval
    #function to change light
    #Detector to check comming car
    #car queue function 

#states:
    # main road states
    # secondary road states
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
        print("green")
        self.green = True
    def turn_yellow():
        """
		The light turns yellow
		"""
        print("yellow")
        self.yellow = True
    def turn_red(self):
        """
        The light turns red
        """
        print("red")
        self.red = True
    def __str__(self):
        """
        Displays the status of the crossroads
        """
        return "Green light =" + str(self.green) + ", cars=" + str(self.cars)

#events
    #main events
    #secondary events

#main drivers
    


### STATE ##########################################


### EVENTS ###########################################

Tc = 30 # Time latency to change the traffic lights from red to green once a car is found waiting in the queue
Tp = 10 # Passage time

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
        if not state.is_green():
            state.add_car()
            if state.waiting_cars() == 1:
                queue.insert(R2G(self.t+Tc))

class R2G(Event):
    def __init__(self,time):
        self.t = time
        self.name = "R2G"
    def action(self,queue,state):
        queue.insert( G2R( self.t + state.waiting_cars() * Tp ) )
        state.turn_green()
        state.purge_cars()

class G2R(Event):
    def __init__(self,time):
        self.t = time
        self.name = "G2R"
    def action(self,queue,state):
        state.turn_red()

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

Q.insert( CAR(74) ) 
Q.insert( CAR(75) )

# For advanced sim , uncomment these lines
#random.seed(1)
#additionalNumCarInQueue=100
#tRandom = 80
#for i in range(1, additionalNumCarInQueue):
#    tRandom = random.randint(tRandom+1, tRandom+10)
#    Q.insert( CAR(tRandom) )  
    

S = State()

#Main driver
# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = Q.next()
    print( e )
    e.action(Q,S)


# What to display or sample display

#print main road () 
#print secondary road ()
#print car status