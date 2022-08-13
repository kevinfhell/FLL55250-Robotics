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
    print("Move arm down")
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
switch_flag = 1
#hub.right_button.wait_until_pressed()
#hub.light_matrix.write('2')
print("Round2")
#Round 2 start
mm_motor = MotorPair("A","B")
wait_for_seconds(1)
hub.motion_sensor.reset_yaw_angle()
move_arm_down_turbo()
gyro_straight_forward(0,52,normal_speed)#step1
right_turn_motor(30,slow_speed)#step2
gyro_straight_forward(30,52,normal_speed+20)
mm_motor = MotorPair("B","A")
#gyro_straight_forward(40,3,normal_speed)
move_arm_up(200,fast_speed)
move_tail_arm_down(-120,fast_speed)
gyro_straight_forward(40,15,normal_speed)
move_arm_down(200,fast_speed)
gyro_straight_forward(40,10,slow_speed)
move_arm_up(180,fast_speed)
#left_turn_motor(55,normal_speed)
#mm_motor.move(-3,"cm",normal_speed)
#move_arm_down_turbo()
gyro_straight_forward(90,80,fast_speed)
print("Round2 end!!!")
#Round 2 end
