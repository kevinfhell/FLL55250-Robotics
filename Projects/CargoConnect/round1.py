#Import
#----------------------------------------------------------------------------------------------------------------------------------------------------
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Object
#----------------------------------------------------------------------------------------------------------------------------------------------------
hub = PrimeHub()
mm_motor = MotorPair("A","B")
#rmm_motor = MotorPair("B","A")
right_motor = Motor("B")
left_motor = Motor("A")
arm_motor = Motor("F")
col_sensor = ColorSensor("C")
dis_sensor = DistanceSensor("D")
tail_motor = Motor("E")
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Function definition
#----------------------------------------------------------------------------------------------------------------------------------------------------

def right_turn(degrees,speed,reset):
    mm_motor.set_default_speed(speed)
    if(reset == 1):
        hub.motion_sensor.reset_yaw_angle()
    while(hub.motion_sensor.get_yaw_angle()<degrees):
        mm_motor.start(100)
    mm_motor.stop()

def reset_turn():
    mm_motor.set_default_speed(normal_speed)
# hub.motion_sensor.reset_yaw_angle()
    while(hub.motion_sensor.get_yaw_angle()>0):
        mm_motor.start(-100)
    mm_motor.stop()

def right_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    mm_motor.move_tank(degrees,'degrees',speed,0)
    mm_motor.stop()

def left_turn(degrees,speed,reset):
    mm_motor.set_default_speed(speed)
    if(reset == 1):
        hub.motion_sensor.reset_yaw_angle()
    while((-hub.motion_sensor.get_yaw_angle())<degrees):
        print(hub.motion_sensor.get_yaw_angle())
        mm_motor.start(-100)
    mm_motor.stop()

def left_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    mm_motor.move_tank(degrees,'degrees',0,speed)
    mm_motor.stop()

def line_follow(speed,m_reflect):
    print("line follow")
    mm_motor.set_default_speed(speed)
    while True:
        mm_motor.start((m_reflect-col_sensor.get_reflected_light())*2)
        if(col_sensor.get_color() == 'red'):
            mm_motor.stop()

def move_arm_up(degree,speed):
    print("Move arm up")
    arm_motor.run_for_degrees(degree,speed)

def move_tail_arm_up(degree,speed):
    print("Move arm up")
    tail_motor.run_for_degrees(-degree,speed)


def move_arm_down(degree,speed):
    print("Move arm down")
    arm_motor.run_for_degrees(-degree,speed)

def move_tail_arm_down(degree,speed):
    print("Move tail arm down")
    tail_motor.run_for_degrees(degree,speed)


def move_arm_down_turbo():
    print("Move up down with maximum power and speed")
    arm_motor.start_at_power(100)
    arm_motor.run_for_degrees(-360,100)

def gyro_straight_forward_cs(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        if(col_sensor.get_reflected_light() < 40):
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

def gyro_straight_backward(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        rmm_motor.start_tank_at_power((power + correction), (power - correction))
    rmm_motor.stop()

def pid_turn(target_angle, p_constant, min_power):
    hub.motion_sensor.reset_yaw_angle()
    mm_motor.set_stop_action('hold')
    error = target_angle - hub.motion_sensor.get_yaw_angle()
    max_power = 100
    while(error != 0):
        error = target_angle - hub.motion_sensor.get_yaw_angle()
        control_output = error - p_constant
        if(abs(control_output) > max_power):
            control_output = max_power * target_angle / abs(target_angle)
        if(abs(control_output) < min_power):
            control_output = min_power * target_angle / abs(target_angle)
        mm_motor.start_at_power(control_output, -control_output)
    mm_motor.stop()

def pid_line_follow(kp,ki,kd,distance):
    last_err = 0
    integral = 0
    motor_power = 27
    target_light = 80
    right_motor.set_degrees_counted(0)
    while(right_motor.get_degrees_counted() < distance / 17.5 * 360):
        error = target_light - col_sensor.get_reflected_light()
        integral = error + integral
        derivative = error - last_err
        correction = (error * kp) + (integral * ki) + (derivative * kd)
        mm_motor.start_tank_at_power((power + correction), (power - correction))
        last_err = error
    mm_motor.stop()

#----------------------------------------------------------------------------------------------------------------------------------------------------
#Variable definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
switch_flag = 0 # use as a local variable to switch between round1 and round3
fast_speed = 70 # maximum speed
normal_speed = 50 # normal speed for routine.
slow_speed = 35 #slow speed to control the accuracy
middle_reflection = 80 # used for the line follower or accurate positioning.
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Execution
hub.light_matrix.show_image('HAPPY')
#Round 1 start
#wait_for_seconds(1)
hub.motion_sensor.reset_yaw_angle()
arm_motor.run_for_rotations(0.3)
mm_motor = MotorPair("B","A")
gyro_straight_forward_print(0,113,normal_speed)
left_turn_motor(99,slow_speed)
gyro_straight_forward(-52,70,normal_speed)
mm_motor.move(200,"degrees",0)
mm_motor = MotorPair("A","B")
mm_motor.move(130,"degrees",0)
right_turn(0,30,0)
mm_motor.move(200,"degrees",0)
wait_for_seconds(1)
while True:
    if(dis_sensor.get_distance_cm() > 22):
        mm_motor.start(0,-10)
    if(dis_sensor.get_distance_cm() <= 22):
        mm_motor.stop()
        break
wait_for_seconds(1)
left_turn_motor(186,slow_speed)
arm_motor.run_for_rotations(-1.1)
wait_for_seconds(1)
while True:
    if(dis_sensor.get_distance_cm() > 19):
        mm_motor.start(0,-10)
    if(dis_sensor.get_distance_cm() <= 19):
        mm_motor.stop()
        break
wait_for_seconds(1)
mm_motor = MotorPair("A","B")
gyro_straight_forward_print(-92,37,slow_speed-10)
wait_for_seconds(1)
arm_motor.set_default_speed(slow_speed-20)
arm_motor.run_for_rotations(0.8)
while True:
    if(dis_sensor.get_distance_cm() > 41):
        mm_motor.start(0,-10)
    if(dis_sensor.get_distance_cm() <= 41):
        mm_motor.stop()
        break
#mm_motor.move(-2,"cm",0)
#wait_for_seconds(1)
#mm_motor.move(15,"degrees",normal_speed)
right_turn_motor(170,normal_speed)
gyro_straight_forward(0,88,normal_speed)
left_turn_motor(70,normal_speed)
gyro_straight_forward(0,120,normal_speed)
#left_turn_motor(60,slow_speed)
#mm_motor.move(8,"cm",0)
#gyro_straight_forward(-1,80,normal_speed)
#Round 1 end
