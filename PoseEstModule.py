import cv2
import math as m
import mediapipe as mp

class poseDetector():

    def __init__(self, statMode = False, upper = False, smooth = True, detCon = 0.5, trackCon = 0.5):
        self.statMode = statMode
        self.upper = upper
        self.smooth = smooth
        self.detCon = detCon
        self.trackCon = trackCon


        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self, self.statMode, self.upper, self.smooth, self.detCon, self.trackCon)


    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
                    
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                      
        return img

    def position(self, img):
        self.lmList = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                height, width, channel = img.shape
                lmX = int(lm.x * width)
                lmY = int(lm.y * height)
                self.lmList.append([id, lmX, lmY])

        return self.lmList

    def angle(self, img, lm1, lm2, lm3):
        x1, y1 = self.lmList[lm1][1:]
        x2, y2 = self.lmList[lm2][1:]
        x3, y3 = self.lmList[lm3][1:]

        angle = m.degrees(m.atan2(y3 - y2, x3 - x2) - m.atan2(y1 - y2, x1 - x2))

        if angle < 0: angle += 360
        cv2.circle(img, (x1, y1), 5, (255, 255, 255), 3, cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 255, 255), 3, cv2.FILLED)
        cv2.circle(img, (x3, y3), 5, (255, 255, 255), 3, cv2.FILLED)

        return angle
