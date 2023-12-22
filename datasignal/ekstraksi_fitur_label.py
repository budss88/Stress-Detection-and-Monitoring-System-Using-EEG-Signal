import pandas as pd
import numpy as np
from scipy.signal import firwin, lfilter, stft
import glob, os, time

start_time = time.time()

# Menentukan frequency bands
alpha_low_band = [8, 10]
alpha_high_band = [11, 12]
beta_low_band = [13, 22]
beta_high_band = [23, 30]

# Mengambil file CSV paling terbaru dalam folder dengan keterangan "*_Filtering (sub-band).csv"
folder_path = 'Data/Filter'

# Direktori tujuan (folder "Data/Ekstraksi" di luar direktori sumber)
destination_directory = os.path.join('Data', 'Ekstraksi')

# Pastikan direktori tujuan ("Data/Ekstraksi") sudah ada atau buat jika belum ada
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)
# Fungsi normalisasi dengan parameter agar nilai mendekati data asli
def normalize_signal(signal, original_mean, original_std, scale_factor=0.5):
    normalized_signal = scale_factor * (signal - np.mean(signal)) / np.std(signal)
    # Mengembalikan nilai yang mendekati data asli
    normalized_signal = normalized_signal * original_std + original_mean
    return normalized_signal

# Mendapatkan file CSV paling terbaru dalam folder
latest_csv_file = max(glob.glob(os.path.join(folder_path, '*_Filtering (sub-band).csv')), key=os.path.getctime)

# Baca file CSV ke pandas dataframe
df = pd.read_csv(latest_csv_file)

# Membuat sinyal EEG dari dataframe
ch_names = ['TP9', 'AF7', 'AF8', 'TP10']
data = df[ch_names].values.T

alpha_low_signal = alpha_low_band
alpha_high_signal = alpha_high_band
beta_low_signal = beta_low_band
beta_high_signal = beta_high_band

# Normalisasi sinyal dengan parameter agar nilai mendekati data asli
alpha_low_signal = normalize_signal(alpha_low_signal, np.mean(data[0]), np.std(data[0]))
alpha_high_signal = normalize_signal(alpha_high_signal, np.mean(data[1]), np.std(data[1]))
beta_low_signal = normalize_signal(beta_low_signal, np.mean(data[2]), np.std(data[2]))
beta_high_signal = normalize_signal(beta_high_signal, np.mean(data[3]), np.std(data[3]))

# Menambahkan kolom alpha low, alpha high, beta low, dan beta high ke dataframe
df['MAP Alpha Low'] = np.mean(np.abs(alpha_low_signal)**2)
df['MAP Alpha High'] = np.mean(np.abs(alpha_high_signal)**2)
df['MAP Beta Low'] = np.mean(np.abs(beta_low_signal)**2)
df['MAP Beta High'] = np.mean(np.abs(beta_high_signal)**2)

# Memeriksa keberadaan kolom-kolom yang akan dihapus sebelum mencoba untuk menghapusnya
columns_to_drop = ['timestamps', 'TP9', 'AF7', 'AF8', 'TP10', 'Right AUX', 'MAP Alpha Low Result', 'MAP Alpha High Result', 'MAP Beta Low Result', 'MAP Beta High Result']
existing_columns = set(df.columns)
columns_to_drop = [col for col in columns_to_drop if col in existing_columns]

# Menghapus kolom-kolom yang tidak diinginkan
df = df.drop(columns=columns_to_drop, errors='ignore')

# Menambahkan kolom baru pada data frame untuk label tingkat stres berdasarkan kombinasi dari sinyal alpha dan beta
df['Stres Level'] = np.where((df['MAP Alpha Low'] > df['MAP Alpha High']) & (df['MAP Beta Low'] > df['MAP Beta High']), 'Normal',
                             np.where((df['MAP Alpha Low'] < df['MAP Alpha High']) & (df['MAP Beta Low'] > df['MAP Beta High']), 'Stres Ringan',
                                      np.where((df['MAP Alpha Low'] > df['MAP Alpha High']) & (df['MAP Beta Low'] < df['MAP Beta High']), 'Stres Sedang',
                                               np.where((df['MAP Alpha Low'] < df['MAP Alpha High']) & (df['MAP Beta Low'] < df['MAP Beta High']), 'Stres Berat', 'Tidak Diketahui'))))

# Menyimpan hanya satu baris dari setiap kolom 'MAP Alpha Low', 'MAP Alpha High', 'MAP Beta Low', dan 'MAP Beta High' ke dalam file CSV
output_df = df[['MAP Alpha Low', 'MAP Alpha High', 'MAP Beta Low', 'MAP Beta High', 'Stres Level']].head(1)
new_file = os.path.join(destination_directory, os.path.basename(latest_csv_file).replace('.csv', '_AB.csv'))
output_df.to_csv(new_file, index=False)

print(f'Data dari file {latest_csv_file} berhasil diproses')

end_time = time.time()
computation_time = end_time - start_time
print(f'Waktu proses: {computation_time:.2f} detik')
