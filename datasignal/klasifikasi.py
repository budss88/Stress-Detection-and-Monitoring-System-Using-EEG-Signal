import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold

# Input Dataset
dataset = pd.read_csv('Data/Kelas/Train/Dataset_Train.csv')
dataset.head()
x = dataset.iloc[:, [0, 3]].values
y = dataset.iloc[:, -1].values

# Membagi Dataset ke Data Training dan Data Testing
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=100)

# Scaling Data
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Handling Class Imbalance with Oversampling
oversampler = RandomOverSampler(sampling_strategy='auto', random_state=100)
x_train_resampled, y_train_resampled = oversampler.fit_resample(x_train, y_train)

# Hyperparameter Tuning
param_grid = {'n_neighbors': [1, 3, 5, 7, 9, 11], 'weights': ['uniform', 'distance'], 'metric': ['euclidean', 'manhattan']}
grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)
grid_search.fit(x_train_resampled, y_train_resampled)
print("Parameter Terbaik:", grid_search.best_params_)

# Menentukan Prediksi
y_pred = grid_search.predict(x_test)

# Evaluasi dan Validasi
cm = confusion_matrix(y_test, y_pred)

akurasi = classification_report(y_test, y_pred, zero_division=1)
print(akurasi)

scores = cross_val_score(grid_search.best_estimator_, x_train, y_train, cv=StratifiedKFold(n_splits=5), scoring='accuracy')
print("Akurasi Cross-Validation: %.2f Persen" % (np.mean(scores) * 100))

# Calculate accuracy
akurasi_test_score = accuracy_score(y_test, y_pred)
print("Tingkat Akurasi pada Data Testing: %.2f Persen" % (akurasi_test_score * 100))

# Write accuracy to file
with open('hasil_akurasi.txt', 'w') as accuracy_file:
    accuracy_file.write(f"{akurasi_test_score * 100:.2f}")

''' # Hapus seluruh file dalam folder Data/Ekstraksi
ekstraksi_path = 'Data/Ekstraksi'
for file in os.listdir(ekstraksi_path):
    file_path = os.path.join(ekstraksi_path, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f'Gagal menghapus {file_path}: {e}')

# Hapus seluruh file dalam folder Data/Filter
filter_path = 'Data/Filter'
for file in os.listdir(filter_path):
    file_path = os.path.join(filter_path, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f'Gagal menghapus {file_path}: {e}')

# Hapus seluruh file dalam folder Data/Label
label_path = 'Data/Label'
for file in os.listdir(label_path):
    file_path = os.path.join(label_path, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f'Gagal menghapus {file_path}: {e}') '''