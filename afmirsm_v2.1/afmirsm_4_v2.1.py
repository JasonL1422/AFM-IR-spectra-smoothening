# Contact: jongcheol1422@gmail.com

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV data
data = pd.read_csv('sample.csv')

# Determine the number of spectra
num_spectra = sum('cm-1' in col for col in data.columns)

# Initialize an empty list to collect start wavenumbers
start_wavenumbers = []

# Function to plot a single pair of raw and smoothed data with vertical lines at 'start' wavenumbers
def plot_single_pair_with_vertical_line(raw_data, smoothed_data, spectrum_index, start_wavenumbers):
    plt.figure(figsize=(10, 8))
    wavenumber_col = 'cm-1' if spectrum_index == 0 else f'cm-1.{spectrum_index}'
    intensity_col = 'mV' if spectrum_index == 0 else f'mV.{spectrum_index}'

    # Plot raw data
    plt.plot(raw_data[wavenumber_col], raw_data[intensity_col], label='Raw Spectrum', linestyle='--', alpha=0.5)
    
    # Plot smoothed data
    plt.plot(smoothed_data[wavenumber_col], smoothed_data[intensity_col], label='Smoothed Spectrum')

    # Add vertical lines at 'start' wavenumbers
    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1, label=f'Start at {start}')
    
    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.legend(prop={'size':6})
    plt.title(f'Comparison of Raw and Smoothed Spectrum {spectrum_index + 1} with Start Lines')
    plt.gca().invert_xaxis()  # Reverse the x-axis
    ax = plt.gca()  # Get the current axes
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.show()

# Plot all raw data across all spectra
def plot_all_raw_data(raw_data, num_spectra):
    plt.figure(figsize=(10, 8))
    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'
        plt.plot(raw_data[wavenumber_col], raw_data[intensity_col], linestyle='--', alpha=0.5, label=f'Raw Spectrum {i+1}')

    # Add vertical lines at 'start' wavenumbers
    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1, label=f'Start at {start}')

    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.title('All Raw Spectra', fontsize=16)
    plt.legend(prop={'size':6})
    plt.gca().invert_xaxis()  # Reverse the x-axis
    ax = plt.gca()  # Get the current axes
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.savefig('All_Raw_Spectra.png', dpi=300)  # Save the figure to a file
    plt.show()

# Plot all smoothed data across all spectra
def plot_all_smoothed_data(smoothed_data, num_spectra):
    plt.figure(figsize=(10, 8))
    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'
        plt.plot(smoothed_data[wavenumber_col], smoothed_data[intensity_col], label=f'Smoothed Spectrum {i+1}')

    # Add vertical lines at 'start' wavenumbers
    for start in start_wavenumbers:
        plt.axvline(x=start, color='gray', linestyle='-', linewidth=1, alpha=0.1, label=f'Start at {start}')

    plt.xlabel('Wavenumber (cm-1)', fontsize=16)
    plt.ylabel('Intensity (mV)', fontsize=16)
    plt.title('All Smoothed Spectra', fontsize=16)
    plt.legend(prop={'size':6})
    plt.gca().invert_xaxis()  # Reverse the x-axis
    ax = plt.gca()  # Get the current axes
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50))
    plt.savefig('All_Smoothed_Spectra.png', dpi=300)  # Save the figure to a file    
    plt.show()
    
def adjust_intensities(data, start):
    # Calculate before2, before1, and target wavenumbers based on the start wavenumber
    before2 = start - 4
    before1 = start - 2
    target = start + 2

    global start_wavenumbers
    # Add the wavenumbers for vertical lines in the plot
    start_wavenumbers.extend([before2, before1, start, target])

    for i in range(num_spectra):
        wavenumber_col = 'cm-1' if i == 0 else f'cm-1.{i}'
        intensity_col = 'mV' if i == 0 else f'mV.{i}'

        # Ensure 'before2', 'before1', 'start', and 'target' are in the data
        if all(wavenumber in data[wavenumber_col].values for wavenumber in [before2, before1, start, target]):
            before2_intensity = data.loc[data[wavenumber_col] == before2, intensity_col].values[0]
            # Replace intensities at 'before1' and 'start' with the intensity at 'before2'
            data.loc[data[wavenumber_col] == before1, intensity_col] = before2_intensity
            data.loc[data[wavenumber_col] == start, intensity_col] = before2_intensity

            start_intensity = before2_intensity  # Start intensity is now the same as before2
            target_intensity = data.loc[data[wavenumber_col] == target, intensity_col].values[0]
            adjustment_factor = start_intensity / target_intensity if target_intensity else 1

            # Apply the adjustment factor from the 'target' to the end of the data range
            target_idx = data.index[data[wavenumber_col] >= target].tolist()
            data.loc[target_idx, intensity_col] *= adjustment_factor

    return data


# Make a copy of the original data for plotting raw data
raw_data = data.copy()

# Adjust the intensities with a single 'start' wavenumber
data = adjust_intensities(data, 990)  # Automatically sets before2=986, before1=988, and target=992
data = adjust_intensities(data, 1210)  # Adjusts for the next range
data = adjust_intensities(data, 1434)  # Adjusts for another range

# Loop over each spectrum and plot the raw and smoothed data pair
for i in range(num_spectra):
    plot_single_pair_with_vertical_line(raw_data, data, i, start_wavenumbers)

# After plotting each pair, plot all raw data in one figure and all smoothed data in another figure
plot_all_raw_data(raw_data, num_spectra)
plot_all_smoothed_data(data, num_spectra)

# Save the smoothed data to a new Excel file
data.to_excel('smoothed_data.xlsx', index=False)
