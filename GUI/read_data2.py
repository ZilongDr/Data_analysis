# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'read_data.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import platform
import sip

from func import FFT as FT
from func import time_frequency_conversion as ft



import matplotlib
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self,parent=None, dpi = 120):
        fig = Figure(dpi = dpi)
        self.axes_sig = fig.add_subplot(121)
        self.axes_fft=fig.add_subplot(122)
        super(MplCanvas,self).__init__(fig)
        fig.tight_layout()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1697, 1532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LoadRef = QtWidgets.QPushButton(self.widget)
        self.LoadRef.setObjectName("LoadRef")
        self.horizontalLayout_2.addWidget(self.LoadRef)
        self.LoadMea = QtWidgets.QPushButton(self.widget)
        self.LoadMea.setObjectName("LoadMea")
        self.horizontalLayout_2.addWidget(self.LoadMea)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.Filtertype = QtWidgets.QComboBox(self.widget)
        self.Filtertype.setObjectName("Filtertype")
        self.horizontalLayout_3.addWidget(self.Filtertype)
        self.NoiseRemv_run = QtWidgets.QPushButton(self.widget)
        self.NoiseRemv_run.setObjectName("NoiseRemv_run")
        self.horizontalLayout_3.addWidget(self.NoiseRemv_run)
        self.Save_NoiseRemv = QtWidgets.QPushButton(self.widget)
        self.Save_NoiseRemv.setObjectName("Save_NoiseRemv")
        self.horizontalLayout_3.addWidget(self.Save_NoiseRemv)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.Deconv = QtWidgets.QComboBox(self.widget)
        self.Deconv.setObjectName("Deconv")
        self.horizontalLayout_4.addWidget(self.Deconv)
        self.Deconv_run = QtWidgets.QPushButton(self.widget)
        self.Deconv_run.setObjectName("Deconv_run")
        self.horizontalLayout_4.addWidget(self.Deconv_run)
        self.Save_Deconv = QtWidgets.QPushButton(self.widget)
        self.Save_Deconv.setObjectName("Save_Deconv")
        self.horizontalLayout_4.addWidget(self.Save_Deconv)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.Save_info = QtWidgets.QPushButton(self.widget)
        self.Save_info.setObjectName("Save_info")
        self.horizontalLayout.addWidget(self.Save_info)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_4.addWidget(self.textBrowser)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        spacerItem = QtWidgets.QSpacerItem(448, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(74, 332, 1541, 1002))
        self.widget1.setObjectName("widget1")
        self.Figure = QtWidgets.QVBoxLayout(self.widget1)
        self.Figure.setContentsMargins(0, 0, 0, 0)
        self.Figure.setObjectName("Figure")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1697, 38))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.filename=''
        self.df=[]
        self.canv = MplCanvas(self)
        
        self.toolbar = Navi(self.canv,self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        
        self.LoadRef.clicked.connect(self.getFile)
        
        self.actionExit.triggered.connect(MainWindow.close)
        
    def Update(self):
        plt.clf()
        plt.style.use('dark_background')
        
        try:
            self.horizontalLayout.removeWidget(self.toolbar)
            self.Figure.removeWidget(self.canv)
            
            sip.delete(self.toolbar)
            sip.delete(self.canv)
            self.toolbar = None
            self.canv = None
            self.Figure.removeItem(self.spacerItem1)
        except Exception as e:
            print(e)
            pass

        self.canv = MplCanvas(self)
        self.toolbar = Navi(self.canv,self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)

        
        self.Figure.addWidget(self.canv)
        
        self.canv.axes_sig.cla()
        ax_sig = self.canv.axes_sig
        self.df.plot(x='Time',y='Signal',ax = self.canv.axes_sig)


        legend_sig = ax_sig.legend()
        legend_sig.set_draggable(True)
        
        ax_sig.set_xlabel('Time (ps)')
        ax_sig.set_ylabel('THz signal')
        
        ax_sig.set_title(self.Title+' '+'time trace')
        
        self.canv.axes_fft.cla()
        ax_fft = self.canv.axes_fft
        legend_fft = ax_fft.legend()
        legend_fft.set_draggable(True)
        
        ax_fft.set_xlabel('X axis')
        ax_fft.set_ylabel('Y axis')
        ax_fft.set_title(self.Title+'FFT')
        
        
        self.canv.draw()
    
        
    def getFile(self):
        self.filename = QFileDialog.getOpenFileName(filter = "dat (*.dat)")[0]
        print("File :", self.filename)
        
        self.readData()
        
    def readData(self):
        import os
        base_name = os.path.basename(self.filename)
        self.Title = os.path.splitext(base_name)[0]
        data = pd.read_csv(self.filename,delimiter='\t',skiprows=3, encoding = 'utf-8').fillna(0)
        print('FILE:',self.Title, data.shape )
        data.columns=['Time', 'Signal']
        self.df=data
        
        
        
        self.Update()
        
        #self.Update(self.themes[0]) # lets 0th theme be the default : bmh

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LoadRef.setText(_translate("MainWindow", "Load Reference"))
        self.LoadMea.setText(_translate("MainWindow", "Load Measurement"))
        self.label.setText(_translate("MainWindow", "Reduce noise"))
        self.NoiseRemv_run.setText(_translate("MainWindow", "Run"))
        self.Save_NoiseRemv.setText(_translate("MainWindow", "Save plot to file"))
        self.label_2.setText(_translate("MainWindow", "Deconvolution extraction"))
        self.Deconv_run.setText(_translate("MainWindow", "Run"))
        self.Save_Deconv.setText(_translate("MainWindow", "Save plot to file"))
        self.label_3.setText(_translate("MainWindow", "Information extracted"))
        self.Save_info.setText(_translate("MainWindow", "Save to file"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

