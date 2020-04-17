# import os, re dan threading
import os
import re
import threading

# import time
import time

# buat kelas ip_check
class ip_check(threading.Thread):
    
    # fungsi __init__; init untuk assign IP dan hasil respons = -1
    def __init__ (self,ip):
        super().__init__()
        self.ip = ip
        self.hasil_respons = -1
    
    # fungsi utama yang diekseskusi ketika thread berjalan
    def run(self):
        # lakukan ping dengan perintah ping -n (gunakan os.popen())
        ping = os.popen('ping -n 2 '+ip)
        
        # loop forever
        while True:
            # baca hasil respon setiap baris
            line = ping.readline()
            
            # break jika tidak ada line lagi
            if not line: break
            
            # baca hasil per line dan temukan pola Received = x
            n_received = received.findall(line)

            # tampilkan hasilnya
            if n_received:
                self.hasil_respons = int(n_received[0])
                
    # fungsi untuk mengetahui status; 0 = tidak ada respon, 1 = hidup tapi ada loss, 2 = hidup
    def status(self):
        # 0 = tidak ada respon
        if self.hasil_respons == 0:
            return 'tidak ada respon'
        # 1 = ada loss
        elif self.hasil_respons == 1:
            return 'ada loss'
        # 2 = hidup
        elif self.hasil_respons == 2:
            return 'hidup'
        # -1 = seharusnya tidak terjadi
        else:
            return 'seharusnya tidak terjadi'
            
# buat regex untuk mengetahui isi dari r"Received = (\d)"
received = re.compile(r"Received = (\d)")

# catat waktu awal
start = time.time()

# buat list untuk menampung hasil pengecekan
check_results = []

# lakukan ping untuk 20 host
for suffix in range(0,20):
    # tentukan IP host apa saja yang akan di ping
    ip = '192.168.43.'+str(suffix)
    
    # panggil thread untuk setiap IP
    t = ip_check(ip)
    
    # masukkan setiap IP dalam list
    check_results.append(t)
    
    # jalankan thread
    t.start()
    

# untuk setiap IP yang ada di list
for el in check_results:
    
    # tunggu hingga thread selesai
    el.join()
    
    # dapatkan hasilnya   WAT???
    print((el.ip + ": " + el.status()))

# catat waktu berakhir
end = time.time()

# tampilkan selisih waktu akhir dan awal
print(end-start)
