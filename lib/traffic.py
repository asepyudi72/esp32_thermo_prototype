import machine
import time

# Sesuaikan dengan pin Anda (4, 16, 17)
merah = machine.Pin(2, machine.Pin.OUT)

def jalankan_loop():
    print("Sistem Traffic Light Aktif...")
    while True:
        # Merah
        merah.value(1)
        time.sleep(1)
