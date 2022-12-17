
from djitellopy import tello
import KeyPressModule as kp
import numpy as np
import cv2
import math
import time
from time import sleep
from pyzbar.pyzbar import decode

##########PARAMETERS ##########
#need speed and angular speed to calc distance
fSpeed = 117/10 # Forward speed in cm/s, actual(15cm/s)
aSpeed = 360/10 # Angular speed in Degrees/s (50rads/s)
interval = 0.25

dInterval = fSpeed*interval # distance per unit
aInterval = aSpeed*interval # angle per unit
###################################
x, y = 500, 500 # starting point, origin = (500,500)
a = 0 # angle is always 0 so it doesn't keep adding to itself
yaw = 0

kp.init()
global imgCap

me = tello.Tello()#tello named me
me.connect()#this connects to tello
me.streamon() #gives streams one by one
print(me.get_battery()) #prints battery

### video capturing for QR code
#img = cv2.imread('1.png')
# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

# used_code = []

points = [(0,0), (0,0)]


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 15
    aspeed = 50
    global x, y, yaw, a
    d = 0 # distance is inside loop to keep adding/tracking

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180


    if kp.getKey("w"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("s"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("UP"):
        ud = speed
    elif kp.getKey("DOWN"):
        ud = -speed

    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval

    if kp.getKey("q"):
        me.land()
    if kp.getKey("e"):
        me.takeoff()

    if kp.getKey('z'): #saving images
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg' ,imgCap) #saves images without writing over with timestamp
        time.sleep(0.3)

    sleep(interval)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

def drawPoints(Mapimg, points):
    for point in points:
        cv2.circle(Mapimg, point, 5, (0,0,255), cv2.FILLED)
    cv2.circle(Mapimg, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(Mapimg, f'({(points[-1][0]-500)/100},{(points[-1][1]-500)/100})m',
                (points[-1][0]+10, points[-1][1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1) #coordinate of distance traveled


while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    Mapimg = np.zeros((1000, 1000, 3), np.uint8)  # creating black image, a matrix of 8-bit pixels
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))
    drawPoints(Mapimg, points)
    cv2.imshow("Mapping Output", Mapimg)
    #cv2.waitKey(1)

    imgCap = me.get_frame_read().frame  # individual image from drone
    imgCap = cv2.resize(imgCap, (360, 240))  # resizing to send img faster
    cv2.imshow("Image", imgCap)  # shows img
    cv2.waitKey(1)  # allows frame to be visible for set time

