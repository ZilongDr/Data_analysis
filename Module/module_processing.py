from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout,QGridLayout,QLineEdit, QWidget,QGroupBox, QDialogButtonBox, QCheckBox
)
import pyqtgraph as pg
import numpy as np

from scipy.fft import next_fast_len
from func import FFT as FT
from func import unit_conversion as ut
from func import misc
from PyQt5.QtGui import QIntValidator

from GUI import Moving_average_gui, Savgol_gui, SWT_gui, TFWindow_gui, BaseLine_sub_gui, BaseLine_gui
from pybaselines import Baseline


#--------------------------------------Dialog for load files--------------------------------------------------------------------------------------------------------
class Load_file_dialog(QDialog, QWidget):
    def __init__(self, data):
        super(QWidget, self).__init__()
        #self.setupUi(self)
        form_group_box = QGroupBox("column headers")
        use_header_box=QGroupBox('Use header as append name')
        timebase_group=QGroupBox('Time')
        signal_group=QGroupBox('Signal')
        layout = QGridLayout()
        layout_time=QGridLayout()
        layout_sig=QGridLayout()
        layout_file=QGridLayout()     
        self.col_num=len(data.columns)
        self.signal_indx=[None]*self.col_num
        self.qlineEdit=[None]*self.col_num
        self.timebase=[None]*self.col_num
        self.signal=[None]*self.col_num       
        col_name=data.columns
        self.col_header=[None]*self.col_num
        self.signal_header=[None]*self.col_num
        for i in range(self.col_num):
            self.qlineEdit[i]=QLineEdit()
            self.timebase[i]=QCheckBox()
            self.signal[i]=QCheckBox()
            self.qlineEdit[i].setText(col_name[i])
            layout.addWidget(self.qlineEdit[i], i, 0)
            layout_time.addWidget(self.timebase[i], i, 0)
            layout_sig.addWidget(self.signal[i], i,0)
        self.filename=QCheckBox()
        layout_file.addWidget(self.filename,1,0)
        form_group_box.setLayout(layout)
        timebase_group.setLayout(layout_time)
        signal_group.setLayout(layout_sig)
        use_header_box.setLayout(layout_file)
        main_layout = QHBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(timebase_group)
        main_layout.addWidget(signal_group)
        main_layout.addWidget(use_header_box)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        #OK_button = QPushButton('OK')
        #OK_button.clicked.connect(self.submitclose)
        button_box.accepted.connect(self.submitclose)
        button_box.rejected.connect(self.exit)
        main_layout.addWidget(button_box)
        button_box.button(QDialogButtonBox.Ok).setText("OK")
        button_box.button(QDialogButtonBox.Cancel).setText("Cancel")
        self.setLayout(main_layout)
        self.setWindowTitle("Set Columns headers")


    def submitclose(self):
        j=0
        for i in range(self.col_num):
            self.col_header[i]=self.qlineEdit[i].text()
            if self.timebase[i].isChecked()==True:
                    self.time_indx=i
            elif self.signal[i].isChecked()==True:
                    self.signal_indx[j]=i
                    if self.filename.isChecked()==True:
                        self.signal_header[j]=self.col_header[i]
                    else:
                        self.signal_header[j]=None
                    j=j+1
        '''
        if self.filename.text():
                self.f_name=self.filename.text()
        else:
                self.f_name=None
        '''
        self.accept()
    
    def exit(self):
        self.close() 

#--------------------------------------Dialog for baseline subtraction---------------------------------------------------------------------------------------------
class BaseLine_Sub_dialog(QDialog, BaseLine_sub_gui.Ui_Dialog):
    def __init__(self, data):
        super().__init__()
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        self.data=data
        self.t_ps=misc.convert_to_np(data['Time'])
        self.E_t=misc.convert_to_np(data['Signal'])
        self.freq_THz=misc.convert_to_np(data['Frequency'])
        self.FT_complex=misc.convert_to_np(data['FT_complex'])
        self.phase=np.angle(self.FT_complex)
        self.amp=abs(self.FT_complex)
        # Baseline initialization:
        self.baseline_num=0
        self.plot_ini()
        self.SetWindowButton.clicked.connect(self.Run_baseline)
        self.ClearButton.clicked.connect(self.clear)
        self.buttonBox.accepted.connect(self.submitclose)
        self.buttonBox.rejected.connect(self.exit)
        
    def regionUpdated(self):
        self.time_lw=self.region.getRegion()[0]
        self.time_hg=self.region.getRegion()[1]
        self.region.setRegion((self.time_lw, self.time_hg))
        
    def plot_ini(self):
        self.FigureFFT.clear()
        self.Figure.clear()
        # Plot data
        #Initialize color counter:
        self.plot_counter=1
        pen=pg.mkPen(color=pg.intColor(self.plot_counter))
        self.FigureFFT.setMouseEnabled(x=True, y=True)
        self.region = pg.LinearRegionItem(values=(self.freq_THz[0], self.freq_THz[200]), bounds=(self.freq_THz[0], self.freq_THz[-1]),brush=(100, 100, 100, 60))
        self.FigureFFT.addItem(self.region, ignoreBounds=True)
        self.FigureFFT.plot(self.freq_THz, self.amp, pen=pen)
        self.region.sigRegionChangeFinished.connect(self.regionUpdated)
        self.Figure.plot(self.t_ps, self.E_t, pen=pen)
    
    def update_plot(self,):
        self.plot_counter=self.plot_counter+1
        pen=pg.mkPen(color=pg.intColor(self.plot_counter))
        self.FigureFFT.plot(self.freq_THz, self.amp_filtered, pen=pen)
        self.Figure.plot(self.t_ps, self.E_t_window, pen=pen)        
    
    def Run_baseline(self):
        self.regionUpdated()
        indx_lw, _=misc.find_array_index(self.freq_THz, self.time_lw)
        indx_hg, _=misc.find_array_index(self.freq_THz, self.time_hg)
        Window=np.zeros_like(self.freq_THz)
        Window[indx_lw:indx_hg]=1
        self.amp_filtered=np.multiply(Window, self.amp)
        self.E_w=self.amp_filtered*np.exp(1j*self.phase)
        f=ut.THz_to_Hz(self.freq_THz)
        Npad=next_fast_len(2**12)
        t, E_t_window_full=FT.IFFT(f, self.E_w, Npad)
        self.E_t_window=E_t_window_full[0:len(E_t_window_full)//2]
        self.update_plot()
    
    def clear(self):
        self.plot_ini()
    
    def submitclose(self):
        self.accept()
        
    def exit(self):
        self.close()
        
    
#--------------------------------------Dialog for smoothing using moving average------------------------------------------------------------------------------------
class Moving_average_dialog(QDialog, Moving_average_gui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        self.Window_num=0
        self.WindowLength.setValidator(QIntValidator())
        self.OKButton.clicked.connect(self.submitclose)
    
    def submitclose(self):
        self.Window_num=self.WindowLength.text()
        self.accept()

#--------------------------------------Dialog for smoothing using Savgol filter------------------------------------------------------------------------------------

class Savgol_dialog(QDialog, Savgol_gui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        self.Window_num=0
        self.FilterOrder_num=0
        self.WindowLength.setValidator(QIntValidator())
        self.FilterOrder.setValidator(QIntValidator())
        self.OKButton.clicked.connect(self.submitclose)
    
    def submitclose(self):
        self.Window_num=self.WindowLength.text()
        self.FilterOrder_num=self.FilterOrder.text()
        self.accept()

# ----------------------------Dialog window for smoothing using SWT----------------------------------------------------------------

class SWT_dialog(QDialog, SWT_gui.Ui_Dialog):
    def __init__(self, data):
        super().__init__()
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        # Configure Combobox
        wt_item=['db4','sym4']
        self.WaveletComboBox.addItems(wt_item)
        self.wt=''
        # Decomposition level input
        self.Level_num=0
        self.Level.setValidator(QIntValidator())
        # Push Button
        self.OKButton.clicked.connect(self.submitclose)
        self.ClearButton.clicked.connect(self.clear_max)
        # Initilize data set from data input
        self.data=data

        # Plot data
        pen = pg.mkPen(color=(255, 0, 0))
        #self.Figure.setBackground('w')
        self.Figure.setMouseEnabled(x=True, y=True)
        self.region = pg.LinearRegionItem(values=(data['Time'][0], data['Time'][100]), bounds=(data['Time'].iloc[0], data['Time'].iloc[-1]),brush=(100, 100, 100, 60))
        self.Figure.addItem(self.region, ignoreBounds=True)
        self.Figure.plot(data['Time'], data['Signal'], pen=pen)
        self.region.sigRegionChangeFinished.connect(self.regionUpdated)
        # Initialize to store the select region ede
        self.time_lw=0
        self.time_hg=0
        # Initilize a list to store all max value
        self.max_value=[]
        self.max_num=0
        # Set the select range and calculate the maximum y value in the range:
        # Press Find Max push button
        self.FindMaxButton.clicked.connect(self.find_max)

    def regionUpdated(self):
        self.time_lw=self.region.getRegion()[0]
        self.time_hg=self.region.getRegion()[1]

    def find_max(self):
        d_array=misc.convert_to_np(self.data['Time'])
        lw_indx=misc.find_array_index(d_array, self.time_lw)[0]
        hg_indx=misc.find_array_index(d_array,self.time_hg)[0]
        #print(lw_indx, hg_indx)
        mx=(self.data['Signal'].iloc[lw_indx:hg_indx]).abs().max()
        
        self.max_value.append(mx)
        
        #self.max_num=max(self.max_value)
        self.lcdNumber.display(mx)

    def submitclose(self):
        self.wt=self.WaveletComboBox.currentText()
        array=np.array(self.max_value)
        array=array[~np.isnan(array)]
        self.max_num=np.amax(array)
        self.Level_num=self.Level.text()
        self.accept()
    
    def clear_max(self):
        self.lcdNumber.display(0)
        self.max_num=0
# ----------------------------Dialog window for removing ambient effect----------------------------------------------------------------

class TFWindow_dialog(QDialog, TFWindow_gui.Ui_Dialog):
    def __init__(self, data_ref, data_sample):
        super().__init__()
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        # Push Button
        self.OKButton.clicked.connect(self.submitclose)
             
        # Remove NaN in the data
        self.t_ps_ref=misc.convert_to_np(data_ref['Time'])
        self.t_ps_sample=misc.convert_to_np(data_sample['Time'])

        self.E_t_ref=misc.convert_to_np(data_ref['Signal'])
        self.E_t_sample=misc.convert_to_np(data_sample['Signal'])
        
        self.f_ref_0=data_ref['Frequency']
        self.Amp_ref_0=abs(data_ref['FT_complex'])
        # Find maximum peak position
        indx_max, _=misc.find_array_index(self.E_t_ref, max(abs(self.E_t_ref)))
        self.t_max=self.t_ps_ref[indx_max]
        
        # Combo box for window function:
        win_item=['boxcar','Gaussian','blackmanharris','flattop', 'hamming', 'nuttall']
        self.WinComboBox.addItems(win_item)
        self.win_func='boxcar'

        # Calculate transfer function in frequency domain:
        FT_sample=misc.convert_to_np(data_sample['FT_complex'])
        FT_ref=misc.convert_to_np(data_ref['FT_complex'])
        self.H=np.divide(FT_sample, FT_ref, out=np.zeros_like(FT_sample), where=FT_ref!=0)
        # Plot initialization:
        self.plot_ini()
        
        # Press Find time window push button
        self.SetWindowButton.clicked.connect(self.SetWindow)
        # Clear button:
        self.ClearButton.clicked.connect(self.ClearAll)
        #pg.plot(self.f_ref_0 ,abs(self.H))
        

    def regionUpdated(self):
        if self.win_func=='boxcar':
            self.time_lw=self.region.getRegion()[0]
            self.time_hg=self.region.getRegion()[1]
        else:
            distance=abs(self.t_max-self.region.getRegion()[0])
        
            self.time_lw=self.t_max-distance
            self.time_hg=self.t_max+distance
        self.region.setRegion((self.time_lw, self.time_hg))
        
        
    def SetWindow(self):

        from scipy.signal.windows import blackmanharris, boxcar, flattop, hamming, nuttall, gaussian
        from func import Gaussian_intensity as GS
        self.win_func=self.WinComboBox.currentText()
        self.regionUpdated()
        self.Window=np.zeros_like(self.t_ps_ref)
        indx_lw, _=misc.find_array_index(self.t_ps_ref, self.time_lw)
        indx_hg, _=misc.find_array_index(self.t_ps_ref, self.time_hg)
        if self.win_func=='Gaussian':
            fwhm=abs(self.time_hg-self.time_lw)*1
            #Window_kernel=GS.calc_I_t(self.t_ps2_ref[indx_lw:indx_hg], fwhm, 0)
            Window_kernel=gaussian(abs(indx_hg-indx_lw), fwhm, True)
        else:
            Window_kernel=locals()[str(self.win_func)](abs(indx_hg-indx_lw), True)
            
        self.Window[indx_lw: indx_hg]=Window_kernel
        self.E_t_ref_window=np.multiply(self.E_t_ref, self.Window)
        Npad=next_fast_len(2**12)
        t_s=ut.ps_to_s(self.t_ps_ref)
        f, self.E_ref_w_window=FT.FFT(t_s, self.E_t_ref_window, Npad)
        self.f_ref_THz=ut.Hz_to_THz(f)
        #self.E_ref_w=abs(self.E_ref_w_window)
        E_sample_w=np.array(np.multiply(self.E_ref_w_window, self.H), dtype=complex)
        t, self.E_sample_t_window=FT.IFFT(f, E_sample_w, Npad)
        self.E_sample_t_window=np.real(self.E_sample_t_window[:len(t)//2])
        
        self.update_plot()
        
    def update_plot(self):
        #self.FigureRef_FFT()
        #self.FigureRef.clear()
        #self.FigureRef_FFT.clear()
        self.plot_counter=self.plot_counter+1
        self.line_ref=self.FigureRef.plot(self.t_ps_ref, self.E_t_ref_window, pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2))
        self.FigureRef.plot(self.t_ps_ref, self.Window, pen=pg.mkPen(color=pg.intColor(self.plot_counter+2), width=2))
        self.line_FFT=self.FigureRef_FFT.plot(self.f_ref_THz, abs(self.E_ref_w_window), pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2))
        self.line_sample=self.FigureSample.plot(self.t_ps_sample, self.E_sample_t_window, pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2))

    def plot_ini(self):
        self.FigureRef.clear()
        self.FigureRef_FFT.clear()
        self.FigureSample.clear()
        # Plot data
        #Initialize color counter:
        self.plot_counter=1
        pen=pg.mkPen(color=pg.intColor(self.plot_counter))
        
        #self.FigureRef.setBackground('w')
        self.FigureRef.setMouseEnabled(x=True, y=True)
        self.region = pg.LinearRegionItem(values=(self.t_max-2, self.t_max+2), bounds=(self.t_ps_ref[0], self.t_ps_ref[-1]),brush=(100, 100, 100, 60))
        self.FigureRef.addItem(self.region, ignoreBounds=True)
        self.FigureRef.plot(self.t_ps_ref, self.E_t_ref, pen=pen)
        line_ver=pg.InfiniteLine(pos=self.t_max, angle=90)
        self.FigureRef.addItem(line_ver)
        self.region.sigRegionChangeFinished.connect(self.regionUpdated)
        self.FigureRef_FFT.plot(self.f_ref_0, self.Amp_ref_0)
        self.FigureRef_FFT.setXRange(0,3)
        #self.FigureTransfer.plot(self.f_ref_0, abs(self.H))
        #self.FigureTransfer.setXRange(0,3)
        self.FigureSample.plot(self.t_ps_sample, self.E_t_sample)

    
    def ClearAll(self):
        self.plot_ini()

        #self.FigureRef.removeItem(self.line_ref)
        #self.line_FFT.clear()
        #self.line_sample.clear()
    
                
    
    def submitclose(self):
        #self.wt=self.WaveletComboBox.currentText()
        
        self.accept()
    
    
class BaseLine_dialog(QDialog, BaseLine_gui.Ui_Dialog):
    def __init__(self, data_ref, data_sample):
        super().__init__()
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        # Push Button
        self.OKButton.clicked.connect(self.submitclose)
        # Set Order:
        self.OrderLineEdit.setText(str(100))
        
        # Remove NaN in the data
        t_ps_ref=np.array(data_ref['Time'])
        self.t_ps2_ref=t_ps_ref[~np.isnan(t_ps_ref)]
        t_ps_sample=np.array(data_sample['Time'])
        self.t_ps2_sample=t_ps_sample[~np.isnan(t_ps_sample)]
        
        E_t_ref=np.array(data_ref['Signal'])
        self.E_t2_ref=E_t_ref[~np.isnan(E_t_ref)]
        E_t_sample=np.array(data_sample['Signal'])
        self.E_t2_sample=E_t_sample[~np.isnan(E_t_sample)]
        
        self.f_ref_0=np.array(data_ref['Frequency'])
        self.Amp_ref_0=abs(data_ref['FT_complex'])
        self.phase_ref_0=np.angle(data_ref['FT_complex'])
        # Find maximum peak position
        indx_max, _=misc.find_array_index(self.E_t2_ref, max(abs(self.E_t2_ref)))
        self.t_max=self.t_ps2_ref[indx_max]
        
        # Combo box for window function:
        method_item=['Whittaker','Morphological','Polynomial']
        self.MethodComboBox.addItems(method_item)
        self.Method=''

        # Calculate transfer function in frequency domain:
        self.H=np.divide(data_sample['FT_complex'], data_ref['FT_complex'])
        # Plot initialization:
        self.plot_ini()
        
        # Press Find time window push button
        self.SubtractButton.clicked.connect(self.Subtract)
        # Clear button:
        self.ClearButton.clicked.connect(self.ClearAll)

        

          
        
    def Subtract(self):
        from pybaselines import Baseline
        indx_lw,_=misc.find_array_index(self.f_ref_0, self.freq_lw)
        indx_hg,_=misc.find_array_index(self.f_ref_0, self.freq_hg)
             
        self.Method=self.MethodComboBox.currentText()
        #Fit baseline in selected range
        baseline_fitter=Baseline(x_data=self.f_ref_0[indx_lw:indx_hg])
        order=int(self.OrderLineEdit.text())
        if self.Method=='Whittaker':
            baseline=baseline_fitter.arpls(-self.Amp_ref_0[indx_lw:indx_hg], lam=order)[0]
        elif self.Method=='Morphological':
            baseline=baseline_fitter.mor(-self.Amp_ref_0[indx_lw:indx_hg], half_window=order)[0]
        elif self.Method=='Polynomial':
            baseline=baseline_fitter.modpoly(-self.Amp_ref_0[indx_lw:indx_hg], poly_order=order)[0]
        
        #offset and Zero padd the rest of the frequency
        baseline_amp=-baseline
        baseline_amp_full=np.zeros_like(self.Amp_ref_0)
        offset=baseline_amp[-1]
        baseline_amp_full[indx_lw:indx_hg]=baseline_amp-offset
        baseline_amp_full[baseline_amp_full<0]=0
        
        self.baseline_complex=baseline_amp_full*np.exp(1j*self.phase_ref_0)
        
        
        Npad=next_fast_len(2**12)
        t_s=ut.ps_to_s(self.t_ps2_ref)
        f_Hz=ut.THz_to_Hz(self.f_ref_0)
        _, self.E_t_ref_bs=FT.IFFT(f_Hz, self.baseline_complex, Npad)
        self.E_t_ref_bs=np.real(self.E_t_ref_bs[0:len(self.t_ps2_ref)])
        #self.E_ref_w=abs(E_ref_w_window)
        
        E_sample_w=np.multiply(self.baseline_complex, self.H)
        E_sample_w=np.array(E_sample_w, dtype=complex)
        _, self.E_t_sample_bs=FT.IFFT(f_Hz, E_sample_w, Npad)
        self.E_t_sample_bs=np.real(self.E_t_sample_bs[0:len(self.t_ps2_sample)])
        
        self.update_plot()
        
    def update_plot(self):
        #self.FigureRef_FFT()
        #self.FigureRef.clear()
        #self.FigureRef_FFT.clear()
        self.plot_counter=self.plot_counter+1
        self.FigureRef.plot(self.t_ps2_ref, self.E_t_ref_bs, pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2))
        #self.FigureRef.plot(self.t_ps2_ref, self.Window, pen=pg.mkPen(color=pg.color(0.5), width=1))
        self.FigureRef_FFT.plot(self.f_ref_0, abs(self.baseline_complex), pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2))
        self.FigureSample.plot(self.t_ps2_sample, self.E_t_sample_bs, pen=pg.mkPen(color=pg.intColor(self.plot_counter), width=2))

    
    def regionUpdated(self):
        self.freq_lw=self.region.getRegion()[0]
        self.freq_hg=self.region.getRegion()[1]
        #print(self.freq_hg, self.freq_lw)


    def plot_ini(self):
        self.FigureRef.clear()
        self.FigureRef_FFT.clear()
        self.FigureSample.clear()
        # Plot data
        
        #Initialize color counter:
        self.plot_counter=1
        pen=pg.mkPen(color=pg.intColor(self.plot_counter))
        
        #self.FigureRef.setBackground('w')
        self.FigureRef_FFT.setMouseEnabled(x=True, y=True)
        self.FigureRef.plot(self.t_ps2_ref, self.E_t2_ref, pen=pen)
        self.FigureRef_FFT.plot(self.f_ref_0, self.Amp_ref_0)
        self.FigureRef_FFT.setXRange(0,3)
        self.region = pg.LinearRegionItem(values=(self.f_ref_0[10], self.f_ref_0[100]), bounds=(self.f_ref_0[0], self.f_ref_0[-1]),brush=(100, 100, 100, 60))
        self.FigureRef_FFT.addItem(self.region, ignoreBounds=True)
        self.region.sigRegionChangeFinished.connect(self.regionUpdated)

        #self.FigureTransfer.plot(self.f_ref_0, abs(self.H))
        #self.FigureTransfer.setXRange(0,3)
        self.FigureSample.plot(self.t_ps2_sample, self.E_t2_sample)

    
    def ClearAll(self):
        self.plot_ini()

        #self.FigureRef.removeItem(self.line_ref)
        #self.line_FFT.clear()
        #self.line_sample.clear()
        
    def submitclose(self):
        #self.wt=self.WaveletComboBox.currentText()
        
        self.accept()
