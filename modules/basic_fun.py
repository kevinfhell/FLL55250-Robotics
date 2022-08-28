# This is the module for all the reusable functions in Lego Spike Prime
#Import




#variable

motors = MotorPair('C', 'D')
timer = Timer()

#Functions




#Gyro turn


def gyro_turn(degree):

    hub.motion_sensor.reset_yaw_angle()

    while hub.motion_sensor.get_yaw_angle() < degree:
        motors.start(100, 20)

    motors.stop()


def gyro_turn_acc(degree):
    
    hub.motion_sensor.reset_yaw_angle()
    while timer.now() < 6:
        angle = hub.motion_sensor.get_yaw_angle()
        motors.start(95,degree-angle)



