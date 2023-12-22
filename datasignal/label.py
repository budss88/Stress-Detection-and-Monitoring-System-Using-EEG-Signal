import pandas as pd
import os, json

# Menentukan folder sumber dan folder tujuan
folder_path = 'Data/Ekstraksi'
destination_directory = os.path.join('Data', 'Label')

# Menentukan direktori tujuan, akan dibuat jika belum ada
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Daftar nama kolom yang ingin disimpan
columns_to_keep = ['MAP Alpha Low', 'MAP Alpha High', 'MAP Beta Low', 'MAP Beta High', 'Stres Level']

# Mengambil daftar semua file CSV di folder dengan keterangan "*_AB.csv"
csv_files = [file for file in os.listdir(folder_path) if file.endswith('_AB.csv')]

# Mengambil file CSV paling terbaru
latest_csv_file = max(csv_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))

# Baca file CSV ke pandas DataFrame
df = pd.read_csv(os.path.join(folder_path, latest_csv_file))

# Menghilangkan kolom yang tidak diperlukan
df = df[columns_to_keep]

# Menghilangkan keterangan "_AB" dari nama file
new_file_name = latest_csv_file.replace('_Filtering (Sub-band)_AB', '')

# Menghitung jumlah kemunculan setiap nilai dalam kolom 'Stress Level'
stress_level_counts = df['Stres Level'].value_counts().to_dict()
print(f'{dict(stress_level_counts)}')

# Simpan nilai stress_level_counts ke dalam file JSON
with open('most_common_stress_level.json', 'w') as json_file:
    most_common_stress_level = max(stress_level_counts, key=stress_level_counts.get)
    json.dump({"most_common_stress_level": most_common_stress_level}, json_file)

# Simpan DataFrame yang sudah diproses ke dalam file CSV baru di folder tujuan
output_file = os.path.join(destination_directory, new_file_name)
df.to_csv(output_file, index=False)
