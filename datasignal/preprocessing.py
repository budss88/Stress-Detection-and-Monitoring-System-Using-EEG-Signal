import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, glob, time
from scipy.signal import firwin, filtfilt
from sklearn.decomposition import FastICA

start_time = time.time()

# Fungsi Filter Artefak ICA
def ica_filter(signal, n_components):
    ica = FastICA(n_components=n_components)
    ica_signal = ica.fit_transform(signal.reshape(-1, 1))
    return ica_signal.flatten()

# Fungsi Filter Bandpass
def bandpass_filter(signal, fs, lowcut, highcut, order=1001):
    nyquist = 0.5 * fs
    if lowcut < 0 or highcut > nyquist:
        raise ValueError("Invalid cutoff frequency: frequencies must be greater than 0 and less than fs/2")
    low = lowcut / nyquist
    high = highcut / nyquist
    taps = firwin(order, [low, high], pass_zero=False)
    filtered_signal = filtfilt(taps, 1.0, signal)
    return filtered_signal

def create_bandpass_filters(fs):
    bands = {'Delta': (0.5, 4.0), 'Theta': (4.0, 8.0), 'Alpha': (8.0, 13.0), 'Beta': (13.0, 30.0), 'Gamma': (30.0, 100.0)}

    filters = {}
    for band, (lowcut, highcut) in bands.items():
        filters[band] = firwin(1001, [lowcut / (0.5 * fs), highcut / (0.5 * fs)], pass_zero=False)
    return filters

def get_latest_csv_file(folder_path):
    list_of_files = glob.glob(os.path.join(folder_path, '*.csv'))
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def preprocess_eeg_data(csv_file, lowcut, highcut, ica_components=1):
    # Mengambil data CSV
    df = pd.read_csv(csv_file)

    # Ekstrak kolom sinyal EEG
    eeg_data = df[['TP9', 'AF7', 'AF8', 'TP10']].values
    
    # Buat filter bandpass untuk sub-band yang berbeda
    bandpass_filters = create_bandpass_filters(fs)

    # Ekstrak sinyal EEG menjadi sub-band
    preprocessed_data = np.zeros_like(eeg_data)  # Inisialisasi array preprocessed_data
    for i, (sub_band, filter_coefficients) in enumerate(bandpass_filters.items()):
        for j in range(eeg_data.shape[1]):
            signal = eeg_data[:, j]
            preprocessed_signal = filtfilt(filter_coefficients, 1.0, signal)
            if ica_components > 0:
                ica_signal = ica_filter(preprocessed_signal, ica_components)
                preprocessed_data[:, j] += ica_signal
            else:
                preprocessed_data[:, j] += preprocessed_signal

    # Rata-rata hasil preprocessed_data
    preprocessed_data /= len(bandpass_filters)

    # Replace kolom sinyal EEG asli dengan preproses data
    df[['TP9', 'AF7', 'AF8', 'TP10']] = preprocessed_data

    # Menyimpan data preprocessed data ke file CSV yang baru
    preprocessed_csv_file = os.path.join('Data', 'Filter', os.path.basename(csv_file).replace('.csv', '_Filtering (Sub-band).csv'))
    df.to_csv(preprocessed_csv_file, index=False)

    # Menampilkan plot data asli dan sinyal preprosesing (opsional, bisa dinonaktifkan)
    fig, axs = plt.subplots(4, 2, figsize=(10, 10))
    fig.suptitle('Perbandingan Data')
    for i in range(eeg_data.shape[1]):
        axs[i, 0].plot(eeg_data[:, i])
        axs[i, 0].set_title(f'Data Asli {df.columns[i+1]}')
        axs[i, 1].plot(preprocessed_data[:, i])
        axs[i, 1].set_title(f'Data Proses Filter {df.columns[i+1]}')
    
    # Simpan grafik sebagai file
    save_folder = os.path.join('Data', 'Plot grafik')
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    fig_name = os.path.join(save_folder, f'{os.path.basename(csv_file).replace(".csv", "")}_Filtering (sub-band).png')
    plt.savefig(fig_name)
    plt.close()

# Dataset
# Mengambil semua file CSV dalam folder 'data'
folder_path = 'Data'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
fs = 256.0  # Frekuensi sampling
ica_components = 1
lowcut = 8.0  # Lower cutoff frekuensi gelombang alpha
highcut = 30.0  # Upper cutoff frekuensi gelombang beta

for i, csv_file in enumerate(csv_files):
    preprocess_eeg_data(csv_file, lowcut, highcut)
    print(f'Proses ke {i+1} dari {len(csv_files)} file')
# Dapatkan file CSV terbaru
''' latest_csv_file = get_latest_csv_file(folder_path) '''

# Proses hanya file CSV terbaru
''' preprocess_eeg_data(latest_csv_file, lowcut, highcut) '''

print(f'Data berhasil diproses')

end_time = time.time()
computation_time = end_time - start_time
print(f'Waktu proses: {computation_time:.2f} detik')
