import math
import cv2
import time
import numpy as np
# import Hand_track as htm
# from Hand_track import hand_detect

# pycaw modules
# https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import mediapipe as mp
import time
import threading 

class hand_detect():
    stop = 1
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        #by default dtection percentage is set to 50% ,  user can increease and decrease it while create an object of the class 
        self.trackCon = trackCon
        #by default tracking percentage is set to 50% ,  user can increease and decrease it while create an object of the class 
        # traking is easier than detection . So we always perform detection first
        
        self.mpHands = mp.solutions.hands
        # self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    
    # detection of hand 
    def find_hand(self,img,draw=True):
        self.imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)
        # print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
            
        return img
    
    # traking of the hand
    def find_hand_posistion(self,img,handNo=0,draw=True):
        landmark_list = [] # it will store all the land marks  while tracking 
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for hand_id, landmark in enumerate(myHand.landmark):
                # print(hand_id, landmark)
                height, width , channel = img.shape 
                center_x_axis, centre_y_axis = int(landmark.x*width) , int(landmark.y*height)
                # print(hand_id,center_x_axis,centre_y_axis)
                landmark_list.append([hand_id,center_x_axis,centre_y_axis])
                if draw:
                    cv2.circle(img,(center_x_axis,centre_y_axis),6,(200,200,120),cv2.FILLED)
                    # cv2.line(img,(center_x_axis,centre_y_axis),7,(120,100,120),cv2.FILLED)
        return landmark_list
    
        




def main():
    cam = cv2.VideoCapture(0)
    h_cam,w_cam = 1200,720
    cam.set(3, w_cam)
    cam.set(4, h_cam)
    pTime = 0
    detector = hand_detect(detectionCon=0.7)
    # pycaw ------------------------------------------
    #pycaw module allows us to control volume of the pc
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange()
    # volume.SetMasterVolumeLevel(-10, None)
    #set variables-----------------------------------
    minVol = volRange[0]
    maxVol = volRange[1]
    vol=0
    volBAR =400
    volPer = 0
    try : 
        while True:
            success, img = cam.read()
            img = detector.find_hand(img)
            lmlist = detector.find_hand_posistion(img)
            if len(lmlist) != 0:
                print(lmlist[4],lmlist[8])

                p, q = lmlist[4][1],lmlist[4][2]
                # and thumb finger landmark is [8][1]
                r, s = lmlist[8][1],lmlist[8][2]
                # calculate the center of index and thumb finge
                center_x,center_y= (p+r)//2, (q+s)//2
                #  draw the circles
                cv2.circle(img,(p,q),8,(255,200,0),cv2.FILLED)
                cv2.circle(img,(r,s),8,(255,200,0),cv2.FILLED)
                cv2.line(img,(p,q),(r,s),(255,200,0),3)
                cv2.circle(img,(center_x,center_y),12,(255,200,0),cv2.FILLED)

                length = math.hypot(r-p,s-q)

                vol = np.interp(length,[50,250],[minVol,maxVol])   
                volBAR = np.interp(length,[50,250],[350,150])
                volPer = np.interp(length,[50,250],[0,100])
                # print("volPer : " ,volPer)
                volume.SetMasterVolumeLevel(vol,None)
                if(length < 50 ):                                                                  
                    cv2.circle(img,(center_x,center_y),12,(100,255,0),cv2.FILLED)

                cv2.putText(img, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)  
                
                # drawing the volume bar 
                cv2.rectangle(img,(50,130),(85,350),(100,230,0),2)
                cv2.rectangle(img,(50,int(volBAR)),(85,350),(230,150,0),2,cv2.FILLED)
                cTime = time.time()
                fps = 1 / (cTime-pTime)
                pTime = cTime
                cv2.putText(img, f'FPS:{int(fps)}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)


            cv2.imshow("Cam Video",img)
            key = cv2.waitKey(1) & 0xFF

            # Check if the 'q' key was pressed
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
        cv2.destroyAllWindows()

    except Exception as e:
        print("An error occur : ", e)


if __name__ == "__main__":
    main()