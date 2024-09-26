# AFM-IR-spectra-smoothening

**[Purpose]** 
<br> To smoothen the AFM-IR spectra due to the laser chip switch at 990, 1210, 1434. The QCL laser in Bruker Icon-IR consist of four chips, each covering four different ranges of wavenumbers. Even though the tilt mirror is calibrated at IR reference (PMMA), the data point discrepancies are inevitable  due to your sample surface geometry, tip draft, etc.
<p align="center">
  <img width="800" src="https://github.com/JasonL1422/AFM-IR-spectra-smoothening/blob/main/etc/Fig2.png">
</p>

**[How to use]**
<br> Adjust the start numbers (start1, start2, start3) and run. 
-	If the data interval is 1cm-1, adjust the line 82-89

**[Notes]**
-	The input .csv file should be in the directory where the Python script is located.
-	Check the input data structure. compare with the sample data.
-	The data points near the 'start' numbers should be hidden and not interpreted. 
