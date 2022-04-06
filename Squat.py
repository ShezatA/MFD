import cv2
import time
from cv2 import WINDOW_NORMAL
import Functions as f
import numpy as np
import PoseEstModule as pem

detector = pem.poseDetector()

class Squat():
    def __init__(self, time = 0.0, reps = 0.0, lKnee = 0.0, rKnee = 0.0, hip = 0.0):
        self.time = time
        self.reps = reps
        self.lKnee = lKnee
        self.rKnee = rKnee
        self.hip = hip

    def angles(self, cam):
        self.lKnee = detector.angle(cam, 23, 25, 27)
        if self.lKnee > 180: self.lKnee -= 180

        self.rKnee = detector.angle(cam, 24, 26, 28)
        if self.rKnee > 180: self.rKnee -= 180

        lHip = detector.angle(cam, 11, 23, 25)
        rHip = detector.angle(cam, 12, 24, 26)
        self.hip = (lHip + rHip) / 2
        if self.hip > 180: self.hip -= 180

        print("Left Knee: " + str(self.lKnee))
        print("Right Knee: " + str(self.rKnee))
        print("Hip: " + str(self.hip))

    def kForm(self, angle, name = "Knee"):
        knee = np.interp(angle, (10, 75), (100, 0))
        print(name + " Completion: " + str(knee) + "%")
        return knee

    def hForm(self, angle):
        hip = np.interp(angle, (65, 165), (0, 100))
        print("Hip Completion: " + str(hip) + "%")

        return hip

    def __str__(self):
        return "Time Elapsed: " + str(self.time) + " seconds\nReps: " + str(self.reps)



def main():
    s = Squat()
    done = True
    start = time.time()
    timeReps = []
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Squat Cam", WINDOW_NORMAL)

    while True:
        if not cap.isOpened:
            print("Cannot open webcam :(")
        else:
            ret, cam = cap.read()
            cam = detector.findPose(cam, False)
            lmList = detector.position(cam)

            if(len(lmList) > 0):
                s.angles(cam)
                lkForm = s.kForm(s.lKnee, "Left Knee")
                rkForm = s.kForm(s.rKnee, "Right Knee")
                hForm = s.hForm(s.hip)

                if lkForm == 100 and rkForm == 100:
                    if hForm == 100 and done == False:
                        s.reps += 0.5
                        done = True

                        if s.reps % 1 == 0: 
                            t = time.time()
                            repT = (t - start)
                            timeReps.append(int(repT))
                elif lkForm == 0 and rkForm == 0:
                    if hForm == 0 and done == True:
                        s.reps += 0.5
                        done = False

                        if s.reps % 1 == 0: 
                            t = time.time()
                            repT = (t - start)
                            timeReps.append(int(repT))
                
            print("Reps: " + str(int(s.reps)) + "\n")
            cv2.imshow("Squat Cam", cam)

        if cv2.waitKey(1) > 0:
            end = time.time()
            cap.release()
            cv2.destroyAllWindows()
            break
        
    s.time = (end - start)
    f.out("Squats.txt", "Time Elapsed: " + str(s.time) + " seconds\nReps: " + str(int(s.reps)))
    print(s)
    f.graph(timeReps, "Squats")