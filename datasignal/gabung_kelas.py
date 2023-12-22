import pandas as pd
import os

# Folder sumber data
directory_path = 'Data/Label'

# Mengambil file CSV paling terbaru
latest_csv_file = max([file for file in os.listdir(directory_path) if file.endswith('.csv')], key=lambda x: os.path.getctime(os.path.join(directory_path, x)))

# Membaca data CSV
new_data = pd.read_csv(os.path.join(directory_path, latest_csv_file))

# Folder data training
training_directory = 'Data/Kelas/Train'
training_file = 'Dataset_Train.csv'

# Membaca data training yang sudah ada
existing_training_file = os.path.join(training_directory, training_file)
if os.path.exists(existing_training_file):
    existing_data = pd.read_csv(existing_training_file)
else:
    existing_data = pd.DataFrame(columns=['MAP Alpha Low', 'MAP Alpha High', 'MAP Beta Low', 'MAP Beta High', 'Stres Level'])

# Menambahkan data baru ke data training
updated_data = pd.concat([existing_data, new_data], ignore_index=True)

# Simpan file CSV yang baru ke dalam folder kelas
if not os.path.exists(training_directory):
    os.makedirs(training_directory)

updated_file_path = os.path.join(training_directory, training_file)
updated_data.to_csv(updated_file_path, index=False)

print(f"File {latest_csv_file} berhasil ditambahkan ke dalam {updated_file_path}.")
