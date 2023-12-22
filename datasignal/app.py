from subprocess import Popen, PIPE
import os, time, json, threading

class EEGProcessing:
    def __init__(self):
        self.stream_process = None

    def connect_muse(self):
        while True:
            # Memulai proses muselsl stream
            self.stream_process = Popen(["muselsl", "stream"], stdout=PIPE, stderr=PIPE)
            # Menunggu 20 detik sebelum menjalankan rekaman
            time.sleep(20)
            # Menjalankan rekaman setelah 20 detik
            self.record_data()

    def record_data(self):
        save_path = "C:\\Users\\Budhi Afrianto\\Downloads\\Skripsi\\Sistem\\Program\\NodeServer\\datasignal\\Data"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        output_filename = "*.csv"
        current_directory = os.getcwd()

        try:
            os.chdir(save_path)
            command = ["muselsl", "record", "--duration", "60"]
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            process.communicate()
            time.sleep(2)
            recorded_file = os.path.join(current_directory, "*.csv")

            if os.path.exists(recorded_file):
                destination_file = os.path.join(save_path, output_filename)
                os.rename(recorded_file, destination_file)
            else:
                print(f"Error: Recorded file not found at {recorded_file}")
        finally:
            os.chdir(current_directory)

        # Setelah rekaman selesai, jalankan semua program lainnya
        self.run_all_programs()

        # Menunggu sebelum mengulang
        time.sleep(10)  # Ganti nilai ini sesuai kebutuhan, misalnya 10 detik

    def run_all_programs(self):
        self.run_processing()
        self.run_feature_extraction()
        self.run_labeling()
        self.combine_classes()
        self.run_classification()
        self.update_results()

    def run_processing(self):
        os.system("python preprocessing.py")

    def run_feature_extraction(self):
        os.system("python ekstraksi_fitur_label.py")

    def run_labeling(self):
        os.system("python label.py")

    def combine_classes(self):
        os.system("python gabung_kelas.py")

    def run_classification(self):
        os.system("python klasifikasi.py")

    def update_results(self):
        with open('most_common_stress_level.json', 'r') as json_file:
            data = json.load(json_file)
            stress_level = data.get('most_common_stress_level', 'Not available')
            print(f"Tingkat Stres: {stress_level}")

        with open('hasil_akurasi.txt', 'r') as accuracy_file:
            accuracy_result = accuracy_file.read()
            print(f"Tingkat Akurasi: {accuracy_result} %")

if __name__ == "__main__":
    eeg_processing = EEGProcessing()
    eeg_processing.connect_muse()
