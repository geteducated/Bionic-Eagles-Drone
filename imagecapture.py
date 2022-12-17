from djitellopy import tello
import cv2

me = tello.Tello()#tello named me
me.connect()#this connects to tello
print("Battery life: ", me.get_battery()) #prints battery %

me.streamon() #gives streams one by one

while True: #loops image capture
    img = me.get_frame_read().frame #individual image from drone
    # img = cv2.resize(img, (360,240) #resizing to send img faster
    cv2.imshow("Image", img) #shows img
    cv2.waitKey(1) #allows frame to be visible for set time
