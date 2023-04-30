import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QFileDialog, QWidget,QGroupBox, QDialogButtonBox, QLineEdit, QGridLayout, QCheckBox, QHBoxLayout
)

from PyQt5.QtGui import QIntValidator

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

import platform
import sip

import numpy as np
import pandas as pd
from func import FFT as FT
from func import time_frequency_conversion as t_to_freq
from func import unit_conversion as ut
from func import misc
from scipy.fft import next_fast_len

from Module.module_deconv import FISTA_dialog, AFISTA_dialog, Load_file_dialog

from GUI.GUI_Deconvolution import Ui_MainWindow
from pylops.utils import dottest


class Window(QMainWindow, Ui_MainWindow):
        def __init__(self, parent=None):
                super().__init__(parent)
                self.setupUi(self)
                # Zero padding number of points:
                self.Npad=next_fast_len(2**12)
                # Close window
                self.QuitButton.clicked.connect(self.close)
                # Clear all
                self.ClearAllButton.clicked.connect(self.clear_all)
                # Tab1: Initialize filename and dict to store loaded data

                self.filename=''
                self.col_name=[]
                self.df_time={}
                self.df_counter=0
                self.df_freq={}
                # Pushbutton Left: load file
                self.LoadButton.clicked.connect(self.getFile)
                # Pushbutton plot selected
                self.PlotButton.clicked.connect(self.loading_plot_time)
                # Pushbutton plot selected
                self.PlotFreqButton.clicked.connect(self.loading_plot_freq)
                # Pushbutton Left: clear time list
                self.ClearButton.clicked.connect(self.clear_time)
                # Pushbutton Left: clear frequency list
                self.ClearFreqButton.clicked.connect(self.clear_freq)
                
                # Tab1: Initialize list view
                #self.model = QStandardItemModel()
                #self.listView.setModel(self.model)
                # Tab1: Skip Row line editor
                self.SkipRow_num=0
                self.SkipRowEdit.setValidator(QIntValidator())
                self.SkipRowEdit.setText(str(self.SkipRow_num))
                # Tab1: Delimiter radio button
                self.Delim='\t'
                self.TabButton.setChecked(True)
                self.TabButton.toggled.connect(self.Tabselected)
                self.CommButton.toggled.connect(self.Commselected)
                self.SemiButton.toggled.connect(self.Semiselected)


                # Right: Set  Domain comobox:
                self.DomainComboBox.addItem('Frequency', ['Simple Frequency domain', 'FFT_Wiener'])
                self.DomainComboBox.addItem('Time', ['FISTA', 'AFISTA', 'SALSA',])
                # Tab3: Update the Deconvolution method combobox once the Geometry combobox is changed:
                self.DomainComboBox.currentIndexChanged.connect(self.updateDeconvCombo)
                self.updateDeconvCombo(self.DomainComboBox.currentIndex())
                self.Dv_func_freq=[] # self.FP, self.air, self.Frequency_domain]
                self.Dv_func_time=[ self.FISTA, self.AFISTA]
                # Tab3: Pushbutton Deconvolute:
                self.DeconvButton.clicked.connect(self.Deconv)
                # Deconvoluted results:
                self.df_decon={}
                # Tab3: Pushbutton Select Ref:
                self.df_ref_time={}
                self.df_ref_freq={}
                self.SetRefButton.clicked.connect(self.Set_Ref)
                # Tab3: Pushbutton Set Sample:
                self.df_sample_time={}
                self.df_sample_freq={}
                self.SetSamButton.clicked.connect(self.Set_Sample)
                # Tab3: Pushbutton remove Ref:
                self.RemRefButton.clicked. connect(self.Remove_Ref)
                # Tab3: Pushbutton remove Sample:
                self.RemSamButton.clicked.connect(self.Remove_Sample)
                
                # Tab3: Reference list view:
                self.ref_deconv_name=''
                # Tab3: Sample list view:
                self.sample_deconv_name=''
                
                #Push Button Save selected:
                self.SaveResultButton.clicked.connect(self.SaveFile)
                #Push Button Remove selected:
                self.RemResultButton.clicked.connect(self.Remv_selected)
                
#----------------------------------------------------Button Functions------------------------------------------------------------
        def Tabselected(self):
                self.Delim='\t'
        def Commselected(self):
                self.Delim=','
        def Semiselected(self):
                self.Delim=';'
        
        def getFile(self):
                self.filename = QFileDialog.getOpenFileName(filter = "dat (*.dat);; csv (*.csv);; txt (*.txt)")[0]
                #print(self.df.keys())
                self.SkipRow_num=int(self.SkipRowEdit.text())
                self.readData()
        
        def loading_plot_time(self):
                
                #Index = self.listView.selectedIndexes()[0]
                #name=Index.model().itemFromIndex(Index).text()
                graphWidget = pg.plot(title="load data")
                items=self.listWidget.selectedItems()
                for i in range(len(items)):
                        name=items[i].text()
                        try:
                                t=self.df_time[name]['Time']
                                E_t=self.df_time[name]['Signal']

                                pen = pg.mkPen(i)
                                graphWidget.plot(t, E_t, pen=pen)
                        except:
                                pass
        
        def loading_plot_freq(self):
                
                #Index = self.listView.selectedIndexes()[0]
                #name=Index.model().itemFromIndex(Index).text()
                graphWidget = pg.plot(title="load data")
                items=self.FreqListWidget.selectedItems()
                
                for i in range(len(items)):
                        name=items[i].text()
                        freq=self.df_freq[name]['Frequency']
                        Amp=(abs(self.df_freq[name]['FT']))**2
                        pen = pg.mkPen(i)
                        graphWidget.plot(freq, Amp, pen=pen)
                
                                
                        

        def readData(self):
                import os
                #self.df.clear()
                base_name = os.path.basename(self.filename)
                self.Title = os.path.splitext(base_name)[0]
                data = pd.read_csv(self.filename,delimiter=self.Delim, skiprows=self.SkipRow_num, keep_default_na=True, encoding = 'utf-8')
                col=data.columns
                self.dlg_file=Load_file_dialog(data)
                
                if self.dlg_file.exec():
                        try:
                                indx=self.dlg_file.col_indx
                                f_name=self.dlg_file.f_name
                                if f_name is not None:
                                        f_name_new=self.Title+'_'+f_name
                                else:
                                        f_name_new=self.Title
                                
                                if indx[0] is not None and indx[2] is not None:
                                        if f_name_new in self.df_time:
                                                f_name_new=f_name_new+'_'+str(self.df_counter)
                                                self.df_counter=self.df_counter+1
                                        else:
                                                f_name_new=f_name_new
                                        t_p=data[col[indx[0]]]
                                        t_p_new=t_p[~np.isnan(t_p)]
                                        E_t=data[col[indx[1]]]
                                        E_t_new=E_t[~np.isnan(E_t)]
                                        d_time={'Time':t_p_new, 'Signal': E_t_new}
                                        data_time=pd.DataFrame(data=d_time)
                                        self.df_time[f_name_new]=data_time
                                        freq=np.array(data[col[indx[2]]])
                                        FT=data[col[indx[3]]]
                                        FT_complex=np.zeros(len(FT), dtype=complex)
                                        for i, n in enumerate(FT):
                                                FT_complex[i]=complex(n)   
                                        f={'Frequency': freq, 'FT': FT_complex}
                                        data_freq=pd.DataFrame(data=f)
                                        self.df_freq[f_name_new]=data_freq
                                        self.listWidget.addItem(f_name_new)
                                        self.FreqListWidget.addItem(f_name_new)
                                elif indx[2] is not None:
                                        if f_name_new in self.df_freq:
                                                f_name_new=f_name_new+'_'+str(self.df_counter)
                                                self.df_counter=self.df_counter+1
                                        else:
                                                f_name_new=f_name_new
                                        freq=np.array(data[col[indx[2]]])
                                        FT=data[col[indx[3]]]
                                        FT_complex=np.zeros(len(FT), dtype=complex)
                                        for i, n in enumerate(FT):
                                                FT_complex[i]=complex(n)
                                        f={'Frequency': freq, 'FT': FT_complex}
                                        data_freq=pd.DataFrame(data=f)
                                        self.df_freq[f_name_new]=data_freq
                                        self.FreqListWidget.addItem(f_name_new)
                                
                                elif indx[0] is not None:
                                        if f_name_new in self.df_time:
                                                f_name_new=f_name_new+'_'+str(self.df_counter)
                                                self.df_counter=self.df_counter+1
                                        else:
                                                f_name_new=f_name_new
                                        t_p=data[col[indx[0]]]
                                        t_p_new=t_p[~np.isnan(t_p)]
                                        E_t=data[col[indx[1]]]
                                        E_t_new=E_t[~np.isnan(E_t)]
                                        d_time={'Time':t_p_new, 'Signal': E_t_new}
                                        data_time=pd.DataFrame(data=d_time)
                                        self.df_time[f_name_new]=data_time
                                        self.listWidget.addItem(f_name_new)
                                
                                else:
                                        print('file not read')
                                        
                                
                                
                                
                        except:
                                pass
                
                
                

        def clear_time(self):
               self.df_time.clear()
               
               self.df_ref_time.clear()
               self.df_ref_freq.clear()
               self.df_sample_time.clear()
               self.df_sample_freq.clear()


               self.listWidget.clear()
               self.RefListWidget.clear()
               self.SamListWidget.clear()
               
        def clear_freq(self):
                self.df_freq.clear()
                self.FreqListWidget.clear()
                
        def clear_all(self):
                self.df_time.clear()
                self.df_ref_time.clear()
                self.df_ref_freq.clear()
                self.df_sample_time.clear()
                self.df_sample_freq.clear()
                self.df_decon.clear()
                self.listWidget.clear()
                self.FreqListWidget.clear()
                self.RefListWidget.clear()
                self.SamListWidget.clear()
                self.DeconvListWidget.clear()
                
                
                

        def updateDeconvCombo(self,index):
                self.DeconvComboBox.clear()
                methods=self.DomainComboBox.itemData(index)
                if methods:
                        self.DeconvComboBox.addItems(methods)
        
        def Set_Ref(self):
                try:
                        items=self.listWidget.selectedItems()[0]
                        name=items.text()
                        self.ref_deconv_name=name
                        self.df_ref_time[name]=self.df_time[name]
                        
                except:
                        items=self.FreqListWidget.selectedItems()[0]
                        name=items.text()
                        self.ref_deconv_name=name
                        self.df_ref_freq[name]=self.df_freq[name]
                self.RefListWidget.addItem(name)

                
        def Remove_Ref(self):
                self.df_ref_time.clear()
                self.df_ref_freq.clear()
                self.RefListWidget.clear()

        def Set_Sample(self):
                try:
                        items=self.listWidget.selectedItems()[0]
                        name=items.text()
                        self.sample_deconv_name=name
                        self.df_sample_time[name]=self.df_time[name]
                        
                except:
                        items=self.FreqListWidget.selectedItems()[0]
                        name=items.text()
                        self.sample_deconv_name=name
                        self.df_sample_freq[name]=self.df_freq[name]
                self.SamListWidget.addItem(name)
                

        def Remove_Sample(self):
                self.df_sample_time.clear()
                self.df_sample_freq.clear()
                self.SamListWidget.clear()

        def clear_info(self):
                self.InfoBrowser.clear()

        def Deconv(self):
                Deconv_method_index=self.DeconvComboBox.currentIndex()
                Deconv_domain_index=self.DomainComboBox.currentIndex()
                if Deconv_domain_index==0:
                        self.Dv_func_freq[Deconv_method_index]()
                elif Deconv_domain_index==1:
                        self.Dv_func_time[Deconv_method_index]()
        
        def SaveFile(self):
                Index = self.DeconvListWidget.selectedItems()[0]
                data_name=Index.text()
                data_to_save=self.df_decon[data_name]
                Path = QFileDialog.getSaveFileName(self, 'Save File', data_name+'_time_freq'+'.dat', )[0]
                with open(Path, 'w') as file:            
                        data_to_save.to_csv(file, sep='\t', index=False)
        
        def Remv_selected(self):
                Index = self.DeconvListWidget.selectedItems()[0]
                name=Index.text()
                del self.df_decon[name]
                row_index=self.DeconvListWidget.currentRow()
                self.DeconvListWidget.takeItem(row_index)
        
#------------------------------------------------Deconvolution functions-----------------------------------------------------------------
        
        def FISTA(self, *args):
                
                data_ref_time=self.df_ref_time[self.ref_deconv_name]
                data_sample_time=self.df_sample_time[self.sample_deconv_name]

                self.dlg_FISTA=FISTA_dialog(data_ref_time, data_sample_time, self.sample_deconv_name)
                if self.dlg_FISTA.exec():
                        data=self.dlg_FISTA.deconv_data
                        name=self.sample_deconv_name+'_'+'deconv'+'_FISTA'
                        self.df_decon[name]=data
                        self.df_time[name]=data
                        self.listWidget.addItem(name)
                        self.DeconvListWidget.addItem(name)
        
        def AFISTA(self, *args):
                
                data_ref_time=self.df_ref_time[self.ref_deconv_name]
                data_sample_time=self.df_sample_time[self.sample_deconv_name]

                self.dlg_AFISTA=AFISTA_dialog(data_ref_time, data_sample_time)
                if self.dlg_AFISTA.exec():
                        data=self.dlg_FISTA.deconv_data
                        name=self.sample_deconv_name+'_'+'deconv'+'_AFISTA'
                        self.df_decon[name]=data
                        self.df_time[name]=data
                        self.listWidget.addItem(name)
                        self.DeconvListWidget.addItem(name)
                                        



        
                

                        
                
                        
             

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
