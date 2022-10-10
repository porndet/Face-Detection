import cv2
from deepface import DeepFace
import sys

class FaceDetection:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_default.xml')
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.cap = cv2.VideoCapture(0)

    def CheckCamera(self):
        if not self.cap:
            return False
        else:
            return True

    def VideoCaptrue(self):
        Checkresult = self.CheckCamera()

        if Checkresult:
            while True:
                self.ret, self.img = self.cap.read()

                self.DetectionAI()

                cv2.imshow("Camera 0", self.img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # print("Age : " + str(self.result['age']))
                    # print("Emotion : " + self.result['dominant_emotion'])
                    return False
        else:
            print("No have camera !!!")

    def DetectionAI(self):
        try:
            self.result = DeepFace.analyze(self.img, actions = ['age', 'emotion'])
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.faces = self.face_cascade.detectMultiScale(self.gray, 1.1, 4)
            self.DetectionFace()
        except:
            return False

    def DetectionFace(self, l = 50, s = 7, d = 20):
        for (x , y, w, h) in self.faces:
            x1, y1 = x + w, y + h  
            cv2.rectangle(self.img, (x, y),(x + w, y + h), (255, 0, 255), 1) 

            #Top, Left
            cv2.line(self.img, (x, y), (x + l, y), (255, 0, 255), s)
            cv2.line(self.img, (x, y), (x, y + l), (255, 0, 255), s)

            #Bottom, Left
            cv2.line(self.img, (x, y1), (x + l, y1), (255, 0, 255), s)
            cv2.line(self.img, (x, y1), (x, y1 - l), (255, 0, 255), s)

            #Top, Right
            cv2.line(self.img, (x1, y), (x1 - l, y), (255, 0, 255), s)
            cv2.line(self.img, (x1, y), (x1, y + l), (255, 0, 255), s)

            #Bottom, Right
            cv2.line(self.img, (x1, y1), (x1 - l, y1), (255, 0, 255), s)
            cv2.line(self.img, (x1, y1), (x1, y1 - l), (255, 0, 255), s)

            cv2.putText(self.img, self.result['dominant_emotion'] + " " + str(self.result['age']), (x, y - d), self.font, 2, (255, 0, 255), 2)


    def __call__(self):
        self.VideoCaptrue()

    def __repr__(self):
        return f'{self.result["dominant_emotion"]} {str(self.result["age"])}'