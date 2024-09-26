"jongcheol1422@gmail.com"

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = pd.read_csv('M16-F2-73IR.csv')
num_spectra = sum('cm-1' in col for col in data.columns)
[start1, start2, start3] = [990, 1210, 1434]

start_wavenumbers = []

#def-----plot----raw&treated----plots------------------------------------------
def plot_single_pair_with_vertical_line(raw_data, smoothed_data, spectrum_index, start_wavenumbers):
    plt.figure(figsize=(10, 8))
    wavenumber_col = 'cm-1' if spectrum_index == 0 else f'cm-1.{spectrum_index}'
    intensity_col = 'mV' if spectrum_index == 0 else f'mV.{spectrum_index}'
    
    plt.plot(raw_data[wavenumber_col], raw_data[intensity_col], label='Raw Spectrum', linestyle='--', alpha=0.5)    
    plt.plot(smoothed_data[wavenumber_col], smoothed_data[intensity_col], label=f'Smth Spectrum_{start1,start2,start3}')

    #vertical gridlines
    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1)
    
    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.legend(prop={'size':8})
    plt.title(f'Comparison {spectrum_index + 1} with Start Lines')
    plt.gca().invert_xaxis()  #x-axis reverse
    ax = plt.gca()  #current axes
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.show()

#def-----plot----all_raw-----plots---------------------------------------------
def plot_all_raw_data(raw_data, num_spectra):
    plt.figure(figsize=(10, 8))
    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'
        plt.plot(raw_data[wavenumber_col], raw_data[intensity_col], linestyle='--', alpha=0.5, label=f'spect {i+1}')

    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1)

    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.title(f'All raw spectrum_{start1,start2,start3}', fontsize=16)
    plt.legend(prop={'size':8})
    plt.gca().invert_xaxis()
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.savefig('All_Raw.png', dpi=300)  #save figure
    plt.show()

#def-----plot----all_treated-----plots-----------------------------------------
def plot_all_smoothed_data(smoothed_data, num_spectra):
    plt.figure(figsize=(10, 8))
    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'
        plt.plot(smoothed_data[wavenumber_col], smoothed_data[intensity_col], label=f'spect {i+1}')

    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1)

    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.title(f'All smth spectrum_dv_{start1,start2,start3}', fontsize=16)
    plt.legend(prop={'size':8})
    plt.gca().invert_xaxis()
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.savefig('All_smth_spectra_dv.png', dpi=300)
    plt.show()
    
#def-----data-----treatment----------------------------------------------------
def adjust_intensities(data, start):
    before4 = start - 8
    before3 = start - 6
    before2 = start - 4
    before1 = start - 2
    target = start + 2
    target2 = start + 4
    target3 = start + 6
    target4 = start + 8

    global start_wavenumbers
    start_wavenumbers.extend([before2, before1, start, target])

    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else 'cm-1'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'


        if all(wavenumber in data[wavenumber_col].values for wavenumber in [before2, before1, start, target]):            
            before4_intensity = data.loc[data[wavenumber_col] == before4, intensity_col].values[0]
            before3_intensity = data.loc[data[wavenumber_col] == before3, intensity_col].values[0]
            #before2_intensity = data.loc[data[wavenumber_col] == before2, intensity_col].values[0]
            #before1_intensity = data.loc[data[wavenumber_col] == before1, intensity_col].values[0]           
            #target_intensity = data.loc[data[wavenumber_col] == target, intensity_col].values[0]
            #target2_intensity = data.loc[data[wavenumber_col] == target2, intensity_col].values[0]  
            target3_intensity = data.loc[data[wavenumber_col] == target3, intensity_col].values[0]  
            target4_intensity = data.loc[data[wavenumber_col] == target4, intensity_col].values[0]              
            
            temp = ((before3_intensity + before4_intensity)/2) / ((target3_intensity + target4_intensity)/2)
            #print[temp]
            #int at 'before1' and 'start' are replaced with the int at 'before2'
            data.loc[data[wavenumber_col] == before2, intensity_col] = before3_intensity
            data.loc[data[wavenumber_col] == before1, intensity_col] = before3_intensity
            data.loc[data[wavenumber_col] == start, intensity_col] = before3_intensity

            target_idx = data.index[data[wavenumber_col] >= target].tolist() # target and the above
            data.loc[target_idx, intensity_col] *= temp
    return data

#def-----data-----treatment----------------------------------------------------
raw_data = data.copy()
data = adjust_intensities(data, start1)
data = adjust_intensities(data, start2)
data = adjust_intensities(data, start3)

#repeat for other spectra
for i in range(num_spectra):
    plot_single_pair_with_vertical_line(raw_data, data, i, start_wavenumbers)

plot_all_raw_data(raw_data, num_spectra)
plot_all_smoothed_data(data, num_spectra)

data.to_excel('smoothed_data_dv.xlsx', index=False)
