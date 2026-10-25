import machine
import time

# Sesuaikan dengan pin Anda (4, 16, 17)
merah = machine.Pin(4, machine.Pin.OUT)
kuning = machine.Pin(16, machine.Pin.OUT)
hijau = machine.Pin(17, machine.Pin.OUT)

def jalankan_loop():
    print("Sistem Traffic Light Aktif...")
    while True:
        # Merah
        merah.value(1); kuning.value(0); hijau.value(0)
        time.sleep(3)
        # Hijau
        merah.value(0); kuning.value(0); hijau.value(1)
        time.sleep(3)
        # Kuning
        merah.value(0); kuning.value(1); hijau.value(0)
        time.sleep(1)
