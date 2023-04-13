import cv2 as cv
import numpy as np
import os

employees=[]
DIR=f'{os.getcwd()}\\Employee_images\\'
for i in os.listdir(DIR):
    employees.append(i)

face_cascade=cv.CascadeClassifier('haarcascade_frontalface_default.xml')

features=[]
labels=[]

def create_train():
    for employee in employees:
        path=os.path.join(DIR,employee)
        label=employees.index(employee)
        for img in os.listdir(path):
            #get each student photo
            img_path=os.path.join(path,img)
            #read images
            img_array=cv.imread(img_path)
            #gray image
            gray_img=cv.cvtColor(img_array,cv.COLOR_BGR2GRAY)
            #detect face from an image
            face_rect=face_cascade.detectMultiScale(gray_img,1.1,10)
            #get region of interest ROI
            for (x,y,w,h) in face_rect:
                face_roi=gray_img[y:y+h,x:x+w]
                features.append(face_roi)
                labels.append(label)

try:
    create_train()
except:
    pass
#convert features to array
def save_trains():
    global features,labels
    feature=np.array(features,dtype='object')
    labelss=np.array(labels)

    face_recognizer=cv.face.LBPHFaceRecognizer_create()
    face_recognizer.train(feature,labelss)
    face_recognizer.save('faces_trained.yml')
    np.save('features.npy',feature)
    np.save("labels.npy",labelss)

try:
    save_trains()
except:
    pass