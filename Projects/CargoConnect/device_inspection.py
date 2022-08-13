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
right_motor = Motor("C")
left_motor = Motor("D")
arm_motor = Motor("E")
col_sensor = ColorSensor("B")
#dis_sensor = DistanceSensor("D")
#tail_motor = Motor("E")
#----------------------------------------------------------------------------------------------------------------------------------------------------


#Function definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
def gyro_inspection(sw):
    hub.motion_sensor.reset_yaw_angle()
    hub.light_matrix.write("Start")
    hub.light_matrix.write("Turn Robot")
    wait_for_seconds(1)
    while sw > 0:
        sw = sw-1
        hub.status_light.on('blue')
        wait_for_seconds(1)
        hub.status_light.off()
        print("sw=",sw)
        if(hub.motion_sensor.get_yaw_angle() != 0):
            hub.light_matrix.write("Good")
        if(sw == 0) and (hub.motion_sensor.get_yaw_angle() == 0):
            hub.status_light.on("red")
            hub.light_matrix.write("N")
        if(sw == 0) and (hub.motion_sensor.get_yaw_angle() != 0):
            hub.status_light.on('green')
            hub.light_matrix.write("Y")

#start main()
gyro_inspection(3)
