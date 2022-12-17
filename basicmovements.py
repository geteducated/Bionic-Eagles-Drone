from djitellopy import tello
from time import sleep

me = tello.Tello()#tello named me
me.connect()#this connects to tello
print(me.get_battery()) #prints battery

me.move_forward() #in cm
me.takeoff()
me.send_rc_control(0,50,0,0)#fwd @ speed50
sleep(2) #flys for 2sec
me.send_rc_control(50,0,0,0)#right @ speed50
sleep(2) #flys for 2sec
me.send_rc_control(0,0,50,0)#up @ speed50
sleep(2)#flys for 2sec
me.send_rc_control(0,0,0,50)#yaw @ speed50
sleep(2) #flys for 2sec
me.send_rc_control(0,0,0,0)#stops
me.land()
