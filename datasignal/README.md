Seluruh program terintegrasi agar dapat berjalan bersamaan secara sekuensial menggunakan multithread. Bahasa yang digunakan adalah C++ untuk program ESP32-Cam, JavaScript untuk program server menggunakan NodeJS, HTML & CSS untuk tampilan website, dan Python untuk pemrosesan data.

Pada Rasberry Pi 3:
1. (App.py) Digunakan untuk menjalankan seluruh program python yang telah disusun, mulai dari tahap perekaman, pengelohan data sampai menampilkan output.
2. (Preprocessing.py) Digunakan untuk mengolah data EEG yang sudah direkam sebelumnya, dimana pada proses ini terdapat proses filtering berupa bandpass filter dan ICA.
3. (EkstraksiFitur.py) Digunakan untuk mengekstrak sinyal berupa alpha dan beta dari sinyal EEG. Disini juga dilakukan proses normalisasi dan perhitungan Mean Absolute Power pada gelombang alpha dan beta. Selain itu dilakukan pelabelan kelas berdasarkan kombinasi gelombang alpha dan beta untuk menentukan kelas tingkat stres.
4. (Label.py) Digunakan untuk mengambil label kelas dari file csv hasil program sebelumnya
5. (GabungKelas.py) Digunakan untuk menambahkan data hasil kelas kedalam dataset untuk selanjutnya diklasifikasikan
6. (Klasifikasi.py) Digunakan untuk mengklasifikasikan hasil berupa perbandingan menggunakan KNN antara data training dan data testing untuk mendapatkan tingkat akurasi pada pengujian
7. (User.html) Digunakan untuk tampilan website
8. (Server.js) Digunakan untuk server lokal yang menyediakan koneksi http lokal dan koneksi websocket
9. (Styles.css) Digunakan untuk tampilan website

==============================================================================================================================================================

1. Hasil dari program Label.py akan ditambahkan kedalam file "most_common_stress_level.JSON" untuk ditampilkan di website
2. Hasil akurasi dari program Klasifikasi.py akan disimpan kedalam hasi_akurasi.txt

==============================================================================================================================================================

1. Akuisisi Data EEG Muse Headband:
- Memerlukan instalasi library muselsl pada sistem atau tempat akuisisi dan pengolahan data
- Memerlukan koneksi bluetooth (Otomatis ketika masing-masing bluetooth pada device sudah dinyalakan)
- Menggunakan bahasa pemrograman Python

2. Akuisisi Data Gambar ESP32-Cam:
- Tidak memerlukan instalasi apapun, hanya konfigurasi resolusi gambar yang optimal, koneksi wifi dan websocket
- Menggunakan bahasa pemrograman C++

3. Website:
- Memerlukan instalasi NVM dan Node.Js untuk membuat dan menjalankan servernya
- Menggunakan HTML/CSS dan bahasa pemrograman Javascript untuk membuat tampilan websitenya
- Untuk menjalankan servernya menggunakan command node pada file js yang menjadi server

4. Pengolahan Data:
Memerlukan Library:
- Pandas
- Numpy
- Matplotlib
- Sklearn dan Scipy
- Popen dan PIPE

Untuk Setting PATH dan folder dataset tinggal menyesuaikan dengan kodingan yang ada
