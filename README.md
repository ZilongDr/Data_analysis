# Data_analysis
Programs for data analysis

# Step to use the program:
## Package to install before use:
1. Python>=3.8, better to be 3.9
2. pyqt5: https://anaconda.org/anaconda/pyqt
3. pylops: https://pylops.readthedocs.io/en/stable/installation.html
4. pyqtgraph: https://www.pyqtgraph.org/

## How to run the program:
### Step 1: Copy all the files to local directory.
### Step 2 : Run the .py files:
* Method 1:
Run the code "Data_processing.py" or "Data_deconvolution.py" in IDE e.g. VS code or Spyder.
* Method 2:
In the command line (Anaconda prompt), navigate to the folder where the .py files are located (use the 'cd' command), then type: python xxxx.py

## In "Data_processing.py":
### Tab 1: Load data 
* Load the data from file by first determining the number of rows to skip and the type of delimiter in the data file. One could load ".csv", ".txt" and ".dat" files.
* If the original data file contains comments, set number of "skip rows" to skip the lines of comments.
* Once the "load" button is pressed, a dialog will be pop up. Click the check boxes to determine the time axis and the signal axis. One could load multiple signals at one time. If "append header" check box is checked, the loaded file names will be appended with corresponding headers.
* The time domain and frequency domain data can be plotted after loading the file. The loaded file will be shown in the list.
* Use the "Subtract baseline" function to subtract the baseline in time domain or remove the low or high frequency components in frequency domain. Drag and set the region to determine the area to keep the frequency components. This is equivalent to performing a bandpass filter in frequency domain.
* Use the average function to average multiply files, by pressing the "Average" button. One can select multiple files by "Shift+" selecting the file names in the list.
* To save the data file by pressing "Save to file" button. The saved data contains both time and frequency domain results.
* Add the file to the left repository by pressing "Add to left" button for further data processing.
### Tab 2: Remove ambient (to be completed)
* Set reference and set sample data from left repository
* Press run to open the operation dialog
* At the moment, only "Window convolution" function works
* In the dialog, choose window function and drag the two vertical lines to set region to keep the main pulse in the reference sigal.
* The calculation process as following:

$H(f)=\frac{FFT[E_{sample}(t)]}{FFT[E_{ref}(t)]}$

$E_{win}(f)=FFT[E_{win}(t)]=FFT[W(t)*E_{ref}(t)]$

$E_{rmv}(t)=FFT^{-1}[H(f)*E_{win}(f)]$

where $H(f)$ is calculated transfer function in frequency domain, $E_{sample}(t)$ is measured time trace on sample, $E_{ref}(t)$ is measured reference time trace
, $W(t)$ is window function in time, $E_{win}(t)$ is snipped reference time trace, $E_{rmv}(t)$ is time trace measured on sample removed from ambient water absorption.

### Tab 3: Data processing (data smoothing)
* Load data to be smoothed by pressing the "Load from left" button
* Select smooth method in the drop box
* Press "select" button to open the operation dialog
* The "Wavelet" method uses SWT denoising method. First choose which wavelet to use (db4 or sym4), then choose the decomposition level. To determine the maximum noise level, 
put the selection region in the figure in the area without signal pulse, ideally before the arrival of the pulse. Then press "find max" button. Then press "OK" button to finish the operation.

## In "Data_deconvolution.py" (To be completed):
### Step 1: Load data from files
* One could choose to load both time and frequency domain data.
### Step 2: Select deconvolution method
* One could use Frequency domain method or Time domain method for the data deconvolution.
* Now only the Time domain -> FISTA method works.
### Step 3: Set reference and sample
* Choose which files to be used as reference and sample by first select the file listed on the left and then press "set ref" or "set sample" button
* Note: to use time domain method, select time traces from left. It won't work with frequency domain data and vice versa.
### Step 4: Press "Deconvolution" button to open the operation dialog
* In "FISTA" method: First drag the selection region to choose the main pulse of the reference pulse plotted in the upper panel. Then determine the number of 
iterations and tolerance. Then press "Run" button. Deconvoluted results in (short time) will be shown in lower panel. Time traces of measured sample data and 
re-constructed data are plotted in the upper panel.
* Pending issue: in "FISTA", it seems that the echoes in longer time scale cannot be seen from deconvoluted result.
### Further data analysis needs to be completed.



