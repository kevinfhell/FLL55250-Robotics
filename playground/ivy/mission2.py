from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()

hub.light_matrix.show_image('HAPPY')
m_motor = MotorPair('B', 'A')
color = ColorSensor('F')
right_motor = Motor('A')

def line_follow(distance):
    print("follow black line")
    right_motor.set_degrees_counted(0)
    while(right_motor.get_degrees_counted() < distance / 17.5 * 360):
        if color.get_color() == 'black':
            m_motor.start_tank_at_power(40,20)
        else:
            m_motor.start_tank_at_power(20,40)


def right_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    mm_motor.move_tank(degrees,'degrees',speed,0)
    mm_motor.stop()


m_motor.move(17, 'in', 0, 30)
m_motor.move_tank(10, 'cm', 30, -30)
print(color.get_color())
if(color.get_color() == 'white'):
    line_follow(22.5, 'inch')
    m_motor.move_tank(10, 'cm', -30, 30)
    loop_time = 4
    While True:
        if(loop_time == 0):
            break:
        loop_time = loop_time - 1
        m_motor.move(7,'inch',0,50)
        m_motor.move(-7,'inch',0,50)
else:
    print("I'm done")


