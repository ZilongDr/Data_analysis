# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:36:09 2023

@author: Wang
"""
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog,
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator

import pyqtgraph as pg

import numpy as np
import pandas as pd
from scipy.fft import next_fast_len

from func import FFT as FT
from func import unit_conversion as ut
from func import misc
from smooth_func import SWT, moving_average

from GUI.GUI_read_data_qtgraph import Ui_MainWindow

from Module.module_processing import Load_file_dialog, Savgol_dialog, SWT_dialog, BaseLine_Sub_dialog, Moving_average_dialog, TFWindow_dialog, BaseLine_dialog

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #--------------------------------------Zero padding points for FFT-------------------------------------
        
        self.Npad=next_fast_len(2**12)
        #---------------------------------------Left panel-------------------------------------------------------
        # Close window
        self.actionExit.triggered.connect(self.close)
        self.QuiteButton.clicked.connect(self.close)
        # Left: Pushbutton remove selected file
        self.RemoveLeftButton.clicked.connect(self.remove_left)
        # Left: Pushbutton clear all
        self.ClearallButton.clicked.connect(self.clear_all)
        # Left: Initilized list view on the left:
        self.model_left=QStandardItemModel()
        self.listView_left.setModel(self.model_left)
        # Left: Initialize dict to store reference and sample data
        self.df_left={}
        self.left_counter=0
        ##=----------------------------------Tab panel-------------------------------------------------------------
        # Tab: Initialize filename and dict to store loaded data
        self.filename=''
        self.df={}
        self.file_counter=0
        # Tab: Skip Row line editor
        self.SkipRow_num=3
        self.SkipRowEdit.setValidator(QIntValidator())
        self.SkipRowEdit.setText(str(self.SkipRow_num))
        # Tab: Delimiter radio button
        self.Delim='\t'
        self.TabButton.setChecked(True)
        self.TabButton.toggled.connect(self.Tabselected)
        self.CommButton.toggled.connect(self.Commselected)
        self.SemiButton.toggled.connect(self.Semiselected)
        # Pushbutton tab: load file
        self.LoadFile.clicked.connect(self.getFile)
        # Pushbutton tab: clear figuer and list
        self.ClearButton.clicked.connect(self.clear_tab)
        # Pushbutton tab: clear plot only
        self.ClearFigureButton1.clicked.connect(self.clear_figure)
        # Pushbutton tab: add to reference
        self.SetLeftButton.clicked.connect(self.set_left)
        # Pushbutton tab: remove select
        self.RemoveButton1.clicked.connect(self.remove)
        # Pushbutton tab: replot select file
        self.PlotButton1.clicked.connect(self.replot)
        # Tab: Pushbutton Subtract Baseline
        self.BaselineSubButton.clicked.connect(self.Baseline_sub)
        # Tab: PUshbutton Average
        self.AverageButton.clicked.connect(self.Average)
        # Tab: Pushbutton save file
        self.SaveButton1.clicked.connect(self.SaveFile)
        # Tab: Figure configuration:
        self.lg_tab=[]
        self.plot_counter=0
        self.FigureSignal.setLabel('left', 'Signal')
        self.FigureSignal.setLabel('bottom', 'Time (ps)')
        self.FigureFFT.setLabel('left', 'Amplitude')
        self.FigureFFT.setLabel('bottom', 'Frequency (THz)')
        self.FigureFFT.setLogMode(x=False, y=False)
        self.FigureFFT.setXRange(0,3)
        #-----------------------------------Tab1 panel---------------------------------------------------------------
        #Tab1: PUshbutton select trace for ambient remove
        # Initialize data dict to store processed data in the list:
        self.df_remv={}
        # Tab1: Pushbutton add to left
        self.AddLeftRemvButton.clicked.connect(self.add_left1)
        # Tab1: Pushbutten Set Reference:
        self.SetRefButton.clicked.connect(self.Set_Ref)
        # Tab1: Pushbutten Set sample:
        self.SetSampButton.clicked.connect(self.Set_Sample)
        # Initialize dict to store ref and sample:
        self.df_ref_remv={}
        self.df_sample_remv={}
        self.ref_remv_name=''
        self.sample_remv_name=''
        # Tab1: Pushbutton run Remove Ambient:
        self.RunRemvhButton.clicked.connect(self.RunRemv)
        # Tab1: Pushbutton clear list:
        self.ClearRemvButton.clicked.connect(self.clear1)
        # Tab1: Pushbutton Save to file:
        self.SaveFileRemvButton.clicked.connect(self.SaveFile1)
        # Tab1: Replot button:
        self.RePlotButton1.clicked.connect(self.replot1)
        # Tab1: Clear Plot button:
        self.ClearPlotButton1.clicked.connect(self.clear_plot1)
        # Tab2: Remove ambient effect combobox items:
        Remv_amb=['Window Convolution', 'DWT', 'Hilbert Huang']
        self.Remv_func=[self.TFWindow_remv]# self.DWT_remv, self.HHT_remv]
        self.RemoveAmbBox.addItems(Remv_amb)
        self.Remv_am_func=[]
        
        self.lg_tab1=[]
        self.plot_counter1=0
        self.FigureSignal1.setLabel('left', 'Signal')
        self.FigureSignal1.setLabel('bottom', 'Time (ps)')
        self.FigureFFT1.setLabel('left', 'Amplitude')
        self.FigureFFT1.setLabel('bottom', 'Frequency (THz)')
        self.FigureFFT1.setLogMode(x=False, y=False)
        self.FigureFFT1.setXRange(0,3)
        
        #-----------------------------------Tab2 panel---------------------------------------------------------------
        # Tab2: Pushbutton select trace from reference or sample
        self.SelectButton2.clicked.connect(self.select_trace)
        # Tab2: Initilize dict to store selected trace
        self.df_select={}
        self.select_name=''
        # Tab2: Pushbutton clear
        self.ClearSmoothButton.clicked.connect(self.clear_tab2)
        # Tab2: Pushbutton clear plot
        self.ClearPlotButton2.clicked.connect(self.clear_plot2)
         # Tab2: Replot button:
        self.ReplotButton2.clicked.connect(self.replot2)
        # Tab2: Pushbutton smooth
        self.SmoothButton2.clicked.connect(self.smooth)
        # Tab2: Pushbutton Add to left
        self.AddLeftButton2.clicked.connect(self.add_left2)
    	# Tab2: Pushbutton save file
        self.SaveButton2.clicked.connect(self.SaveFile2)
        # Tab2: name to appdend after smmoth:
        self.name_smooth=''
        # Tab2: Smooth comobox items:
        Smooth_item=['Wavelet', 'Moving average','Savgol filter',]
        self.SmoothCombo.addItems(Smooth_item)
        self.Sm_func=[self.swt, self.Moving_Aver, self.Savgol, ]

        
        
        # Tab2: Figure configuration:
        self.lg_tab2=[]
        self.plot_counter2=0
        self.FigureSignal2.setLabel('left', 'Signal')
        self.FigureSignal2.setLabel('bottom', 'Time (ps)')
        self.FigureFFT2.setLabel('left', 'Amplitude')
        self.FigureFFT2.setLabel('bottom', 'Frequency (THz)')
        self.FigureFFT2.setLogMode(x=False, y=False)

        self.FigureFFT2.setXRange(0,3)
        # Tab2: Initialize smooth method dialog:
        self.dlg_MA = Moving_average_dialog()
        self.dlg_Sav = Savgol_dialog()
        


#------------------------------Left Functions-------------------------------------------------------------------------
    def remove_left(self):
        Index = self.listView_left.selectedIndexes()[0]
        name=Index.model().itemFromIndex(Index).text()
        del self.df_left[name]
        row_index=Index.row()
        self.model_left.removeRow(row_index)

    def clear_all(self):
        self.model_left.clear()
        self.listWidget.clear()
        self.AmbientListWidget.clear()
        self.listWidget2.clear()
        self.df_left.clear()
        self.df.clear()
        self.left_counter=0
        self.file_counter=0
        self.df_remv.clear()
        self.df_select.clear()
        self.FigureFFT.clear()
        self.FigureSignal.clear()
        self.FigureFFT1.clear()
        self.FigureSignal1.clear()
        self.FigureFFT2.clear()
        self.FigureSignal2.clear()
        
#------------------------------Tab Functions:------------------------------------------------------------------
    def Tabselected(self):
        self.Delim='\t'
    def Commselected(self):
        self.Delim=','
    def Semiselected(self):
        self.Delim=';'
        
    def getFile(self):
        self.filename = QFileDialog.getOpenFileName(filter = "dat (*.dat);; csv (*.csv);; txt (*.txt)")[0]
        if self.filename !="":
            self.SkipRow_num=int(self.SkipRowEdit.text())
            #print(self.df.keys())
            self.readData()
    
    def combine_fft_data(self, t, E_t):
        data={'Time': t, 'Signal': E_t}
        data_pd=pd.DataFrame(data=data)
        t_s=ut.ps_to_s(t)
        f, E_w_complex=FT.FFT(t_s,E_t, self.Npad) #f in the unit of Hz, zeroN_factor: zero padding factor
        f_THz=ut.Hz_to_THz(f)
        #E_w=abs(E_w_complex)
        data_fft={'Frequency':f_THz, 'FT_complex':E_w_complex}
        fft_pd=pd.DataFrame(data=data_fft )
        # Combine time and frequency domain data
        data_combined=pd.concat([data_pd, fft_pd], ignore_index=True, axis=1)
        data_combined.columns=['Time', 'Signal', 'Frequency', 'FT_complex']
        
        return data_combined

    def readData(self):
        import os
        #self.df.clear()
        base_name = os.path.basename(self.filename)
        self.Title = os.path.splitext(base_name)[0]
        data = pd.read_csv(self.filename,delimiter=self.Delim,skiprows=self.SkipRow_num, keep_default_na=True, encoding = 'utf-8')
        data=data.dropna(axis=1, how='all')
        col=data.columns
        self.dlg_file=Load_file_dialog(data)
        if self.dlg_file.exec():
            try:
                header=self.dlg_file.signal_header
                #data.columns=header
                #Original data
                time_indx=self.dlg_file.time_indx
                signal_indx=self.dlg_file.signal_indx
                #f_name=self.dlg_file.f_name
                t_ps=misc.convert_to_np(data[col[time_indx]])
                t_ps=t_ps-t_ps[0]
                t_interp=np.linspace(t_ps[0], t_ps[-1], 2**11)
                print(t_interp)
                for counter, i in enumerate(signal_indx):
                    if i is not None:    
                        #if f_name is not None:
                        #    f_name_new=self.Title+'_'+f_name+'scan_'+str(counter)
                        #else:
                        append_name=header[counter]
                        if append_name is not None:
                            f_name_new=self.Title+ '_'+append_name 
                        else:
                            f_name_new=self.Title
                        if f_name_new in self.df:
                            f_name_new=f_name_new+'_'+str(self.file_counter)
                            self.file_counter=self.file_counter+1
                        E_t=misc.convert_to_np(data[col[i]])
                        #pg.plot(t_ps, E_t)
                        #Data interpolation:
                        E_t_interp=np.interp(t_interp,t_ps,E_t)
                        data_combined=self.combine_fft_data(t_interp, E_t_interp)
                        self.df[f_name_new]=data_combined
                        # update figure in tab 1
                        self.plot_data_tab(f_name_new)
                        # update list view in tab 1
                        self.listWidget.addItem(f_name_new)
                        
                    else:
                        pass
            except:
                pass
            
    def Baseline_sub(self):
        item=self.listWidget.selectedItems()[0]
        name=item.text()
        data=self.df[name]
        self.dlg_Baseline_sub=BaseLine_Sub_dialog(data)
        if self.dlg_Baseline_sub.exec():
            t_ps=self.dlg_Baseline_sub.t_ps
            E_t=self.dlg_Baseline_sub.E_t_window
            freq=self.dlg_Baseline_sub.freq_THz
            E_w=self.dlg_Baseline_sub.E_w
            f_name=name+'_baseline_subtracted'
            df_time={'Time':t_ps, 'Signal':E_t}
            data_time=pd.DataFrame(data=df_time)
            df_freq={'Frequency':freq, 'FT_complex':E_w}
            data_freq=pd.DataFrame(data=df_freq)
            data_combined=pd.concat([data_time, data_freq], ignore_index=True, axis=1)
            data_combined.columns=['Time', 'Signal', 'Frequency', 'FT_complex']
            self.df[f_name]=data_combined
            self.listWidget.addItem(f_name)
            self.plot_data_tab(f_name)
            
            
    
    def Average(self):
        import difflib
        items=self.listWidget.selectedItems()
        name_list=[]
        for i in range(len(items)):
            name=items[i].text()
            name_list.append(name)
        match=difflib.SequenceMatcher(None, name_list[0], name_list[1]).find_longest_match(alo=0, ahi=len(name_list[0]), blo=0, bhi=len(name_list[1]))
        name_to_save=name_list[0][match.a:match.a+match.size]+'_Average'
        # Do the average:
        y=np.zeros_like(misc.convert_to_np(self.df[name_list[0]]['Signal']))
        for i in name_list:
            Signal=misc.convert_to_np(self.df[i]['Signal'])
            y=y+Signal
        data_t=misc.convert_to_np(self.df[name_list[0]]['Time'])
        y=np.array(y/len(items))
        data_to_save=self.combine_fft_data(data_t, y)
        self.df[name_to_save]=data_to_save
        self.plot_data_tab(name_to_save)
        self.listWidget.addItem(name_to_save)

    def set_left(self):
        # update list view in "Select file name"
        Index = self.listWidget.selectedItems()[0]
        name=Index.text()
        #print(type(selectedIndex))
        # update list view in tab 1
        if name in self.df_left:
            name=name+'_'+str(self.left_counter)
            self.left_counter=self.left_counter+1
        self.model_left.appendRow(QStandardItem(name))
        data=self.df[name]
        self.df_left[name]=data
        #print(self.df_ref.keys())

    def remove(self):
        Index = self.listWidget.selectedItems()[0]
        name=Index.text()
        del self.df[name]
        row_index=self.listWidget.currentRow()
        self.listWidget.takeItem(row_index)
        

    def clear_tab(self):
        self.FigureSignal.clear()
        self.FigureFFT.clear()
        self.listWidget.clear()
        self.df.clear()
        self.file_counter=0
    
    def clear_figure(self):
        self.FigureSignal.clear()
        self.FigureFFT.clear()

    def replot(self):
        # update list view in "Select file name"
        Index = self.listWidget.selectedItems()[0]
        name=Index.text()
        self.plot_data_tab(name)

    def plot_data_tab(self, name):
        self.lg_tab.append(name)
        self.FigureSignal.addLegend()
        data_to_plot=self.df[name]
        self.FigureSignal.plot(data_to_plot['Time'],data_to_plot['Signal'], pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2), name=self.lg_tab[-1])
       
        self.FigureFFT.addLegend()
        self.FigureFFT.plot(data_to_plot['Frequency'],abs(data_to_plot['FT_complex']),pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2), name=self.lg_tab[-1])
        
        self.plot_counter=self.plot_counter+1
    
    def SaveFile(self):
        
        Index = self.listWidget.selectedItems()[0]
        data_name=Index.text()
        data_to_save=self.df[data_name]
        Path = QFileDialog.getSaveFileName(self, 'Save File', data_name+'_time_freq'+'.dat', )[0]
        with open(Path, 'w') as file:            
            data_to_save.to_csv(file, sep='\t', index=False)
        
#-------------------------------------------Tab1 functions-------------------------------------------------------
    def Set_Ref(self):        
        Index = self.listView_left.selectedIndexes()[0]
        name=Index.model().itemFromIndex(Index).text()
        self.ref_remv_name=name
        self.df_ref_remv[name]=self.df_left[name]
        self.listView_left.clearSelection()
        self.Remv_amb_indicator.setText('Reference selected')
    
    def Set_Sample(self):
        Index = self.listView_left.selectedIndexes()[0]
        name=Index.model().itemFromIndex(Index).text()
        self.sample_remv_name=name
        self.df_sample_remv[name]=self.df_left[name]
        self.listView_left.clearSelection()
        self.Remv_amb_indicator.setText('Sample selected')

    def RunRemv(self):
        Remv_method_index=self.RemoveAmbBox.currentIndex()
        data_ref=self.df_ref_remv[self.ref_remv_name]
        data_sample=self.df_sample_remv[self.sample_remv_name]
        self.Remv_func[Remv_method_index](data_ref, data_sample)   
    
    def clear_plot1(self):
        self.FigureSignal1.clear()
        self.FigureFFT1.clear()
        
    def SaveFile1(self):
        item=self.AmbientListWidget.selectedItems()[0]
        data_name=item.text()
        data_to_save=self.df_remv[data_name]
        Path = QFileDialog.getSaveFileName(self, 'Save File', data_name+'_Remove_ambient'+'.dat', )[0]
        with open(Path, 'w') as file:            
            data_to_save.to_csv(file, sep='\t', index=False)
    
    def Base_line(self, data_ref, data_sample):
        self.dlg_BaseLine=BaseLine_dialog(data_ref, data_sample)
        if self.dlg_BaseLine.exec():
            name_remv_sample=self.sample_remv_name+'_base_line_remv'
            data_sample_remv=self.dlg_BaseLine.E_t_sample_bs
            data_combined_sample=self.combine_fft_data(self.dlg_BaseLine.t_ps2_sample, data_sample_remv)
            name_remv_ref=self.ref_remv_name+'_base_line_remv'
            data_ref={'Time': self.dlg_BaseLine.t_ps2_ref, 'Signal': self.dlg_BaseLine.E_t_ref_bs}
            data_pd=pd.DataFrame(data=data_ref)

            data_ref_fft={'Frequency':self.dlg_BaseLine.f_ref_0, 'FT_complex':self.dlg_BaseLine.baseline_complex}

            fft_ref_pd=pd.DataFrame(data=data_ref_fft )
            # Combine time and frequency domain data
            data_combined_ref=pd.concat([data_pd, fft_ref_pd], ignore_index=True, axis=1)
            data_combined_ref.columns=['Time', 'Signal', 'Frequency', 'FT_complex']
            
            self.df_remv[name_remv_sample]=data_combined_sample
            self.df_remv[name_remv_ref]=data_combined_ref

            self.plot_data_tab1(data_combined_sample, name_remv_sample)
            self.plot_data_tab1(data_combined_ref, name_remv_ref)
            self.add_to_list1(name_remv_sample)
            self.add_to_list1(name_remv_ref) 
        return
    
    def TFWindow_remv(self, data_ref, data_sample):
        self.dlg_TFWindow=TFWindow_dialog(data_ref, data_sample)
        if self.dlg_TFWindow.exec(): 
            name_remv_sample=self.sample_remv_name+'_time_window_remv'
            data_sample_remv=self.dlg_TFWindow.E_sample_t_window
            
            data_combined_sample=self.combine_fft_data(self.dlg_TFWindow.t_ps2_sample, data_sample_remv)
            
            
            name_remv_ref=self.ref_remv_name+'_time_window_remv'
            data_ref={'Time': self.dlg_TFWindow.t_ps2_ref, 'Signal': self.dlg_TFWindow.E_t_ref_window}
            data_pd=pd.DataFrame(data=data_ref)

            data_ref_fft={'Frequency':self.dlg_TFWindow.f_ref_THz, 'FT_complex':self.dlg_TFWindow.E_ref_w_window}
            fft_ref_pd=pd.DataFrame(data=data_ref_fft )
            # Combine time and frequency domain data
            data_combined_ref=pd.concat([data_pd, fft_ref_pd], ignore_index=True, axis=1)
            data_combined_ref.columns=['Time', 'Signal', 'Frequency', 'FT_complex']
            
            self.df_remv[name_remv_sample]=data_combined_sample
            self.df_remv[name_remv_ref]=data_combined_ref

            self.plot_data_tab1(data_combined_ref, name_remv_sample)
            self.plot_data_tab1(data_combined_sample, name_remv_ref)
            self.add_to_list1(name_remv_sample)
            self.add_to_list1(name_remv_ref)
            
    def add_to_list1(self, name):
        self.AmbientListWidget.addItem(name)
    
    def add_left1(self):
        item=self.AmbientListWidget.selectedItems()[0]
        name=item.text()
        self.model_left.appendRow(QStandardItem(name))
        self.df_left[name]=self.df_remv[name]
    
    def clear1(self):
        self.FigureSignal1.clear()
        self.FigureFFT1.clear()
        self.AmbientListWidget.clear()
        self.df_remv.clear()
        self.df_ref_remv.clear()
        self.df_sample_remv.clear()
    
    
    def replot1(self):
        # update list view in "Select file name"
        item=self.AmbientListWidget.selectedItems()[0]
        name=item.text()
        data=self.df_remv[name]
        self.plot_data_tab1(data, name)
    
    def plot_data_tab1(self, data, name):        
        self.lg_tab1.append(name)
        self.FigureSignal1.addLegend()
        data_to_plot=data
        self.FigureSignal1.plot(data_to_plot['Time'],data_to_plot['Signal'], pen=pg.mkPen(color=pg.intColor(self.plot_counter1), width=2), name=self.lg_tab1[-1])
       
        self.FigureFFT1.addLegend()
        self.FigureFFT1.plot(data_to_plot['Frequency'],abs(data_to_plot['FT_complex']),pen=pg.mkPen(color=pg.intColor(self.plot_counter1), width=2), name=self.lg_tab1[-1])
        
        self.plot_counter1=self.plot_counter1+1
#-------------------------------------------Tab 2 functions------------------------------------------------------
    def select_trace(self):
        Index = self.listView_left.selectedIndexes()[0]
        name=Index.model().itemFromIndex(Index).text()
        self.df_select[name]=self.df_left[name]
    
        self.select_name=name
        self.listView_left.clearSelection()
        #print(self.df_select[name])
        self.plot_data_tab2(self.select_name)
        
    def smooth(self):
        smooth_method_index=self.SmoothCombo.currentIndex()
        data=self.df_select[self.select_name]
        t_ps=misc.convert_to_np(data['Time'])
        E_t=misc.convert_to_np(data['Signal'])
        self.Sm_func[smooth_method_index](t_ps, E_t, data)        

    
    def Moving_Aver(self, t_ps, E_t, *args):
        """Launch the employee dialog."""
        if self.dlg_MA.exec():     
            try:
                y_smooth=moving_average.moving_average(E_t, int(self.dlg_MA.Window_num))
                data_combined=self.combine_fft_data(t_ps, y_smooth)

                name_smooth=self.select_name+'_moving_average_Window='+self.dlg_MA.Window_num
                self.name_smooth=name_smooth
                self.df_select[name_smooth]=data_combined
                self.plot_data_tab2(name_smooth)
                
                self.add_to_list2(name_smooth)
            except:
                print('Window length should be larger than 0')
             
    
    def Savgol(self, t_ps, E_t, *args):
        from scipy.signal import savgol_filter
        if self.dlg_Sav.exec(): 
            try:
                y_smooth=savgol_filter(E_t, int(self.dlg_Sav.Window_num), int(self.dlg_Sav.FilterOrder_num))
                
                data_combined=self.combine_fft_data(t_ps, y_smooth)
                name_smooth=self.select_name+'_Savgol_Window='+self.dlg_Sav.Window_num+'_order='+self.dlg_Sav.FilterOrder_num
                self.name_smooth=name_smooth
                self.df_select[name_smooth]=data_combined
                self.plot_data_tab2(name_smooth)
                
                self.add_to_list2(name_smooth)
            except:
                print('Window or order input value wrong')
            
    def swt(self, t_ps, E_t, *args):
        import pywt
        #data=self.df_select[self.select_name]
        
        self.dlg_SWT=SWT_dialog(args[0])
        if self.dlg_SWT.exec(): 
            
            try:
                y_smooth, coeff, coeff_new=SWT.SWT_Wavelet(E_t, self.dlg_SWT.wt, int(self.dlg_SWT.Level_num), self.dlg_SWT.max_num)
                
                data_combined=self.combine_fft_data(t_ps, y_smooth)

                name_smooth=self.select_name+'_SWT_Wavelet='+self.dlg_SWT.wt+'_level='+self.dlg_SWT.Level_num
                self.name_smooth=name_smooth
                self.df_select[name_smooth]=data_combined
                self.plot_data_tab2(name_smooth)
                
                self.add_to_list2(name_smooth)
            except:
                print('Filter error')
            #pg.plot(t, y_smooth)
        #name_smooth=self.select_name+'_swt'
        

    def add_to_list2(self, name):
        self.listWidget2.addItem(name)

    def add_left2(self):
        item=self.listWidget2.selectedItems()[0]
        name=item.text()
        self.model_left.appendRow(QStandardItem(name))
        self.df_left[name]=self.df_select[name]
        
    def plot_data_tab2(self, name):
        # update figure in tab 2
        #plt.clf()
        data_to_plot=self.df_select[name]
        self.FigureSignal2.addLegend()
        self.FigureSignal2.plot(data_to_plot['Time'],data_to_plot['Signal'], pen=pg.mkPen(color=pg.intColor(self.plot_counter2), width=2), name=name)
        self.FigureFFT2.addLegend()
        self.FigureFFT2.plot(data_to_plot['Frequency'],abs(data_to_plot['FT_complex']), pen=pg.mkPen(color=pg.intColor(self.plot_counter2), width=2), name=name)
        self.plot_counter2=self.plot_counter2+1
        
    def clear_tab2(self):
        self.FigureSignal2.clear()
        self.FigureFFT2.clear()
        self.model_smooth.clear()
        self.df_select.clear()
        
    def clear_plot2(self):
        self.FigureSignal2.clear()
        self.FigureFFT2.clear()
    def replot2(self):
        # update list view in "Select file name"
        Index = self.listWidget2.selectedItems()[0]
        data_name=Index.text()
        self.plot_data_tab2(data_name)
        
    def SaveFile2(self):
        Index = self.listWidget2.selectedItems()[0]
        data_name=Index.text()
        data_to_save=self.df_select[data_name]
        Path = QFileDialog.getSaveFileName(self, 'Save File', data_name+'.dat', )[0]
        with open(Path, 'w') as file:            
            data_to_save.to_csv(file, sep='\t', index=False)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
