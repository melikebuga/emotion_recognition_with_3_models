
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
import os
import cv2 as cv
from kamera import kameradan_tespit
from face_img import detect

class AnaPencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.kamera_genislik = 600
        self.kamera_yukseklik = 400
        self.baslat()
        self.simdikiEmoji = 0
        self.emojiAdedi = (len(os.listdir("emojiler")))
        self.emojiler = os.listdir("emojiler")
        self.resmiGuncelle()
        self.tahmin_edilen_duygu = "notr"
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.kamera_calistir)
    
    def baslat(self):
        self.setWindowTitle("Melike Buğa Bitirme Çalışması")
        self.setWindowIcon(QtGui.QIcon('images/yobu.jpg'))
        self.setMinimumSize(1000,750)
        self.setMaximumSize(1000,750)
        
        #Tab oluşturma
        self.tab=QtWidgets.QTabWidget(self)
        self.tab.setStyleSheet("border: 0px solid black;border-radius: 0px;background: #efecf7;")
        self.tab.move(0,0)
        self.tab.resize(1200,810)
        self.tab.setTabShape(QtWidgets.QTabWidget.TabShape(QtWidgets.QTabWidget.Triangular))
        
        #Orijinal tabı oluşturuldu.
        self.ana_tab=QtWidgets.QWidget()
        self.ana_tab.setStyleSheet("border: 0px solid black;border-radius: 10px;background: #efecf7;")
        
        #Orjinal Resim başlığı
        self.orjinal_resim_text=QtWidgets.QLabel(self.ana_tab)
        self.orjinal_resim_text.setText("ORJİNAL RESİM")
        self.orjinal_resim_text.setStyleSheet("background-color:#c39435;color:#ffffff;border-radius:20px;border-style: solid;")
        self.orjinal_resim_text.move(130,50)
        self.orjinal_resim_text.resize(171,51)
        self.orjinal_resim_text.setFont(QtGui.QFont("MS Shell Dlg 2", 13,QtGui.QFont.Bold))
        self.orjinal_resim_text.setAlignment(QtCore.Qt.AlignCenter)
        
        #Resmin gözükeceği yer
        self.orjinal_resim_img=QtWidgets.QLabel(self.ana_tab)
        self.orjinal_resim_img.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.orjinal_resim_img.move(10,120)
        self.orjinal_resim_img.setScaledContents(True)
        self.orjinal_resim_img.resize(400,400)
        
        #Resim seçme butonu
        self.orjinal_resim_bulma_btn=QtWidgets.QPushButton(self.ana_tab)
        self.orjinal_resim_bulma_btn.setText("RESİM SEÇ")
        self.orjinal_resim_bulma_btn.setStyleSheet("background-color:#4d9a5c;color:#ffffff;border-radius:20px;border-style: solid;")
        self.orjinal_resim_bulma_btn.move(130,550)
        self.orjinal_resim_bulma_btn.resize(171,51)
        self.orjinal_resim_bulma_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 15,QtGui.QFont.Bold))
        self.orjinal_resim_bulma_btn.clicked.connect(self.resim_sec)
        
        #Resimde Bulunan Yüzler Başlığı
        self.bulunan_resimdeki_yuzler_text=QtWidgets.QLabel(self.ana_tab)
        self.bulunan_resimdeki_yuzler_text.setText("RESİMDE BULUNAN YÜZLER")
        self.bulunan_resimdeki_yuzler_text.setStyleSheet("background-color:#c39435;color:#ffffff;border-radius:20px;border-style: solid;")
        self.bulunan_resimdeki_yuzler_text.move(550,50)
        self.bulunan_resimdeki_yuzler_text.resize(261,51)
        self.bulunan_resimdeki_yuzler_text.setFont(QtGui.QFont("MS Shell Dlg 2", 13,QtGui.QFont.Bold))
        self.bulunan_resimdeki_yuzler_text.setAlignment(QtCore.Qt.AlignCenter)
        
        #Resminde Bulunan yuzler gözükeceği yer
        self.bulunan_resimdeki_yuzler_img=QtWidgets.QLabel(self.ana_tab)
        self.bulunan_resimdeki_yuzler_img.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.bulunan_resimdeki_yuzler_img.move(480,120)
        self.bulunan_resimdeki_yuzler_img.setScaledContents(True)
        self.bulunan_resimdeki_yuzler_img.resize(400,400)
        
        #Resimdeki yuzleri bul butonu
        self.resimdeki_yuzleri_bul_btn=QtWidgets.QPushButton(self.ana_tab)
        self.resimdeki_yuzleri_bul_btn.setText("RESİMDEKİ YÜZLERİ BUL")
        self.resimdeki_yuzleri_bul_btn.setStyleSheet("background-color:#4d9a5c;color:#ffffff;border-radius:20px;border-style: solid;")
        self.resimdeki_yuzleri_bul_btn.move(550,550)
        self.resimdeki_yuzleri_bul_btn.resize(291,51)
        self.resimdeki_yuzleri_bul_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 15,QtGui.QFont.Bold))
        self.resimdeki_yuzleri_bul_btn.clicked.connect(self.yuz_bul)

        
        #Emoji tabı oluşturuldu.
        self.emoji_tab=QtWidgets.QWidget()
        self.emoji_tab.setStyleSheet("border: 0px solid black;border-radius: 10px;background: #efecf7; ")
        
        
        #Kamera ac kapa butonu
        self.toggle_btn=QtWidgets.QPushButton(self.emoji_tab)
        self.toggle_btn.setText("KAMERA AÇ KAPA")
        self.toggle_btn.setStyleSheet("background-color:#4d9a5c;color:#ffffff;border-radius:20px;border-style: solid;")
        self.toggle_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 12,QtGui.QFont.Bold))
        self.toggle_btn.resize(165,60)
        self.toggle_btn.move(20,210)
        self.toggle_btn.clicked.connect(self.timer_ac_kapa)
        
        
        #Sol Btn
        self.sol_btn=QtWidgets.QPushButton(self.emoji_tab)
        self.sol_btn.setText("SOL")
        self.sol_btn.setStyleSheet("background-color:#c39435;color:#ffffff;border-radius:20px;border-style: solid;")
        self.sol_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 12,QtGui.QFont.Bold))
        self.sol_btn.resize(50,50)
        self.sol_btn.move(20,50)
        self.sol_btn.clicked.connect(self.emojiSol)
        
        #Test Btn
        self.test_btn=QtWidgets.QPushButton(self.emoji_tab)
        self.test_btn.setText("DUYGU DURUMU")
        self.test_btn.setStyleSheet("background-color:#c39435;color:#ffffff;border-radius:20px;border-style: solid;")
        self.test_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 12,QtGui.QFont.Bold))
        self.test_btn.resize(150,60)
        self.test_btn.move(300,50)
        self.test_btn.clicked.connect(self.test_fn)
        
        #Emojinin Gözükeceği yer
        self.emoji_img=QtWidgets.QLabel(self.emoji_tab)
        self.emoji_img.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.emoji_img.move(70,50)
        self.emoji_img.setScaledContents(True)
        self.emoji_img.resize(150,150)
        
        
        #Kameranın Gözükeceği yer
        self.kamera_goruntusu=QtWidgets.QLabel(self.emoji_tab)
        self.kamera_goruntusu.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.kamera_goruntusu.move(30,300)
        self.kamera_goruntusu.setScaledContents(True)
        self.kamera_goruntusu.resize(self.kamera_genislik,self.kamera_yukseklik)
        
        #Sag Btn
        self.sag_btn=QtWidgets.QPushButton(self.emoji_tab)
        self.sag_btn.setText("SAĞ")
        self.sag_btn.setStyleSheet("background-color:#c39435;color:#ffffff;border-radius:20px;border-style: solid;")
        self.sag_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 12,QtGui.QFont.Bold))
        self.sag_btn.resize(50,50)
        self.sag_btn.move(220,50)
        self.sag_btn.clicked.connect(self.emojiSag)
        
        #Label
        self.label = QtWidgets.QLabel(self.emoji_tab)
        self.label.setText("SONUÇ")
        self.label.setStyleSheet("color:red;padding:100px")
        self.label.resize(450,50)   
        self.label.move(230,120)
        
        self.tab.addTab(self.ana_tab,"Görüntüden Yüz Tanımlama")
        self.tab.addTab(self.emoji_tab,"Kameradan Yüz Tanımlama")

    def resim_sec(self):
        self.resimUrl = QtWidgets.QFileDialog.getOpenFileName(self,"Lütfen bir resim seçiniz",'',"Image Files (*.png *.jpg *.jpeg)")
        self.resim=self.resimUrl[0]
        self.orjinal_resim_img.setPixmap(QtGui.QPixmap(self.resim))
        
    def yuz_bul(self):
        img=cv.imread(str(self.resim))
        yuz=detect(img)
        cv.imwrite('output/output.jpg',yuz)
        self.bulunan_resimdeki_yuzler_img.setPixmap(QtGui.QPixmap('output/output.jpg'))


    def emojiSag(self):
        if(self.simdikiEmoji+1 < self.emojiAdedi):
            self.simdikiEmoji = self.simdikiEmoji + 1;
        else:
            self.simdikiEmoji = 0
            
        self.resmiGuncelle()
        
        
    def emojiSol(self):
        if(self.simdikiEmoji-1 > -1):
            self.simdikiEmoji = self.simdikiEmoji + -1;
        else:
            self.simdikiEmoji = self.emojiAdedi-1
            
        self.resmiGuncelle()
    
    def resmiGuncelle(self):
        self.emoji_img.setPixmap(QtGui.QPixmap('emojiler/' + self.emojiler[self.simdikiEmoji]))
        
        
    def kamera_calistir(self):
        ret, image = self.cap.read()
        image,duygu,ne_kadar_dogru = kameradan_tespit(image)
        self.tahmin_edilen_duygu = duygu
        # dogru duygu mu degerlendir
        emoji_uzantili = self.emojiler[self.simdikiEmoji]
        if ne_kadar_dogru > 0.5:
            if( self.tahmin_edilen_duygu == emoji_uzantili.replace(".png","")):
                self.label.setText("Eşleşti")
            else:
                self.label.setText("Eşleşmiyor")
        else:
            self.label.setText("Eşleşmiyor")
        height, width, channel = image.shape
        step = channel * width
        qImg = QtGui.QImage(image.data, self.kamera_genislik, self.kamera_yukseklik, step, QtGui.QImage.Format_RGB888)
        self.kamera_goruntusu.setPixmap(QtGui.QPixmap.fromImage(qImg))   
        
    
    def timer_ac_kapa(self):
        print(self.timer.isActive())
        if not self.timer.isActive():
            self.cap = cv.VideoCapture(0)
            self.timer.start(20)
        else:
            self.timer.stop()
            self.cap.release()
            
    
    def test_fn(self):
        print(self.emojiler[self.simdikiEmoji])
app=QtWidgets.QApplication(sys.argv)     
ana = AnaPencere()
ana.show()
sys.exit(app.exec_())