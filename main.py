# -*- coding: utf-8 -*-
"""
Created on Tue May 31 19:45:46 2022

@author: mehme
"""

#----------------------KÜTÜPHANE--------------------------#
#---------------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *
from HakkindaUI import *

#----------------------UYGULAMA OLUŞTUR-------------------#
#---------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

penHakkinda=QDialog()
ui2=Ui_Dialog()
ui2.setupUi(penHakkinda)



#----------------------VERİTABANI OLUŞTUR-----------------
#---------------------------------------------------------#
import sqlite3
global curs
global conn

conn=sqlite3.connect('veritabani.db')
curs=conn.cursor()
sorguCreTblDava=("CREATE TABLE IF NOT EXISTS Dava(                    \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,       \
                 MüvekkilAdi TEXT NOT NULL,                           \
                 MüvekkilSoyadi TEXT NOT NULL,                        \
                 TCNo TEXT NOT NULL UNIQUE,                           \
                 MüvekkilTel TEXT NOT NULL,                           \
                 KarsiTaraf TEXT NOT NULL,                            \
                 KarsiAvukat TEXT NOT NULL,                           \
                 DavaDurumu TEXT NOT NULL,                            \
                 DavaTuru TEXT NOT NULL,                            \
                 DavaTarihi TEXT NOT NULL,                              \
                 Miktar TEXT NOT NULL)")
curs.execute(sorguCreTblDava)
conn.commit()
#----------------------KAYDET-----------------------------#
#---------------------------------------------------------#
def EKLE():
    _lneMuvekkilAdi=ui.lneMuvekkilAdi.text()
    _lneMuvekkilSoyadi=ui.lneMuvekkilSoyadi.text()
    _lneTCK=ui.lneTCK.text()
    _lneMuvekkilTel=ui.lneMuvekkilTel.text()
    _lneKarsiTaraf=ui.lneKarsiTaraf.text()
    _lneKarsiAvukat=ui.lneKarsiAvukat.text()
    _cmbDavaDurumu=ui.cmbDavaDurumu.currentText()
    _lwDavaTuru=ui.lwDavaTuru.currentItem().text()
    _cwDavaTarihi=ui.cwDavaTarihi.selectedDate().toString(QtCore.Qt.ISODate)
    _lneMiktar=ui.lneMiktar.text()
    
        
             
    curs.execute("INSERT INTO Dava \
                     (MüvekkilAdi,MüvekkilSoyadi,TCNo,MüvekkilTel,KarsiTaraf,KarsiAvukat,DavaDurumu,DavaTarihi,DavaTuru,Miktar) \
                      VALUES (?,?,?,?,?,?,?,?,?,?)", \
                      (_lneMuvekkilAdi,_lneMuvekkilSoyadi,_lneTCK,_lneMuvekkilTel,_lneKarsiTaraf,_lneKarsiAvukat, \
                           _cmbDavaDurumu,_lwDavaTuru,_cwDavaTarihi,_lneMiktar))
    conn.commit()
    LISTELE()
     
#----------------------LİSTELE-----------------------------#
#---------------------------------------------------------#  
def LISTELE():
    
    ui.tblwBilgiler.clear()
    
    ui.tblwBilgiler.setHorizontalHeaderLabels(('No','Müvekkil Adı','Müvekkil Soyadı','Müvekkil TCNo', \
                                                  'Müvekkil TEL', 'Karşı Taraf', 'Karşı Avukat', 'Dava Durumu', \
                                                   'Dava Türü','Dava Tarihi', 'Miktar'))
    
    ui.tblwBilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    curs.execute("SELECT * FROM Dava")
    
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tblwBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.lneTCK.clear()
    ui.lneMuvekkilAdi.clear()
    ui.lneMuvekkilSoyadi.clear()
    ui.cmbDavaDurumu.setCurrentIndex(-1)
    
    curs.execute("SELECT COUNT(*) FROM Dava")
    kayitSayisi=curs.fetchone()
    ui.lblKayitSayisi.setText(str(kayitSayisi[0]))
    
   
    

LISTELE()

     #----------------------ÇIKIŞ-----------------------------#
#---------------------------------------------------------#  
def CIKIS():
    cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()
        #----------------------SİL-----------------------------#
#---------------------------------------------------------# 
def SIL():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Kaydı silmek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.tblwBilgiler.selectedItems()
        silinecek=secili[3].text()
        try:
            curs.execute("DELETE FROM Dava WHERE TCNo='%s'" %(silinecek))
            conn.commit()
            
            LISTELE()
            
            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...",10000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi...",10000)
        
        
     
#----------------------ARAMA-----------------------------#
#---------------------------------------------------------# 

def ARA():
    aranan1=ui.lneTCK.text()
    aranan2=ui.lneMuvekkilAdi.text()
    aranan3=ui.lneMuvekkilSoyadi.text()
    
    curs.execute("SELECT * FROM Dava WHERE TCNo=? OR MüvekkilAdi=? OR MüvekkilSoyadi=? OR (MüvekkilAdi=? AND MüvekkilSoyadi=?)",  \
                 (aranan1,aranan2,aranan3,aranan2,aranan3))
    conn.commit()
    ui.tblwBilgiler.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tblwBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    

#----------------------DOLDUR-----------------------------#
#---------------------------------------------------------#
def DOLDUR():
    secili=ui.tblwBilgiler.selectedItems()
    ui.lneTCK.setText(secili[3].text())
    ui.lneMuvekkilAdi.setText(secili[1].text())
    ui.lneMuvekkilSoyadi.setText(secili[2].text())
    ui.cmbDavaDurumu.setCurrentText(secili[7].text())
    if secili[8].text()=="TESPİT DAVASI":
        ui.lwDavaTuru.item(0).setSelected(True)
        ui.lwDavaTuru.setCurrentItem(ui.lwDavaTuru.item(0))
    if secili[8].text()=="TOPLULUK DAVALARI":
        ui.lwDavaTuru.item(1).setSelected(True)
        ui.lwDavaTuru.setCurrentItem(ui.lwDavaTuru.item(1))
    if secili[8].text()=="İNŞAİ DAVALAR":
        ui.lwDavaTuru.item(2).setSelected(True)
        ui.lwDavaTuru.setCurrentItem(ui.lwDavaTuru.item(2))
    if secili[8].text()=="TERDİTLİ DAVALAR":
        ui.lwDavaTuru.item(3).setSelected(True)
        ui.lwDavaTuru.setCurrentItem(ui.lwDavaTuru.item(3))
    if secili[8].text()=="KISMİ DAVA":
        ui.lwDavaTuru.item(4).setSelected(True)
        ui.lwDavaTuru.setCurrentItem(ui.lwDavaTuru.item(4))
    if secili[8].text()=="BELİRSİZ ALACAK DAVASI":
        ui.lwDavaTuru.item(5).setSelected(True)
        ui.cwDavaTarihi.setCurrentItem(ui.cwDavaTarihi.item(8)) 
    yil=int(secili[9].text()[0:4])
    ay=int(secili[9].text()[5:7])
    gun=int(secili[9].text()[8:10])
    ui.cwDavaTarihi.setSelectedDate(QtCore.QDate(yil,ay,gun))
    ui.lneMuvekkilTel.setText(secili[4].text())
    ui.lneKarsiTaraf.setText(secili[5].text())
    ui.lneKarsiAvukat.setText(secili[6].text())
    ui.lneMiktar.setText(secili[10].text())
    
   #----------------------GÜNCELLE-----------------------------#
#---------------------------------------------------------#
def GUNCELLE():
    cevap=QMessageBox.question(penAna,"KAYIT GÜNCELLE","Kaydı güncellemek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.tblwBilgiler.selectedItems()
            _Id=int(secili[0].text())
            _lneMuvekkilAdi=ui.lneMuvekkilAdi.text()
            _lneMuvekkilSoyadi=ui.lneMuvekkilSoyadi.text()
            _lneTCK=ui.lneTCK.text()
            _lneMuvekkilTel=ui.lneMuvekkilTel.text()
            _lneKarsiTaraf=ui.lneKarsiTaraf.text()
            _lneKarsiAvukat=ui.lneKarsiAvukat.text()
            _cmbDavaDurumu=ui.cmbDavaDurumu.currentText()
            _lwDavaTuru=ui.lwDavaTuru.currentItem().text()
            _cwDavaTarihi=ui.cwDavaTarihi.selectedDate().toString(QtCore.Qt.ISODate)
            _lneMiktar=ui.lneMiktar.text()
        
             
            curs.execute("UPDATE Dava SET MüvekkilAdi=?, MüvekkilSoyadi=?, TCNo=?, MüvekkilTel=?, KarsiTaraf=?, KarsiAvukat=?,\
                         DavaDurumu=?, DavaTuru=?,DavaTarihi=?, Miktar=? WHERE Id=?", \
                         (_lneMuvekkilAdi,_lneMuvekkilSoyadi,_lneTCK,_lneMuvekkilTel,   _lneKarsiTaraf,_lneKarsiAvukat, \
                           _cmbDavaDurumu,_lwDavaTuru,_cwDavaTarihi,_lneMiktar,_Id))
            conn.commit()
            
            LISTELE()
            
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata meydana geldi" +str(Hata))
    else:
        ui.statusbar.showMessage("Güncellme iptal edildi",10000)



#----------------------HAKKINDA-----------------------------#
#---------------------------------------------------------#
def HAKKINDA():
    penHakkinda.show()
#----------------------SİNYAL-SLOT-----------------------------#
#---------------------------------------------------------#
ui.btnEkle.clicked.connect(EKLE)
ui.btnListele.clicked.connect(LISTELE)
ui.btnCikis.clicked.connect(CIKIS)
ui.btnSil.clicked.connect(SIL)
ui.btnAra.clicked.connect(ARA)
ui.tblwBilgiler.itemSelectionChanged.connect(DOLDUR)
ui.btnGuncelle.clicked.connect(GUNCELLE)
ui.menuhakkinda.triggered.connect(HAKKINDA)



sys.exit(Uygulama.exec_())