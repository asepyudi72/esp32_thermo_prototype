import network
import urequests
import os
import machine
import time

# ==========================================
# PENGATURAN UTAMA
# ==========================================
# Salin URL RAW dari GitHub Anda (Wajib diakhiri tanda / )
URL_BASE = "https://raw.githubusercontent.com/asepyudi72/esp32_thermo_prototype/refs/heads/main/"

# Daftar file yang di-download dari GitHub (wifi_config.txt TIDAK dimasukkan di sini!)
DAFTAR_FILE = [
    "main.py",
    "version.txt"
]

def ambil_kredensial_wifi():
    # Membaca SSID dan Password dari file lokal wifi_config.txt
    try:
        with open("wifi_config.txt", "r") as f:
            baris = f.readlines()
            ssid = baris[0].strip()
            password = baris[1].strip()
            return ssid, password
    except Exception as e:
        print("Gagal membaca wifi_config.txt! Pastikan file sudah dibuat di ESP32.")
        return None, None

def hubungkan_wifi():
    ssid, password = ambil_kredensial_wifi()
    if not ssid:
        return False
        
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Menghubungkan ke Wi-Fi: {ssid}...")
        wlan.connect(ssid, password)
        timeout = 0
        while not wlan.isconnected() and timeout < 30:
            time.sleep(0.5)
            timeout += 1
            
    if wlan.isconnected():
        print("Wi-Fi Terhubung! IP:", wlan.ifconfig())
        return True
    else:
        print("Gagal terhubung ke Wi-Fi. Periksa SSID/Password di wifi_config.txt")
        return False

def ambil_versi_lokal():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except OSError:
        return "0.0.0"

def hapus_file_jika_ada(path_file):
    try:
        os.remove(path_file)
    except OSError:
        pass

def lakukan_ota():
    versi_lokal = ambil_versi_lokal()
    print(f"Versi Lokal ESP32: {versi_lokal}")
    print("Memeriksa pembaruan di GitHub...")
    
    try:
        respon = urequests.get(URL_BASE + "version.txt")
        versi_terbaru = respon.text.strip()
        respon.close()
        
        print(f"Versi di GitHub: {versi_terbaru}")
        
        if versi_terbaru != versi_lokal:
            print("Versi baru ditemukan! Memulai proses unduhan...")
            
            # Download file proyek ke format sementara (.tmp)
            for file in DAFTAR_FILE:
                url_download = URL_BASE + file
                file_tmp = file + ".tmp"
                
                print(f"Mengunduh {file}...")
                res_file = urequests.get(url_download)
                konten = res_file.text
                res_file.close()
                
                with open(file_tmp, "w") as f:
                    f.write(konten)
            
            # Jika sukses semua, timpa file asli
            print("Menerapkan pembaruan...")
            for file in DAFTAR_FILE:
                file_tmp = file + ".tmp"
                hapus_file_jika_ada(file)
                os.rename(file_tmp, file)
                
            print("Update sukses total! Sistem merestart...")
            time.sleep(1)
            machine.reset()
        else:
            print("Sistem sudah menggunakan versi terbaru.")
            
    except Exception as e:
        print("Proses OTA Gagal:", e)
        for file in DAFTAR_FILE:
            hapus_file_jika_ada(file + ".tmp")

# ==========================================
# ALUR JALANNYA PROGRAM
# ==========================================
if hubungkan_wifi():
    lakukan_ota()

# --- PROGRAM UTAMA ANDA DI SINI ---
print("Menjalankan aplikasi utama...")
led = machine.Pin(2, machine.Pin.OUT)
while True:
    led.value(not led.value())
    time.sleep(1)

