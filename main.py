import network
import urequests
import os
import machine
import time

# --- KONFIGURASI ---
SSID = "NAZLA_plus"
PASSWORD = "BH5H5G8TGGN"
# Ganti dengan URL server lokal atau link mentah (Raw) dari GitHub Anda
#https://github.com/asepyudi72/
#https://github.com/asepyudi72/esp32_thermo_prototype
#20.205.243.166
URL_VERSI = "http://192.168.1"
URL_MAIN = "http://192.168.1"

VERSI_SEKARANG = "1.0.0" # Versi yang terinstal di ESP32 saat ini

def hubungkan_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Terhubung! IP:", wlan.ifconfig()[0])

def cek_dan_update_ota():
    print("Mengecek pembaruan...")
    try:
        # 1. Ambil info versi terbaru dari server
        respon_versi = urequests.get(URL_VERSI)
        versi_terbaru = respon_versi.text.strip()
        respon_versi.close()
        
        print(f"Versi ESP32: {VERSI_SEKARANG} | Versi Server: {versi_terbaru}")
        
        if versi_terbaru != VERSI_SEKARANG:
            print("Versi baru ditemukan! Memulai unduhan...")
            
            # 2. Unduh isi main.py yang baru
            respon_main = urequests.get(URL_MAIN)
            kode_baru = respon_main.text
            respon_main.close()
            
            # 3. Simpan dan timpa file main.py lama di storage ESP32
            with open("main.py", "w") as f:
                f.write(kode_baru)
                
            print("Update sukses! Me-restart ESP32...")
            time.sleep(1)
            machine.reset() # Reboot agar program baru langsung berjalan
        else:
            print("Firmware sudah yang terbaru.")
            
    except Exception as e:
        print("Gagal mengecek OTA:", e)

# --- ALUR UTAMA ---
hubungkan_wifi()
cek_dan_update_ota()

# --- MASUKKAN PROGRAM UTAMA ANDA DI SINI ---
print("Program Utama Berjalan...")
led = machine.Pin(2, machine.Pin.OUT)
while True:
    led.value(not led.value())
    time.sleep(0.5) # Blink normal
