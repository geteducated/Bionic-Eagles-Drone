
from djitellopy import Tello
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
me = Tello()
me.connect()
print("Battery Life: ", me.get_battery())
# global img

me.streamoff()
me.streamon() #gives streams one by one
# me.get_frame_read
# me.frame

### video capturing for QR code
# cap = cv2.VideoCapture(me.get_frame_read)
# cap.set(3,640)
# cap.set(4,480)

used_code = []

points = [(0,0), (0,0)]

# def getKeyboardInput():
#     lr, fb, ud, yv = 0, 0, 0, 0
#
#     speed = 15
#     aspeed = 50
#     global x, y, yaw, a
#     d = 0 # distance is inside loop to keep adding/tracking
#
#     if kp.getKey("LEFT"):
#         lr = -speed
#         d = dInterval
#         a = -180
#
#     elif kp.getKey("RIGHT"):
#         lr = speed
#         d = -dInterval
#         a = 180
#
#
#     if kp.getKey("w"):
#         fb = speed
#         d = dInterval
#         a = 270
#
#     elif kp.getKey("s"):
#         fb = -speed
#         d = -dInterval
#         a = -90
#
#     if kp.getKey("UP"):
#         ud = speed
#     elif kp.getKey("DOWN"):
#         ud = -speed
#
#     if kp.getKey("a"):
#         yv = -aspeed
#         yaw -= aInterval
#
#     elif kp.getKey("d"):
#         yv = aspeed
#         yaw += aInterval
#
#     if kp.getKey("q"):
#         me.land()
#     if kp.getKey("e"):
#         me.takeoff()
#
#     # if kp.getKey('z'): #saving images
#     #     cv2.imwrite(f'Resources/Images/{time.time()}.jpg' ,imgCap) #saves images without writing over with timestamp
#     #     time.sleep(0.3)
#
#     sleep(interval)
#     a += yaw
#     x += int(d*math.cos(math.radians(a)))
#     y += int(d*math.sin(math.radians(a)))
#
#     return [lr, fb, ud, yv, x, y]

# def drawPoints(Mapimg, points):
#     for point in points:
#         cv2.circle(Mapimg, point, 5, (0,0,255), cv2.FILLED)
#     cv2.circle(Mapimg, points[-1], 8, (0, 255, 0), cv2.FILLED)
#     cv2.putText(Mapimg, f'({(points[-1][0]-500)/100},{(points[-1][1]-500)/100})m',
#                 (points[-1][0]+10, points[-1][1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1) #coordinate of distance traveled

while True:
    # vals = getKeyboardInput()
    # me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    #
    # Mapimg = np.zeros((1000, 1000, 3), np.uint8)  # creating black image, a matrix of 8-bit pixels
    # if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
    #     points.append((vals[4], vals[5]))
    # drawPoints(Mapimg, points)
    # cv2.imshow("Mapping Output", Mapimg)
    #cv2.waitKey(1)

    # img = me.get_frame_read().frame  # individual image from drone
    # img = cv2.resize(img, (360, 240))  # resizing to send img faster
    # cv2.imshow("Image", img)  # shows img
    # cv2.waitKey(1)  # allows frame to be visible for set time

    img = me.get_frame_read().frame
    for qr in decode(img):
        myData = qr.data.decode('UTF-8')  # convets to str
        if qr.data.decode('UTF-8') not in used_code:
            print(qr.data)
            print(myData)
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 200), 2)
            pts2 = qr.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)
            used_code.append(myData)
            time.sleep(1)
        elif qr.data.decode('UTF-8') in used_code:
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 200), 2)
            pts2 = qr.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)
            print("Alreay seen, try a different qr.")
            time.sleep(0)
        else:
            pass
        if len(used_code) == 5:
            print(used_code)
        else:
            pass
        cv2.imshow("results", img)
        cv2.waitKey(1)
