from djitellopy import tello
import KeyPressModule as kp
import numpy as np
from time import sleep
import time
import cv2
from pyzbar.pyzbar import decode
import math

######## PARAMETERS ###########
fSpeed = 117 / 10  # Forward Speed in cm/s   (15cm/s)
aSpeed = 360 / 10  # Angular Speed Degrees/s  (50d/s)
interval = 0.25
dInterval = fSpeed * interval
aInterval = aSpeed * interval

###############################################

x, y = 500, 500
a = 0
yaw = 0
kp.init()

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

used_code = []

points = [(0, 0), (0, 0)]


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 15

    aspeed = 50

    global x, y, yaw, a

    d = 0

    if kp.getKey("LEFT"):

        lr = -speed

        d = dInterval

        a = -180

    elif kp.getKey("RIGHT"):

        lr = speed

        d = -dInterval

        a = 180

    if kp.getKey("UP"):

        fb = speed

        d = dInterval

        a = 270

    elif kp.getKey("DOWN"):

        fb = -speed

        d = -dInterval

        a = -90

    if kp.getKey("w"):

        ud = speed

    elif kp.getKey("s"):

        ud = -speed

    if kp.getKey("a"):

        yv = -aspeed

        yaw -= aInterval

    elif kp.getKey("d"):

        yv = aspeed

        yaw += aInterval

    if kp.getKey("q"): me.land(); sleep(3)

    if kp.getKey("e"): me.takeoff()

    sleep(interval)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',

                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,

                (255, 0, 255), 1)


while True:

    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((1000, 1000, 3), np.uint8)

    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))

    drawPoints(img, points)
    cv2.imshow("Output", img)

########################################
  


    success, QRimg = me.get_frame_read()
    for qr in decode(QRimg):
        myData = qr.data.decode('UTF-8')  # convets to str
        if qr.data.decode('UTF-8') not in used_code:
            print(qr.data)
            print(myData)
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(QRimg, [pts], True, (255, 0, 200), 2)
            pts2 = qr.rect
            cv2.putText(QRimg, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)
            used_code.append(myData)
            time.sleep(1)
        elif qr.data.decode('UTF-8') in used_code:
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(QRimg, [pts], True, (255, 0, 200), 2)
            pts2 = qr.rect
            cv2.putText(QRimg, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 200), 2)
            print("Alreay seen, try a different qr.")
            time.sleep(0)
        else:
            pass
        if len(used_code) == 5:
            print(used_code)
        else:
            pass
        cv2.imshow("results", QRimg)
    cv2.waitKey(1)