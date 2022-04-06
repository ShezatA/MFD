import cv2
import time
from cv2 import WINDOW_NORMAL
import Functions as f
import numpy as np
import PoseEstModule as pem

detector = pem.poseDetector()

class Pushup():
    def __init__(self, time = 0.0, reps = 0.0, lElbow = 0.0, rElbow = 0.0, hip = 0.0):
        self.time = time
        self.reps = reps
        self.lElbow = lElbow
        self.rElbow = rElbow
        self.hip = hip

    def angles(self, cam):
        self.lElbow = detector.angle(cam, 11, 13, 15)
        if self.lElbow > 180: self.lElbow -= 180

        self.rElbow = detector.angle(cam, 12, 14, 16)
        if self.rElbow > 180: self.rElbow -= 180

        lHip = detector.angle(cam, 11, 23, 25)
        rHip = detector.angle(cam, 12, 24, 26)
        self.hip = (lHip + rHip) / 2

        print("Left Elbow: " + str(self.lElbow))
        print("Right Elbow: " + str(self.rElbow))
        if self.hip < 160: print("Straighten Back! Hip Angle: " + str(self.hip))

    def eForm(self, angle, name):
        x = np.interp(angle, (85, 120), (0, 100))
        print(name + " Completion: " + str(x) + "%")
        return x

    def __str__(self):
        return "Time Elapsed: " + str(self.time) + " seconds\nReps: " + str(self.reps)



def main():
    p = Pushup()
    done = True
    start = time.time()
    timeReps = []
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Pushup Cam", WINDOW_NORMAL)
            
    while True:
        if not cap.isOpened:
            print("Cannot open webcam :(")
        else:
            ret, cam = cap.read()
            cam = detector.findPose(cam, False)
            lmList = detector.position(cam)

            if(len(lmList) > 0):
                p.angles(cam)
                leForm = p.eForm(p.lElbow, "Left Elbow")
                reForm = p.eForm(p.rElbow, "Right Elbow")

                if leForm == 100 and reForm == 100 and p.hip > 160:
                    if done == False:
                        p.reps += 0.5
                        done = True

                        if p.reps % 1 == 0: 
                            t = time.time()
                            repT = (t - start)
                            timeReps.append(int(repT))
                elif leForm == 0 and reForm == 0 and p.hip > 160:
                    if done == True:
                        p.reps += 0.5
                        done = False

                        if p.reps % 1 == 0: 
                            t = time.time()
                            repT = (t - start)
                            timeReps.append(int(repT))

            print("Reps: " + str(int(p.reps)) + "\n")
            cv2.imshow("Pushup Cam", cam)

        if cv2.waitKey(1) > 0:
            end = time.time()
            cap.release()
            cv2.destroyAllWindows()
            break

    p.time = (end - start)
    f.out("Pushups.txt", "Time Elapsed: " + str(p.time) + " seconds\nReps: " + str(int(p.reps)))
    print(p)
    f.graph(timeReps, "Pushups")
    