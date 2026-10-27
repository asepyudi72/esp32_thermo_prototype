import network
import urequests
import os
import machine
import time

#URL_BASE = "https://githubusercontent.com"
URL_BASE ="https://github.com/asepyudi72/esp32_thermo_prototype/blob/main/"

DAFTAR_FILE = [
    "main.py",
    "version.txt",
    "lib/ota_updater.py",
    "lib/traffic.py"
]

def ambil_kredensial_wifi():
    try:
        with open("wifi_config.txt", "r") as f:
            baris = f.readlines()
            return baris[0].strip(), baris[1].strip()
    except:
        print("Gagal membaca wifi_config.txt!")
        return None, None

def hubungkan_wifi():
    ssid, password = ambil_kredensial_wifi()
    if not ssid: return False
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Menghubungkan ke Wi-Fi: {ssid}...")
        wlan.connect(ssid, password)
        timeout = 0
        while not wlan.isconnected() and timeout < 30:
            time.sleep(0.5)
            timeout += 1
    return wlan.isconnected()

def ambil_versi_lokal():
    try:
        with open("version.txt", "r") as f: return f.read().strip()
    except OSError: return "0.0.0"

def hapus_file_jika_ada(path_file):
    try: os.remove(path_file)
    except OSError: pass

def periksa_dan_update():
    versi_lokal = ambil_versi_lokal()
    print(f"Versi Lokal: {versi_lokal}")
    try:
        respon = urequests.get(URL_BASE + "version.txt")
        versi_terbaru = respon.text.strip()
        respon.close()
        
        if versi_terbaru != versi_lokal:
            print("Ada update baru! Mengunduh...")
            for file in DAFTAR_FILE:
                # Membuat folder lib/ otomatis jika mengunduh file di dalam lib
                if "/" in file:
                    try: os.mkdir(file.rsplit("/", 1)[0])
                    except OSError: pass
                    
                res_file = urequests.get(URL_BASE + file)
                konten = res_file.text
                res_file.close()
                with open(file + ".tmp", "w") as f: f.write(konten)
                
            for file in DAFTAR_FILE:
                hapus_file_jika_ada(file)
                os.rename(file + ".tmp", file)
            print("Sukses! Restart...")
            time.sleep(1)
            machine.reset()
        else:
            print("Sudah versi terbaru.")
    except Exception as e:
        print("OTA Gagal:", e)
        for file in DAFTAR_FILE: hapus_file_jika_ada(file + ".tmp")
