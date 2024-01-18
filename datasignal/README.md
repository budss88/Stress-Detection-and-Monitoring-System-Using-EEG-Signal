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

-------------------------------------------------------------------------------
1. Hasil dari program Label.py akan ditambahkan kedalam file "most_common_stress_level.JSON" untuk ditampilkan di website
2. Hasil akurasi dari program Klasifikasi.py akan disimpan kedalam hasi_akurasi.txt
