import cv2
import numpy as np
import math
import time
from channels.generic.websocket import WebsocketConsumer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VideoStreamConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.configure_volume_control()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        frame = self.decode_frame(text_data)
        processed_frame = self.process_frame(frame)
        self.send(text_data=self.encode_frame(processed_frame))

    def configure_volume_control(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        volRange = self.volume.GetVolumeRange()
        self.minVol = volRange[0]
        self.maxVol = volRange[1]

    def process_frame(self, frame):
        detector = hand_detect(detectionCon=0.7)
        img = detector.find_hand(frame)
        lmlist = detector.find_hand_posistion(img)

        if len(lmlist) != 0:
            p, q = lmlist[4][1], lmlist[4][2]
            r, s = lmlist[8][1], lmlist[8][2]
            center_x, center_y = (p + r) // 2, (q + s) // 2
            cv2.circle(img, (p, q), 8, (255, 200, 0), cv2.FILLED)
            cv2.circle(img, (r, s), 8, (255, 200, 0), cv2.FILLED)
            cv2.line(img, (p, q), (r, s), (255, 200, 0), 3)
            cv2.circle(img, (center_x, center_y), 12, (255, 200, 0), cv2.FILLED)

            length = math.hypot(r - p, s - q)

            vol = np.interp(length, [50, 250], [self.minVol, self.maxVol])
            volBAR = np.interp(length, [50, 250], [350, 150])
            volPer = np.interp(length, [50, 250], [0, 100])
            self.volume.SetMasterVolumeLevel(vol, None)

            if length < 50:
                cv2.circle(img, (center_x, center_y), 12, (100, 255, 0), cv2.FILLED)

            cv2.putText(img, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)
            cv2.rectangle(img, (50, 130), (85, 350), (100, 230, 0), 2)
            cv2.rectangle(img, (50, int(volBAR)), (85, 350), (230, 150, 0), 2, cv2.FILLED)

        return img

    def encode_frame(self, frame):
        return cv2.imencode('.jpg', frame)[1].tobytes()

    def decode_frame(self, data):
        return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

class hand_detect:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def find_hand(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_hand_posistion(self, img, handNo=0, draw=True):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for hand_id, landmark in enumerate(myHand.landmark):
                height, width, channel = img.shape
                center_x_axis, centre_y_axis = int(landmark.x * width), int(landmark.y * height)
                landmark_list.append([hand_id, center_x_axis, centre_y_axis])
                if draw:
                    cv2.circle(img, (center_x_axis, centre_y_axis), 6, (200, 200, 120), cv2.FILLED)
        return landmark_list