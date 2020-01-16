
from threading import Thread
import time
import sys
import random
from itertools import cycle
"""

#features:

    #Generate cars in random 0 to 5 min ------ok
    #function to change light-----------------ok
    #Detector to check comming car------------ok
    #car queue function ----------------------ok
    #continuation of change in lights---------ok
    #time to control the speed to simulation--ok    

"""


lights = {"Green": 0, "Yellow": 1, "Red": 2}
main_street_light_state = "Green"
second_street_light_state = "Red"
global_timer = 0
stop_controller = False
car_detected = False
simulation_time = 1000
controller_speed=  0.001
# class definition
class event:
    def __str__(self):
        return "event class"
    next_event = -1
    duration = -1
    def set_lights(self, main_street, second_street):
        global main_street_light_state, second_street_light_state
        main_street_light_state = main_street
        second_street_light_state = second_street

class g2y(event):
    def __str__(self):
        return "g2y"
    duration = 180
    def set_lights(self):
        super().set_lights("Green", "Red")

class y2r(event):
    def __str__(self):
        return "y2r"
    duration = 5
    def set_lights(self):
        super().set_lights("Yellow", "Red")


class r2g1(event):
    def __str__(self):
        return "r2g1"
    duration = 50
    def set_lights(self):
        super().set_lights("Red", "Green")

class r2g2(event):
    def __str__(self):
        return "r2g2"
    duration = 5
    def set_lights(self):
        super().set_lights("Red", "Yellow")

def controller(event):
    global global_timer, stop_controller, car_detected
    actual_event = event
    relative_time = 0
    print(str(actual_event))
    print("Main_sig:  second_sig timestamp timer")
    while True:
        if stop_controller:
            break
        global_timer += 1
        relative_time += 1
        print( main_street_light_state +"\t\t" +second_street_light_state + "\t" + str(global_timer) + "\t " + str(relative_time))
        #if(str(actual_event)=="g2y"):
            #print("a:"+str(actual_event))
        if car_detected and (str(actual_event)=="g2y"):
                print("Detector: Car detected in Green!")
                #print(str(actual_event))
                actual_event = actual_event.next_event()
                #print(str(actual_event))
                relative_time = 0
                actual_event.set_lights()
                car_detected = False
        elif relative_time >= actual_event.duration:
            print(str(actual_event))
            relative_time = 0
            actual_event = actual_event.next_event()
            actual_event.set_lights()
        time.sleep(controller_speed)

g2y.next_event = y2r
y2r.next_event = r2g1
r2g1.next_event = r2g2
r2g2.next_event = g2y

#lst = [g2y,y2r,r2g1,r2g2]

#pool = cycle(lst)


light_controller = Thread(target=controller, args=((g2y(),)))
#to start the thread
light_controller.daemon = True
 
car_list=[0]            
car_list.clear()  

#randomisation part1: number of cars 
additionalNumCarInQueue = random.randint(0,5) +1
print('additionalNumCarInQueue:' + str(additionalNumCarInQueue) )

#randomisation part2: number of cars 
Start = 1
#car in 0 to 5 mins
Stop = 300
limit = additionalNumCarInQueue

car_list = [random.randint(Start, Stop) for iter in range(limit)]

print("cars:"+str(car_list))
#car_list = [291]
light_controller.start()
car_detected_set = False
while(global_timer < simulation_time):
    if global_timer in car_list and car_detected_set != global_timer:
        car_detected = True
        car_detected_set = global_timer
stop_controller = True
print("Total simulation time"+str(global_timer))
sys.exit(0)

