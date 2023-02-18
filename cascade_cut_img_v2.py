import matplotlib.pyplot as plt
import cv2
import sys
import dataclasses
import datetime
import databasen1

path = "C:/xampp/htdocs/dashboard/Website_Project"

class Data:
    cascade_face = "./data/haarcascades/haarcascade_frontalface_alt2.xml" # 顔
    cascade_mouth = "./data/cascade-files/haarcascade_mcs_mouth.xml" # 口
    cascade_eye = "./data/cascade-files/haarcascade_eye.xml" # 目
    cascade_nose = "./data/cascade-files/haarcascade_mcs_nose.xml" # 鼻
    black_img = "./black.jpg"
    
    
def get_time_name(count):
    """時間を画像名にする関数　（重複を避けるために画像名にcountを足す）

    Args:
        count (int): 何回目の検出か

    Returns:
        String : 画像名
    """
    time = datetime.datetime.now()
    time_now = time.strftime('%Y_%m_%d_%H%M%S%m_')
    name = str( time_now + str(count))
    
    return name


def create_draw_img(draw_list: list, get_color_point, face_img, count, face_path):
    """切り出し箇所を塗りつぶす関数

    Args:
        draw_list (list): 塗り潰し対象の座標情報が入った2重list
        get_color_point (list): 鼻の座標　
        face_img (img): 顔画像
        count: 検出回数
    """
    if get_color_point:
        color_list = list(face_img[get_color_point[0], get_color_point[1]]) # BGR
        # print("色　", color_list)
        color = (int(color_list[0]), int(color_list[1]), int(color_list[2])) # BGR 
        # print("変換　", color)
       
    else:
        color = (255, 255, 255)
    
    for inner_list in draw_list:
        point_from = inner_list[0]
        work_size = inner_list[1]
        
        cv2.rectangle(face_img, point_from, work_size, color, thickness=-1)
    draw_name = get_time_name(count)
    # cv2.rectangle(face_img, draw_point, box, (255, 255, 255), thickness=-1)
    cv2.imwrite('../img/draw_face/draw_face' +  draw_name + '.jpg', face_img)
    cv2.imwrite(path + '/img/draw_face/draw_face' +  draw_name + '.jpg', face_img)
    draw_path = str('./img/draw_face/draw_face' +  draw_name + '.jpg')
    
    databasen1.database_input('temp', 'face', 0, 0, face_path, draw_path)
        

cascade_face = cv2.CascadeClassifier(Data.cascade_face)
cascade_mouth = cv2.CascadeClassifier(Data.cascade_mouth)
cascade_eye = cv2.CascadeClassifier(Data.cascade_eye)
cascade_nose = cv2.CascadeClassifier(Data.cascade_nose)

black_img = cv2.imread(Data.black_img)


draw_color_point = ""

cap = cv2.VideoCapture(1)
count = 0

databasen1.Deletedatabase('temp')

while True:
    ret, frame = cap.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_list = cascade_face.detectMultiScale(img_gray, minSize=(100,100))
    draw_list = [] # 塗りつぶし箇所
    if not len(face_list) == 0:
        count += 1
       
        x = face_list[0][0]
        y = face_list[0][1]
        w = face_list[0][2]
        h = face_list[0][3]
        
        test_x = x
        test_y = y
        
        point_from = (x, y)
        work_size = (x + w, y + h)
        inner_list = [point_from, work_size]
        draw_list.append(inner_list)
        
        face_img = frame[y : y + h, x : x + w]
        face_name = get_time_name(count)
        
        face_path = str('./img/face/face_' + face_name + '.jpg')
        
        cv2.imwrite('../img/face/face_' + face_name + '.jpg', face_img) # 顔写真
        cv2.imwrite(path + '/img/face/face_' +  face_name + '.jpg', face_img)
        
        img_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        # 鼻
        nose_list = cascade_nose.detectMultiScale(img_gray, scaleFactor=1.3, minNeighbors=4, minSize=(65,65))
        # print("鼻　", nose_list)/
        if len(nose_list) == 0:
            nose_name = get_time_name(count)
            draw_point = (0, 0)
            cv2.imwrite ('../img/nose/nose_' + nose_name + '.jpg', black_img)
            cv2.imwrite(path + '/img/nose/nose_' +  nose_name + '.jpg', black_img)
            nose_path = str('./img/nose/nose_' + nose_name + '.jpg')
            databasen1.database_input('temp', 'nose', 0, 0, nose_path)
            
        else:
            x = nose_list[0][0]
            y = nose_list[0][1]
            w = nose_list[0][2]
            h = nose_list[0][3]
            
            
            
            draw_color_point = [x - 50 , y + 40] # 塗り潰しカラー座標
            draw_point = (x, y)
            box = (x - 50, y + 100)
            point_from = (x, y)
            work_size = (x + w, y + h)
            inner_list = [point_from, work_size]
            draw_list.append(inner_list)
            
            nose_img = face_img[y : y + h, x : x + w]
            nose_name = get_time_name(count)
            
            cv2.imwrite('../img/nose/nose_' +  nose_name + '.jpg',nose_img)
            cv2.imwrite(path + '/img/nose/nose_' +  nose_name + '.jpg', nose_img)
            nose_path = str('./img/nose/nose_' + nose_name + '.jpg')

            databasen1.database_input('temp', 'nose', int(x), int(y), nose_path)
            
        #口
        mouth_list = cascade_mouth.detectMultiScale(img_gray,  1.7, 8)
        # mouth_list = Data.cascade_mouth1.detectMultiScale(img_gray,  scaleFactor=1.2, minNeighbors=7 ,minSize=(65,65))
        # print("口　", mouth_list)
        if len(mouth_list) == 0:
            # print("きた")
            mouth_name = get_time_name(count)
            cv2.imwrite ('../img/mouth/mouth_' + mouth_name + '.jpg', black_img)
            cv2.imwrite(path + '/img/mouth/mouth_' +  mouth_name + '.jpg', black_img)
            mouth_path = str('./img/mouth/mouth_' +  mouth_name + '.jpg')
            databasen1.database_input('temp', 'mouth', 0, 0, mouth_path)
            
        else:
            x = mouth_list[0][0]
            y = mouth_list[0][1]
            w = mouth_list[0][2]
            h = mouth_list[0][3]
            
            point_from = (x, y)
            work_size = (x + w, y + h)
            inner_list = [point_from, work_size]
            draw_list.append(inner_list)
            
            mouth_img = face_img[y : y + h, x : x + w]
            mouth_name = get_time_name(count)
            
            cv2.imwrite('../img/mouth/mouth_' +  mouth_name + '.jpg', mouth_img)
            cv2.imwrite(path + '/img/mouth/mouth_' +  mouth_name + '.jpg', mouth_img)
            mouth_path = str('./img/mouth/mouth_' +  mouth_name + '.jpg')
            databasen1.database_input('temp', 'mouth', int(x), int(y), mouth_path)
            
        #目
        eye_list = cascade_eye.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=10)
        if  len(eye_list) < 2:
            eye_name = get_time_name(count)
            cv2.imwrite ('../img/eye/eye_r_' + eye_name + '.jpg', black_img)
            cv2.imwrite(path + '/img/eye/eye_r_' +  eye_name + '.jpg', black_img)
            eye_r_path = str('./img/eye/eye_r_' + eye_name + '.jpg')
            databasen1.database_input('temp', 'eyeright', 0, 0, eye_r_path, "")
            cv2.imwrite ('../img/eye/eye_l_' + eye_name + '.jpg', black_img)
            cv2.imwrite(path + '/img/eye/eye_l_' +  eye_name + '.jpg', black_img)
            eye_l_path = str('./img/eye/eye_l_' + eye_name + '.jpg')
            databasen1.database_input('temp', 'eyeleft', 0, 0, eye_l_path)
            
        else:
            right_flag = True
            for (x,y,w,h) in eye_list:
                
                if right_flag:
                    right_flag = False
                    
                    point_from = (x , y )
                    work_size = (x + w, y + h)
                    inner_list = [point_from, work_size]
                    draw_list.append(inner_list)
                    
                    eye_img = face_img[y : y + h, x : x + w]
                    eye_name = get_time_name(count)
                
                    cv2.imwrite ('../img/eye/eye_r_' + eye_name + '.jpg', eye_img)
                    cv2.imwrite(path + '/img/eye/eye_r_' +  eye_name + '.jpg', eye_img)
                    eye_r_path = str('./img/eye/eye_r_' + eye_name + '.jpg')
                    databasen1.database_input('temp', 'eyeright', 0, 0, eye_r_path)
                else:
                    point_from = (x, y)
                    work_size = (x + w, y + h)
                    inner_list = [point_from, work_size]
                    draw_list.append(inner_list)
                    
                    eye_img = face_img[y : y + h, x : x + w]
                    eye_name = get_time_name(count)
                    cv2.imwrite ('../img/eye/eye_l_' + eye_name + '.jpg', eye_img)
                    cv2.imwrite(path + '/img/eye/eye_l_' +  eye_name + '.jpg', eye_img)
                    eye_l_path = str('./img/eye/eye_l_' + eye_name + '.jpg')
                    databasen1.database_input('temp', 'eyeleft', 0, 0, eye_l_path)
                    break
        
        create_draw_img(draw_list, draw_color_point, face_img, count, face_path)
        # print(face_img)
    if count == 5:
        break
    
cap.release()
cv2.destroyAllWindows()
print("-end-")



