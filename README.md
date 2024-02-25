# AFM-IR-spectra-smoothening

**[Purpose]** 
<br> This script was created to smoothen the gap in AFM-IR spectra from laser chip switch. The QCL laser in Bruker Icon-IR consist of four chips, each covering four different ranges of wavenumbers. The chip switch occurs at ~991, 1212, 1433 cm-1. Even though the tilt mirror calibration is perfect at IR reference (PMMA), the data point discrepancies are inevitable often due to your sample surface geometry, tip draft, etc.       **[Contact]** Jongcheol Lee (jongcheol1422@gmail.com) 2024.02.25
<p align="center">
  <img width="800" src="https://github.com/JasonL1422/AFM-IR-spectra-smoothening/blob/main/etc/Fig2.png">
</p>

**[How it works]**
<br> Once you pick a wavenumber (the ‘start’ wavenumber), the script sets ‘before’ and ‘after’ (named “target” in the script) wavenumbers. The intensities at the start wavenumber are replaced with the one at the ‘before’ wavenumber. The intensities after that are (including the one at ‘after’ wavenumber) are adjusted (divided or multiplied by a certain numbers) to shift down or raise the later range of the spectrum.

**[How to use]**
-	Examine your raw spectrum, select the ‘start’ wavenumber, and adjust the numbers in the script line ~105:
-	If your data interval is 1cm-1, adjust the numbers in line ~74 in the script to ‘-1’ and ‘+1’  (the given sample data is with a 2 cm-1 interval):

**[Notes]**
-	There are two versions available. One with number 3 makes the three intensity numbers, before and after the start wavenumber, the same (flat). The other with number 4 makes the total four intensity numbers the same (before2, before1, start, after).
-	The input .csv file should be in the directory where the Python script is located.
-	The operation applies to all spectra in the initial .csv file and generate smoothened spectra in a separate .xlsx file. 
-	The script also produces plots (it may ask you to install something for plotting). The three or four vertical gray lines are where the intensity numbers were flattened.
-	The input data should be in a certain format (column, row). The given sample is as it is from Nanoscope software from Bruker. If your data are from different software, it should be adjusted manually. Please open the sample.csv. and check.
-	Users are encouraged to try both versions according to their case and select the proper ‘start’ wavenumbers to minimize the data misuse. The data/peak interpretation near those numbers could be unreliable. 


