#simulation_project

#headers
from random import seed
from random import randint

from heapq import *
from numpy import random


#initial conditions

#features:

    #Generate cars in random 1 to 5 min ------no,not yet  
    #timer of dt 5 seconds interval -----no because car could arrive in anytime
    #function to change light-------okay
    #Detector to check comming car-------okay
    #car queue function ---------okay

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
        print("\t\t\t\tGREEN\t\tred")
        self.green = True
    def turn_yellow(self):
        """
		The light turns yellow
		"""
        print("\t\t\t\tYELLOW\t\tred")
        self.yellow = True
    def turn_red1(self):
        """
        The light turns red green
        """
        print("\t\t\t\tRED\t\tgreen ")
        self.red = True
    def turn_red2(self):
        """
        The light turn red yellow
        """
        print("\t\t\t\tRED\t\tyellow")
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
            queue.insert(Y2R1(self.t+50))
            queue.insert(R2G(self.t+180))

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

print("cars(time)\t\tmain road signal\tsecondary road signal")
# seed random number generator

class nocar(Event):
    def __init__(self,time):
        self.t = time
        self.name = "nocar"
    def action(self,queue,state):    
        a=5
        b=50
        c=180     
        for x in range(0, 2, 1):
            queue.insert(G2Y(self.t+a))
            queue.insert(Y2R1(self.t+b))
            queue.insert(R2G(self.t+c))
            a=a+180
            b=b+185
            c=c+235

#randomisation part1: number of cars 
additionalNumCarInQueue = random.randint(0,5) 
print("additionalNumCarInQueue")
print(additionalNumCarInQueue)
for i in range(0, additionalNumCarInQueue):
    tRandom = random.randint(0, 240)
    #randomisation part2: time in random
    print("tRandom")
    print(tRandom)
    Q.insert( CAR(tRandom) )


print("cars(time)\t\tmain road signal\tsecondary road signal")

Q.insert(nocar(0))
S = State()

#Main driver
# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = Q.next()
    print( e )
    e.action(Q,S)
