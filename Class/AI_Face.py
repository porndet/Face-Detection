import cv2
from deepface import DeepFace
import sys
from datetime import datetime

class FaceDetection:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_eye.xml')
        self.eyeLeft_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_lefteye_2splits.xml')
        self.eyeRight_cascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_righteye_2splits.xml')
        self.mouth_cascade = cv2.CascadeClassifier('./data/haarcascades/Mouth.xml')
        self.nose_cascade = cv2.CascadeClassifier('./data/haarcascades/Nariz.xml')
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.cap = cv2.VideoCapture(0)
        self.colorGreen = (0, 255, 0)
        self.filenameFormat = "{:s}/{:s}-{:%Y%m%d_%H%M%S}.{:s}"
        self.EXTENSION = 'jpg'

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

                # date = datetime.now()
                # outfile = self.filenameFormat.format("Face", "Face", date, self.EXTENSION)
                # cv2.imwrite(outfile, self.roi_img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return False
        else:
            print("No have camera !!!")

    def DetectionAI(self):
        try:
            self.result = DeepFace.analyze(self.img, actions = ['age', 'emotion'])
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.DetectionFace()
            self.DetectionEyeLeft()
            # self.DectectionEye()
            # self.DectectionMouth()
            # self.DectectionNose()
        except:
            return False

    def DetectionFace(self, l = 50, s = 7, d = 20):
        self.faces = self.face_cascade.detectMultiScale(self.gray, 1.2, 10)

        for (x , y, w, h) in self.faces:
            x1, y1 = x + w, y + h  

            self.roi_img = self.img[y : y + h, x : x + w]

            # date = datetime.now()
            # outfile = self.filenameFormat.format("Face", "Face", date, self.EXTENSION)
            # cv2.imwrite(outfile, self.roi_img)

            cv2.rectangle(self.img, (x, y), (x + w, y + h), self.colorGreen, 1) 

            #Top, Left
            cv2.line(self.img, (x, y), (x + l, y), self.colorGreen, s)
            cv2.line(self.img, (x, y), (x, y + l), self.colorGreen, s)

            #Bottom, Left
            cv2.line(self.img, (x, y1), (x + l, y1), self.colorGreen, s)
            cv2.line(self.img, (x, y1), (x, y1 - l), self.colorGreen, s)

            #Top, Right
            cv2.line(self.img, (x1, y), (x1 - l, y), self.colorGreen, s)
            cv2.line(self.img, (x1, y), (x1, y + l), self.colorGreen, s)

            #Bottom, Right
            cv2.line(self.img, (x1, y1), (x1 - l, y1), self.colorGreen, s)
            cv2.line(self.img, (x1, y1), (x1, y1 - l), self.colorGreen, s)

            cv2.putText(self.img, self.result['dominant_emotion'] + " " + str(self.result['age']), (x, y - d), self.font, 2, (0, 255, 0), 2)

    def DetectionEyeLeft(self):
        self.EyeLeft = self.eyeLeft_cascade.detectMultiScale(self.roi_img, 1.1, 4)
        for (x , y, w, h) in self.EyeLeft:
            cv2.rectangle(self.roi_img, (x, y),(x + w, y + h), (255, 255, 0), 1) 

    # def DectectionEye(self):
    #     self.Eye = self.eye_cascade.detectMultiScale(self.roi_img, 1.1, 12)
    #     for index, (x , y, w, h) in enumerate(self.Eye):

    #         if index == 0:
    #             eyeLeftimage = self.roi_img[y : y + h, x : x + w]
    #             date = datetime.now()
    #             outfile = self.filenameFormat.format("EyeLeft", "EyeLeft", date, self.EXTENSION)
    #             cv2.imwrite(outfile, eyeLeftimage)

    #         else:
    #             eyeRightimage = self.roi_img[y : y + h, x : x + w]
    #             date = datetime.now()
    #             outfile = self.filenameFormat.format("EyeRight", "EyeRight", date, self.EXTENSION)
    #             cv2.imwrite(outfile, eyeRightimage)

    #         cv2.rectangle(self.roi_img, (x, y),(x + w, y + h), (255, 255, 0), 1) 

    def DectectionMouth(self):
        self.Mouth = self.mouth_cascade.detectMultiScale(self.roi_img, 1.1, 8)
        for (x , y, w, h) in self.Mouth:
            mouthimage = self.roi_img[y : y + h, x : x + w]

            date = datetime.now()
            outfile = self.filenameFormat.format("Mouth", "Mouth", date, self.EXTENSION)
            cv2.imwrite(outfile, mouthimage)

            cv2.rectangle(self.roi_img, (x, y),(x + w, y + h), (255, 0, 0), 1) 

    def DectectionNose(self):
        self.Nose = self.nose_cascade.detectMultiScale(self.roi_img, 1.1, 8)
        for (x , y, w, h) in self.Nose:
            noseimage = self.roi_img[y : y + h, x : x + w]

            date = datetime.now()
            outfile = self.filenameFormat.format("Nose", "Nose", date, self.EXTENSION)
            cv2.imwrite(outfile, noseimage)

            cv2.rectangle(self.roi_img, (x, y),(x + w, y + h), (0, 255, 255), 1) 

    def __call__(self):
        self.VideoCaptrue()

    def __repr__(self):
        return f'{self.result["dominant_emotion"]} {str(self.result["age"])}'