

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(465, 294)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.buton_siteEkle = QtWidgets.QPushButton(self.centralwidget)
        self.buton_siteEkle.setGeometry(QtCore.QRect(10, 10, 151, 23))
        self.buton_siteEkle.setObjectName("buton_siteEkle")
        self.buton_siteCikar = QtWidgets.QPushButton(self.centralwidget)
        self.buton_siteCikar.setGeometry(QtCore.QRect(10, 40, 151, 23))
        self.buton_siteCikar.setObjectName("buton_siteCikar")
        self.buton_HepsiniKaldir = QtWidgets.QPushButton(self.centralwidget)
        self.buton_HepsiniKaldir.setGeometry(QtCore.QRect(10, 70, 151, 23))
        self.buton_HepsiniKaldir.setObjectName("buton_HepsiniKaldir")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(190, 30, 256, 221))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 10, 231, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 465, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Site Engelleme Programı"))
        self.buton_siteEkle.setText(_translate("MainWindow", "Site Ekle..."))
        self.buton_siteCikar.setText(_translate("MainWindow", "Yasak Olanlardan Çıkar"))
        self.buton_HepsiniKaldir.setText(_translate("MainWindow", "Tüm Kısıtlamaları Kaldır"))
        self.label.setText(_translate("MainWindow", "Engellenmiş Siteler Listesi :"))


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox


class myApp(QtWidgets.QMainWindow):

    def __init__(self,path="C:\Windows\System32\drivers\etc\hosts"):
        super(myApp, self).__init__()

        width = 465
        height = 294
        self.setFixedSize(width, height)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buton_siteEkle.clicked.connect(self.f_siteEkle)
        self.ui.buton_siteCikar.clicked.connect(self.f_siteCikar)
        self.ui.buton_HepsiniKaldir.clicked.connect(self.f_hepsiniKaldir)
        self.engelli_siteleri_yukle()


    def f_siteEkle(self):

        diyalog_popup=QInputDialog
        metin,cevap=diyalog_popup.getText(self,
                                 "Site Girişi",
                                 "Site ekle : ",
                                 QLineEdit.Normal,
                                 )
        
        son_index=self.ui.listWidget.count()

        if metin and cevap is not None:
            result=self.yazi_ekle(metin)
            if(result==False):return
            self.ui.listWidget.insertItem(son_index,metin)

    def f_siteCikar(self):
        index_no=self.ui.listWidget.currentRow()
        eleman=self.ui.listWidget.item(index_no)


        if eleman is None:
            return None
        
        soru=QMessageBox.critical(self,
                                  "Siteyi Engellemeyi Kaldıma",
                                  f"{eleman.text()} sitesinin engelini kaldırmak ister misiniz?",
                                  QMessageBox.Yes | QMessageBox.No)

        if soru==QMessageBox.Yes:
            self.yazi_sil(eleman.text())
            eleman=self.ui.listWidget.takeItem(index_no)
            del eleman

    def f_hepsiniKaldir(self):

        index_no=self.ui.listWidget.currentRow()

        if self.ui.listWidget.count()==0:
            return None

        soru=QMessageBox.critical(self,
                                  "Tüm Kısıtlamaları Kaldırma",
                                  "Bütün siteleri erişilebilir hale getirmek istediğinizden emin misiniz?",
                                  QMessageBox.Yes | QMessageBox.No)
        
        if soru==QMessageBox.Yes:
            self.tum_kisitlamalari_kaldir()
            self.ui.listWidget.clear()

 
    #----------------------------------------------------------------------------
    def engelli_siteleri_yukle(self):

        self.path="C:\Windows\System32\drivers\etc\hosts"

        with open(self.path,"r+",encoding="utf-8") as file:
            satirlar=file.readlines()

            file.seek(0)

            liste=[]
            for i in satirlar:
                if("0.0.0.0" in i):
                    new_string=i[7:-1]
                    new_string=new_string.replace(" ","")
                    liste.append(new_string)

        
        self.ui.listWidget.addItems(liste)

    def yazi_ekle(self,metin):
        
        new_string=metin.replace("https://","").replace("/","")
        new_string_2 = "0.0.0.0 " + new_string + "\n"

        with open(self.path,"r",encoding="utf-8") as file:
            filedata=file.read()        
        
        if(new_string_2 in filedata):
            print("var")
            return False

        with open(self.path,"a",encoding="utf-8") as file:
            file.write(new_string_2)

    def yazi_sil(self,metin):

        new_string=metin.replace("https://","").replace("/","")
        new_string_2 = "0.0.0.0 " + new_string + "\n"

        with open(self.path,"r",encoding="utf-8") as file:
            filedata=file.read()

        filedata=filedata.replace(new_string_2,"")

        with open(self.path,'w',encoding="utf-8") as file:
            file.write(filedata)


    def tum_kisitlamalari_kaldir(self):
        with open(self.path,"r+",encoding="utf-8") as file:
            satirlar=file.readlines()

            file.seek(0)

            for i in satirlar:
                print(i)
                if("0.0.0.0" not in i):
                    file.write(i)

            file.truncate()

def uygulama_calistir():
    app=QtWidgets.QApplication(sys.argv)
    win=myApp()
    win.show()
    sys.exit(app.exec_())

uygulama_calistir()