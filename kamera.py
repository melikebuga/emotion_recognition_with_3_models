from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier('model/haarcascade-frontalface-default.xml')
duygu_modeli = load_model('model/_Xception.49-0.64.hdf5', compile=False)
cinsiyet_modeli = load_model('model/cinsiyet_model.hdf5', compile=False)
cinsiyetler=["kadin","erkek"]
duygular = ["kizgin" ,"igrenme","korku", "mutlu", "uzgun", "sasirma","notr"]

def kameradan_tespit(cerceve):
    
    resim_gri_hali = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
    yuzler = face_cascade.detectMultiScale(resim_gri_hali,scaleFactor=1.3, minNeighbors=5)
    
    cerceve_klonu = cerceve.copy()
    duygu = "notr"
    duygu_sonucu = 0
    for (x, y, w, h) in yuzler:

        roi = resim_gri_hali[y:y + h, x:x + w]
        roiForGender = roi
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        roiForGender = cv2.resize(roiForGender, (64, 64))
        roiForGender = roiForGender.astype("float") / 255.0
        roiForGender = img_to_array(roiForGender)
        roiForGender = np.expand_dims(roiForGender, axis=0)

        tahminler = duygu_modeli.predict(roi)[0]
        duygu_sonucu = np.max(tahminler)

        cinsiyet_tahminleri=cinsiyet_modeli.predict(roiForGender)[0]
        cinsiyet_sonucu=np.max(cinsiyet_tahminleri)
        
        duygu = str(duygular[tahminler.argmax()])
        cinsiyet = str(cinsiyetler[cinsiyet_tahminleri.argmax()])

        label =[" Duygu durumu: "+ duygu +" (%"+str(round(duygu_sonucu*100,2))+") ",
                " Cinsiyet: "+ cinsiyet +" (%"+str(round(cinsiyet_sonucu*100,2))+") "]

        eksirota=[62,30]

        cv2.rectangle(cerceve_klonu, (x, y-90), (x + w, y -15),(0,0,255),5)
        cv2.rectangle(cerceve_klonu, (x, y-90), (x + w, y -15),(0,0,255),-1)

        for i in range(0,2):
            cv2.putText(cerceve_klonu, label[i], (x,y-eksirota[i]),cv2.FONT_HERSHEY_SIMPLEX, float((w)/600), (255, 255, 255), 2)

        cv2.rectangle(cerceve_klonu, (x, y), (x + w, y + h),(0,0,255),5)
    
    return cerceve_klonu,duygu,duygu_sonucu