#Import
#----------------------------------------------------------------------------------------------------------------------------------------------------
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Object
#----------------------------------------------------------------------------------------------------------------------------------------------------
hub = PrimeHub()
mm_motor = MotorPair("B","A")
right_motor = Motor("A")
left_motor = Motor("B")
r_arm_motor = Motor("C")
l_arm_motor = Motor("E")
col_sensor_l = ColorSensor("D")
col_sensor_r = ColorSensor("F")

#----------------------------------------------------------------------------------------------------------------------------------------------------
#Function definition
#----------------------------------------------------------------------------------------------------------------------------------------------------

def right_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    mm_motor.move_tank(degrees,'degrees',speed,0)
    mm_motor.stop()

def left_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    mm_motor.move_tank(degrees,'degrees',0,speed)
    mm_motor.stop()

def arm_up(arm, degree, speed):
    arm.run_for_degrees(degree, speed)

def gyro_straight_forward_cs_l(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        if(col_sensor_l.get_reflected_light() < 40):
            mm_motor.stop()
            break
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        mm_motor.start_tank_at_power((power + correction), (power - correction))
    mm_motor.stop()

def gyro_straight_forward_cs_r(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        if(col_sensor_r.get_reflected_light() < 40):
            mm_motor.stop()
            break
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        mm_motor.start_tank_at_power((power + correction), (power - correction))
    mm_motor.stop()

def gyro_straight_forward(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        mm_motor.start_tank_at_power((power + correction), (power - correction))
    mm_motor.stop()

def gyro_straight_forward_print(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        print("yaw",hub.motion_sensor.get_yaw_angle())
        mm_motor.start_tank_at_power((power + correction), (power - correction))
    mm_motor.stop()

def pid_turn(target_angle, p_constant, min_power):
    mm_motor.set_stop_action('hold')
    error = target_angle - hub.motion_sensor.get_yaw_angle()
    max_power = 80
    while(error > 3):
        error = target_angle - hub.motion_sensor.get_yaw_angle()
        control_output = error - p_constant
        if(abs(control_output) > max_power):
            control_output = int(max_power * target_angle / abs(target_angle))
        if(abs(control_output) < min_power):
            control_output = int(min_power * target_angle / abs(target_angle))
        mm_motor.start_tank_at_power(control_output, -control_output)
    mm_motor.stop()


#----------------------------------------------------------------------------------------------------------------------------------------------------
#Variable definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
fast_speed = 70 # maximum speed
normal_speed = 50 # normal speed for routine.
slow_speed = 35 #slow speed to control the accuracy
#----------------------------------------------------------------------------------------------------------------------------------------------------
while True:
    hub.right_button.wait_until_pressed()
    hub.motion_sensor.reset_yaw_angle()#Round 1
    gyro_straight_forward_print(-4,85.5,fast_speed)
    arm_up(l_arm_motor,-150, 50)#lift up
    arm_up(l_arm_motor,30, 60)# do not touch bar
    gyro_straight_forward_print(0,22,fast_speed)
    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(0,102,fast_speed+30)
#----------------------------------------------------------------------------------------------------------------------------------------------------    
    hub.right_button.wait_until_pressed()
    hub.motion_sensor.reset_yaw_angle()#Round 2
    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(0,68,fast_speed)#TV

    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(0,12,fast_speed)
    left_turn_motor(180,50)
    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(-45,66,fast_speed)
    pid_turn(45,1,40)

    gyro_straight_forward_print(45,80,fast_speed)#WIND TURBINE
    cnt = 0
    while (cnt < 3):
        cnt = cnt + 1
        mm_motor = MotorPair("A","B")
        gyro_straight_forward_print(45,10,fast_speed)
        mm_motor = MotorPair("B","A")
        gyro_straight_forward_print(45,80,fast_speed+10)

    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(46,36,fast_speed)#put units in TOY FACTORY

    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(46,2,normal_speed)
    left_turn_motor(250,50)
    mm_motor.move(-87,"cm",0,fast_speed+30)
#...............................................................
    hub.right_button.wait_until_pressed()
    hub.motion_sensor.reset_yaw_angle()#Round 3
    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(0,14,fast_speed)

    gyro_straight_forward_print(-46,142,fast_speed)
    right_turn_motor(45,50)
    mm_motor.move(2,"cm",0)
    r_arm_motor.run_for_degrees(-240,50)
    r_arm_motor.run_for_degrees(240,50)#Hybrid car

    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(-45,15,fast_speed+30)
    left_turn_motor(250,50)
    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(-120,40,fast_speed+30)
    gyro_straight_forward_print(-165,55,fast_speed+30)
    gyro_straight_forward_print(-95,95,fast_speed+30)
#...............................................................


#...............................................................
    hub.right_button.wait_until_pressed()
    hub.motion_sensor.reset_yaw_angle() #Round 4
    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(9,80,fast_speed+20)
    gyro_straight_forward_print(0,12,fast_speed+20)
    mm_motor.move(250,"degrees",0,normal_speed)#put units
    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(7,4,normal_speed)#move back slowly
    gyro_straight_forward_print(7,107,fast_speed+20)
#...............................................................
    hub.right_button.wait_until_pressed()
    hub.motion_sensor.reset_yaw_angle()#Dam #Round 5
    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(3,52,fast_speed+20)#
    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(3,58,fast_speed+20)
#.......................................................    
    hub.right_button.wait_until_pressed()
    hub.motion_sensor.reset_yaw_angle()#Round 6

    mm_motor = MotorPair("A","B")
    gyro_straight_forward_print(24,110,fast_speed)

    pid_turn(80,1,40)

    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(80,30,normal_speed)

    i = 0
    while (i < 4):
        i = i + 1
        mm_motor = MotorPair("B","A")
        gyro_straight_forward_print(85,7,normal_speed)

        mm_motor = MotorPair("A","B")
        gyro_straight_forward_print(85,3,normal_speed)

    gyro_straight_forward_print(85,4,normal_speed)
    gyro_straight_forward_print(60,39,normal_speed)
    pid_turn(145,1,40)
    gyro_straight_forward_print(145,37,fast_speed)#put units in the circle

    mm_motor = MotorPair("B","A")
    gyro_straight_forward_print(145,4,normal_speed)#move back

    pid_turn(175,1,60)#178 to 175
    mm_motor.move(50,"cm",0,fast_speed)#lift HI FIVE
#----------------------------------------------------------------------------------------------------------------------------------------------------
   
    
