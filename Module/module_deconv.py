import pylops
from GUI import FISTA_gui, AFISTA_gui
from PyQt5.QtWidgets import (
    QDialog, QFileDialog, QWidget,QGroupBox, QDialogButtonBox, QLineEdit, QGridLayout, QCheckBox, QHBoxLayout
)
from PyQt5.QtGui import QIntValidator
import pyqtgraph as pg
import pandas as pd
import numpy as np
#--------------------------------------Load file dialog ----------------------------------------------------------------------                
class Load_file_dialog(QDialog, QWidget):
    def __init__(self, data):
        super(QWidget, self).__init__()
        #self.setupUi(self)
        
        form_group_box = QGroupBox("column headers")
        file_name_group_box=QGroupBox('Append file name')
        timebase_group=QGroupBox('Time')
        signal_group=QGroupBox('Signal')
        freqbase_group=QGroupBox('Freq')
        ft_group=QGroupBox('FT_complex')
        layout_col = QGridLayout()
        layout_time=QGridLayout()
        layout_sig=QGridLayout()
        layout_freq=QGridLayout()
        layout_ft=QGridLayout()
        layout_file=QGridLayout()
        self.col_num=len(data.columns)
        self.qlineEdit=[None]*self.col_num
        self.col_indx=[None]*4
        self.timebase=[None]*self.col_num
        self.signal=[None]*self.col_num
        self.freqbase=[None]*self.col_num
        self.ft_complex=[None]*self.col_num
        col_name=data.columns
        self.col_header=[None]*self.col_num
        for i in range(self.col_num):
            self.qlineEdit[i]=QLineEdit()
            self.timebase[i]=QCheckBox()
            self.freqbase[i]=QCheckBox()
            self.signal[i]=QCheckBox()
            self.ft_complex[i]=QCheckBox()
            self.qlineEdit[i].setText(col_name[i])
            layout_col.addWidget(self.qlineEdit[i], i, 0)
            layout_time.addWidget(self.timebase[i], i,0)
            layout_sig.addWidget(self.signal[i],i,0)
            layout_freq.addWidget(self.freqbase[i],i,0)
            layout_ft.addWidget(self.ft_complex[i],i,0)
        
        self.filename=QLineEdit()
        layout_file.addWidget(self.filename,1,0)
        form_group_box.setLayout(layout_col)
        timebase_group.setLayout(layout_time)
        signal_group.setLayout(layout_sig)
        freqbase_group.setLayout(layout_freq)
        ft_group.setLayout(layout_ft)
        file_name_group_box.setLayout(layout_file)
        main_layout = QHBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(timebase_group)
        main_layout.addWidget(signal_group)
        main_layout.addWidget(freqbase_group)
        main_layout.addWidget(ft_group)
        main_layout.addWidget(file_name_group_box)
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
        for i in range(self.col_num):
                if self.timebase[i].isChecked()==True:
                       self.col_indx[0]=i
                elif self.signal[i].isChecked()==True:
                        self.col_indx[1]=i
                elif self.freqbase[i].isChecked()==True:
                        self.col_indx[2]=i
                elif self.ft_complex[i].isChecked()==True:
                        self.col_indx[3]=i
                else:              
                       pass
        if self.filename.text():
                self.f_name=self.filename.text()
        else:
                self.f_name=None
        #self.col_header_new=list(filter(None, self.col_header))
        #print(self.col_indx)
        #self.col_indx_new=[x for x in self.col_indx if x is not None]
        
        
        self.accept()
    
    def exit(self):
        self.close() 

#--------------------------------------Deconvolution dialog---------------------------------------------------------

class FISTA_dialog(QDialog, FISTA_gui.Ui_Dialog):
        def __init__(self, data_ref, data_sample, sample_name):
                super().__init__()
                # Run the .setupUi() method to show the GUI
                self.setupUi(self)
                self.data_ref=data_ref
                self.data_sample=data_sample
                self.data_name=sample_name
                # number of iteration input
                self.niter_num=100
                self.niter.setValidator(QIntValidator())
                self.niter.setText(str(self.niter_num))
                # tolerant
                self.Tol_num=1e-5
                self.Tol.setText(str(self.Tol_num))

                # Push Button
                self.OKButton.clicked.connect(self.submitclose)
                self.ClearButton.clicked.connect(self.clear_max)
                self.CancelhButton.clicked.connect(self.exit)
                # Text browser
                self.textBrowser.setAcceptRichText(True)
                # Plot data
                #self.GraphWidget.setBackground('w')
                self.GraphWidget1.plot(self.data_sample['Time'], self.data_sample['Signal'], pen=pg.mkPen(0))
                # Press Run push button
                self.RunButton.clicked.connect(self.Run_FISTA)
                # Press Save button
                self.SaveButton.clicked.connect(self.SaveFile)
        
    
        def Run_FISTA(self, ):
                t=self.data_ref['Time']
                Kernel=self.data_ref['Signal']
                y=self.data_sample['Signal']
                N=len(Kernel)
                if not self.niter.text():
                        pass
                else:
                        self.niter_num=int(self.niter.text())
                if not self.Tol.text():
                        pass
                else:
                        self.Tol_num=float(self.Tol.text())
                Cop=pylops.signalprocessing.Convolve1D(N, h=Kernel)
                #dottest(Cop, verb=True)
                
                pen = pg.mkPen(1)
                #L = np.abs((Cop.H * Cop).eigs(1)[0])
                xfista, iteration_result, resista = pylops.optimization.sparsity.fista(
                        Cop, y, niter=self.niter_num, eps=5e-1, tol=self.Tol_num, threshkind='soft', show=True)
                

                self.GraphWidget2.plot(t, xfista, pen=pen)
                text='Acutal iteration runned'+str(iteration_result)
                self.textBrowser.append(text)
                d={'Time':t, 'Signal': xfista}
                self.deconv_data=pd.DataFrame(data=d)

        def SaveFile(self):
            data_to_save=self.deconv_data
            Path = QFileDialog.getSaveFileName(self, 'Save File', self.data_name+'_deconvoluted'+'.dat', )[0]
            with open(Path, 'w') as file:            
                data_to_save.to_csv(file, sep='\t', index=False)
        
        def submitclose(self):
            
                self.accept()
    
        def clear_max(self):
                #self.GraphWidget1.clear()
                self.GraphWidget2.clear()
                
                self.niter_num=100 
                self.Tol_num=1e-5
                self.textBrowser.clear()
        
        def exit(self):
                self.close()             
                
class AFISTA_dialog(QDialog, AFISTA_gui.Ui_Dialog):
        def __init__(self, data_ref, data_sample):
                super().__init__()
                # Run the .setupUi() method to show the GUI
                self.setupUi(self)
                self.data_ref=data_ref
                self.data_sample=data_sample
                # number of iteration input
                self.niter_num=100
                self.niter.setValidator(QIntValidator())
                self.niter.setText(str(self.niter_num))
                # tolerant
                self.Tol_num=1e-5
                self.Tol.setText(str(self.Tol_num))

                # Push Button
                self.OKButton.clicked.connect(self.submitclose)
                self.ClearButton.clicked.connect(self.clear_max)
                self.CancelhButton.clicked.connect(self.exit)
                # Text browser
                
                self.textBrowser.setAcceptRichText(True)
                # Plot data
                
                #self.GraphWidget.setBackground('w')
                self.GraphWidget1.plot(self.data_sample['Time'], self.data_sample['Signal'], pen=pg.mkPen(0))
                # Press Find Max push button
                self.RunButton.clicked.connect(self.Run_FISTA)
        
    
        def Run_FISTA(self, ):
                t=self.data_ref['Time']
                Kernel=self.data_ref['Signal']
                y=self.data_sample['Signal']
                N=len(Kernel)
                if not self.niter.text():
                        pass
                else:
                        self.niter_num=int(self.niter.text())
                if not self.Tol.text():
                        pass
                else:
                        self.Tol_num=float(self.Tol.text())
                Cop=pylops.signalprocessing.Convolve1D(N, h=Kernel)
                #dottest(Cop, verb=True)
                
                pen = pg.mkPen(1)
                #L = np.abs((Cop.H * Cop).eigs(1)[0])
                xfista, iteration_result, resista = pylops.optimization.sparsity.fista(
                        Cop, y, niter=self.niter_num, eps=5e-1, tol=self.Tol_num, threshkind='soft', show=True)
                

                self.GraphWidget2.plot(t, xfista, pen=pen)
                text='Acutal iteration runned'+str(iteration_result)
                self.textBrowser.append(text)
                d={'Time':t, 'Signal': xfista}
                self.deconv_data=pd.DataFrame(data=d)

        def submitclose(self):
            
                self.accept()
    
        def clear_max(self):
                #self.GraphWidget1.clear()
                self.GraphWidget2.clear()
                
                self.niter_num=100 
                self.Tol_num=1e-5
                self.textBrowser.clear()
        
        def exit(self):
                self.close()        
                