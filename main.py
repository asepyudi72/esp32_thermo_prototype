import gc
import lib/ota_updater as ota
import lib/traffic as traffic
#test gc for RAM saving
# 1. Jalankan pengecekan OTA dari library ota_updater
if ota.hubungkan_wifi():
    ota.periksa_dan_update()

# 2. Bersihkan RAM dari sisa proses unduhan HTTP/WiFi
gc.collect()

# 3. Jalankan aplikasi utama dari library traffic
traffic.jalankan_loop()

