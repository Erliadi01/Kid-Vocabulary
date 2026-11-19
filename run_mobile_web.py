import os
os.environ["FLET_WEB_MODE"] = "1"
os.environ["FLET_FORCE_WEB_SERVER"] = "1"

import socket
import flet as ft
from main import main

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.20"

if __name__ == "__main__":
    ip = get_local_ip()
    port = 8550
    print("=" * 60)
    print("  LET'S LEARN ENGLISH: JUNGLE ADVENTURE 🌴🦁")
    print("  MOBILE WEB SERVER UNTUK HP (ANDROID & IOS)")
    print("=" * 60)
    print(f"\n👉 Langkah Membuka di HP:")
    print(f"   1. Pastikan HP dan Laptop terhubung ke Wi-Fi yang sama.")
    print(f"   2. Buka aplikasi browser di HP (Chrome / Safari).")
    print(f"   3. Ketik alamat URL berikut:")
    print(f"      http://{ip}:{port}\n")
    print("=" * 60)
    print("Server siap melayani audio & tampilan HP...")
    print("Server sedang berjalan... (Tekan Ctrl+C untuk berhenti)\n")

    # Jalankan server web FastAPI/Flet dengan aset audio agar bisa diakses oleh HP di jaringan Wi-Fi lokal
    ft.run(main, host="0.0.0.0", port=port, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
