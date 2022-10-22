import cv2
from deepface import DeepFace
from datetime import datetime

class FaceDetection:
    def __init__(self):

        self.haarcascades = {
            'face':  cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_default.xml'), 
            'eye': cv2.CascadeClassifier('./data/haarcascades/haarcascade_eye.xml'),
            'eyeleft': cv2.CascadeClassifier('./data/haarcascades/haarcascade_lefteye_2splits.xml'),
            'eyeright': cv2.CascadeClassifier('./data/haarcascades/haarcascade_righteye_2splits.xml'),
            'mouth': cv2.CascadeClassifier('./data/haarcascades/Mouth.xml'),
            'nose': cv2.CascadeClassifier('./data/haarcascades/Nariz.xml')
        }

        self.cascadefile = {
            'eyeleft': cv2.CascadeClassifier('./data/cascade-files/haarcascade_mcs_lefteye.xml'),
            'eyeright': cv2.CascadeClassifier('./data/cascade-files/haarcascade_mcs_righteye.xml'),
            'mouth': cv2.CascadeClassifier('./data/cascade-files/haarcascade_mcs_mouth.xml'),
            'nose': cv2.CascadeClassifier('./data/cascade-files/haarcascade_mcs_nose.xml')            
        }

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

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return False
        else:
            print("No have camera !!!")

    def DetectionAI(self):
        try:
            self.result = DeepFace.analyze(self.img, actions = ['age', 'emotion'])
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.DetectionFace()
            self.DectectionEye()
            self.DectectionMouth()
            self.DectectionNose()
        except:
            return False

    def DetectionFace(self, l = 50, s = 7, d = 20):
        self.faces = self.haarcascades['face'].detectMultiScale(self.gray, 1.2, 10)

        for (x , y, w, h) in self.faces:
            x1, y1 = x + w, y + h

            self.roi_img = self.img[y : y + h, x : x + w]

            self.date = datetime.now()
            outfile = self.filenameFormat.format("Face", "Face", self.date, self.EXTENSION)
            cv2.imwrite(outfile, self.roi_img)

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

    def DectectionEye(self):
        self.Eye = self.haarcascades['eye'].detectMultiScale(self.roi_img, 1.7, 8)
        roieye_img = self.roi_img

        for (x, y, w, h) in self.Eye:
            cv2.rectangle(roieye_img, (x, y),(x + w, y + h), (255, 255, 0), 1)
        else:
            if len(self.Eye) == 1:
                print("No can't detection left or right Eye")
            else:
                if self.Eye[0][0] > self.Eye[1][0]:
                    xr, yr, wr, hr = self.Eye[0]
                    xl, yl, wl, hl = self.Eye[1]

                    EyeRight_Image = self.roi_img[yr : yr + hr, xr : xr + wr]
                    outfile = self.filenameFormat.format("EyeRight", "EyeRight", self.date, self.EXTENSION)
                    cv2.imwrite(outfile, EyeRight_Image)

                    EyeLeft_Image = self.roi_img[yl : yl + hl, xl : xl + wl]
                    outfile = self.filenameFormat.format("EyeLeft", "EyeLeft", self.date, self.EXTENSION)
                    cv2.imwrite(outfile, EyeLeft_Image)

    def DectectionMouth(self):
        self.Mouth = self.cascadefile['mouth'].detectMultiScale(self.roi_img, 1.7, 8)
        roimouth_img = self.roi_img

        for (x , y, w, h) in self.Mouth:
            mouthimage = self.roi_img[y : y + h, x : x + w]

            outfile = self.filenameFormat.format("Mouth", "Mouth", self.date, self.EXTENSION)
            cv2.imwrite(outfile, mouthimage)

            cv2.rectangle(roimouth_img, (x, y),(x + w, y + h), (255, 0, 0), 1) 

    def DectectionNose(self):
        self.Nose = self.cascadefile['nose'].detectMultiScale(self.roi_img, 1.7, 4)
        roinose_img = self.roi_img

        for (x , y, w, h) in self.Nose:
            noseimage = self.roi_img[y : y + h, x : x + w]

            outfile = self.filenameFormat.format("Nose", "Nose", self.date, self.EXTENSION)
            cv2.imwrite(outfile, noseimage)

            cv2.rectangle(roinose_img, (x, y),(x + w, y + h), (0, 255, 255), 1) 

    def __call__(self):
        self.VideoCaptrue()

    def __repr__(self):
        return f'{self.result["dominant_emotion"]} {str(self.result["age"])}'