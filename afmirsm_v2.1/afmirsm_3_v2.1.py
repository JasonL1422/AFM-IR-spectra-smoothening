"jongcheol1422@gmail.com"

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = pd.read_csv('sample.csv')
num_spectra = sum('cm-1' in col for col in data.columns)

#def-----plot----raw&treated----plots------------------------------------------
start_wavenumbers = []
def plot_single_pair_with_vertical_line(raw_data, smoothed_data, spectrum_index, start_wavenumbers):
    plt.figure(figsize=(10, 8))
    wavenumber_col = 'cm-1' if spectrum_index == 0 else f'cm-1.{spectrum_index}'
    intensity_col = 'mV' if spectrum_index == 0 else f'mV.{spectrum_index}'

    plt.plot(raw_data[wavenumber_col], raw_data[intensity_col], label='Raw Spectrum', linestyle='--', alpha=0.5)
    plt.plot(smoothed_data[wavenumber_col], smoothed_data[intensity_col], label='Smoothed Spectrum')

    #vertical gridlines
    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1, label=f'Start at {start}')
    
    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.legend(prop={'size':6})
    plt.title(f'Comparison of Raw and Smoothed Spectrum {spectrum_index + 1} with Start Lines')
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
        plt.plot(raw_data[wavenumber_col], raw_data[intensity_col], linestyle='--', alpha=0.5, label=f'Raw Spectrum {i+1}')

    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1, label=f'Start at {start}')

    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.title('All Raw Spectra', fontsize=16)
    plt.legend(prop={'size':6})
    plt.gca().invert_xaxis()
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.savefig('All_Raw_Spectra.png', dpi=300)  #save figure
    plt.show()

#def-----plot----all_treated-----plots-----------------------------------------
def plot_all_smoothed_data(smoothed_data, num_spectra):
    plt.figure(figsize=(10, 8))
    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'
        plt.plot(smoothed_data[wavenumber_col], smoothed_data[intensity_col], label=f'Smoothed Spectrum {i+1}')

    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1, label=f'Start at {start}')

    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.title('All Smoothed Spectra', fontsize=16)
    plt.legend(prop={'size':6})
    plt.gca().invert_xaxis()
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.savefig('All_Smoothed_Spectra.png', dpi=300)
    plt.show()

#def-----data-----treatment----------------------------------------------------
def adjust_intensities(data, start):
    global start_wavenumbers
    before1 = start - 2
    target = start + 2

    start_wavenumbers.extend([before1, start, target])

    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'

        if before1 in data[wavenumber_col].values:
            before1_intensity = data.loc[data[wavenumber_col] == before1, intensity_col].values[0]
            data.loc[data[wavenumber_col] == start, intensity_col] = before1_intensity

        if target in data[wavenumber_col].values:
            #int at 'before1' and 'start' are replaced with the int at 'target'
            start_intensity = data.loc[data[wavenumber_col] == start, intensity_col].values[0]
            target_intensity = data.loc[data[wavenumber_col] == target, intensity_col].values[0]
            adjustment_factor = start_intensity / target_intensity if target_intensity else 1

            #adjustment factor treated
            target_idx = data.index[data[wavenumber_col] >= target].tolist()
            data.loc[target_idx, intensity_col] *= adjustment_factor

    return data

#def-----data-----treatment----------------------------------------------------
raw_data = data.copy()
data = adjust_intensities(data, 990)  #this automatically sets before1=988, and target=992
data = adjust_intensities(data, 1210)  #adjusts for the next range
data = adjust_intensities(data, 1434)  #adjusts for another range

#repeat for other spectra
for i in range(num_spectra):
    plot_single_pair_with_vertical_line(raw_data, data, i, start_wavenumbers)

plot_all_raw_data(raw_data, num_spectra)
plot_all_smoothed_data(data, num_spectra)

data.to_excel('smoothed_data.xlsx', index=False)
