#Import
#----------------------------------------------------------------------------------------------------------------------------------------------------
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
#----------------------------------------------------------------------------------------------------------------------------------------------------
#Object
#----------------------------------------------------------------------------------------------------------------------------------------------------
hub = PrimeHub()
mm_motor = MotorPair("C","D")
#rmm_motor = MotorPair("B","A")
#right_motor = Motor("C")
#left_motor = Motor("D")
#arm_motor = Motor("E")
col_sensor = ColorSensor("B")
dis_sensor = DistanceSensor("D")
#tail_motor = Motor("E")
#----------------------------------------------------------------------------------------------------------------------------------------------------


#Function definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
def fight_in_circle(sw):
    hub.light_matrix.write("Start")
    wait_for_seconds(1)
    while True:
        mm_motor.move(1, 'cm', steering=180)
        if(col_sensor.get_reflected_light() < 20):
            mm_motor.move(-10, 'cm', 0)
        if(dis_sensor.get_distance_cm() < 10):
            mm_motor.move(2, 'cm', 0)

#start main()

while True:
    hub.left_button.wait_until_pressed()
    fight_in_circle()


