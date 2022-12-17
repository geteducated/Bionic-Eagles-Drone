
from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
print("Battery Life: ", me.get_battery())
global img

me.streamon() #gives streams one by one

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("w"): fb = speed
    elif kp.getKey("s"): fb = -speed

    if kp.getKey("UP"): ud = speed
    elif kp.getKey("DOWN"): ud = -speed

    if kp.getKey("a"): yv = -speed
    elif kp.getKey("d"): yv = speed

    if kp.getKey("q"): me.land()
    if kp.getKey("e"): me.takeoff(); #time.sleep(.01)

    if kp.getKey('z'): #saving images
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg' ,img) #saves images without writing over with timestamp
        time.sleep(0.3)

    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = me.get_frame_read().frame  # individual image from drone
    img = cv2.resize(img, (360,240)) #resizing to send img faster
    cv2.imshow("Image", img) #shows img
    cv2.waitKey(1) #allows frame to be visible for set time
