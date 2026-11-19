# 🌴 Let's Learn English: Jungle Adventure 🦁

Aplikasi edukasi anak interaktif berbahasa Inggris bertema petualangan hutan tropis (*Jungle Adventure*) yang dirancang khusus untuk anak usia 4–8 tahun menggunakan bahasa pemrograman **Python** dan framework modern **Flet**. Dilengkapi fitur Text-to-Speech (TTS) otomatis untuk pelafalan kata bahasa Inggris yang fasih dan alami.

---

## ✨ Fitur Utama & 5 Layar (Screens)

### 1. 🚀 Login / Start Screen (Halaman Awal)
* **Nuansa Hutan Tropis Ceria**: Latar belakang gradasi hutan rimba dengan maskot hewan safari (🌴 🦁 🐒 🦒 🦜).
* **Judul Kartun Tebal**: *"LET'S LEARN ENGLISH! - JUNGLE ADVENTURE"*.
* **Tombol Utama "QUICK PLAY"**: Tombol hijau terang besar untuk langsung masuk belajar tanpa perlu login rumit.
* **Tombol "SELECT AVATAR"**: Menuju pemilihan karakter hewan safari.
* **Parent Gate (Pojok Kanan Atas)**: Tombol gembok kuning khusus orang tua dengan tantangan matematika acak (misal: `7 x 3 = ?`) untuk membuka pengaturan.
* **Toggle Suara (Pojok Kiri Atas)**: Tombol on/off suara dan musik.

### 2. 🐾 Select Avatar Screen (Pemilihan Karakter Anak)
* **6 Pilihan Kartu Avatar Hewan Lucu**:
  1. 🦁 **Leo the Lion** - *Brave Safari King!*
  2. 🦒 **Gigi the Giraffe** - *Curious Sky Scout!*
  3. 🐒 **Momo the Monkey** - *Fun Acrobat Buddy!*
  4. 🐘 **Ellie the Elephant** - *Wise & Gentle Giant!*
  5. 🐯 **Toby the Tiger** - *Speedy Jungle Runner!*
  6. 🐼 **Pip the Panda** - *Cuddly Bamboo Scout!*
* **Input Nama Panggilan**: Anak/orang tua dapat mengetik nama panggilan anak (default: `BUDI`).
* **Tombol "START ADVENTURE 🌟"**: Menyimpan profil aktif ke state aplikasi dan memutar salam suara ramah.

### 3. 🗺️ Main Menu / Dashboard Belajar
* **Header Profil**: Menampilkan avatar terpilih, nama anak, dan jumlah bintang emas (`⭐ 120`).
* **Grid 4 Kategori Belajar Utama**:
  * 🦁 **ANIMALS** (Singa, Monyet, Gajah, Jerapah, Harimau, Zebra, Kuda Nil, Burung Beo).
  * 🍎 **FRUITS** (Apel, Pisang, Jeruk, Stroberi, Semangka, Mangga, Nanas, Anggur).
  * 🔢 **NUMBERS** (Angka 1 sampai 10).
  * 🎨 **COLORS** (Merah, Biru, Kuning, Hijau, Oranye, Ungu, Merah Muda, Cokelat).
* **Panel Misi & Evaluasi**:
  * Tombol **"QUIZ TIME! 🎯"**: Membuka kuis petualangan.
  * Tombol **"DAILY QUESTS 📅"**: Modal misi harian (belajar kata, kuis, kumpulkan bintang) dengan progress bar dan klaim reward bonus bintang!
* **Bottom Navigation Bar**:
  * **"🏠 HOME"**: Kembali ke halaman awal.
  * **"🔊 SUARA ON/OFF"**: Toggle suara efek & TTS.
  * **"🏆 ACHIEVEMENTS"**: Ruang piala dan lencana petualang (6 lencana tantangan).

### 4. 📖 Tap-and-Learn Screen (Layar Materi Belajar Kosakata)
* Kartu-kartu kosakata interaktif dengan visual emoji besar, tulisan kapital tebal, terjemahan Indonesia, dan tombol speaker 🔊.
* **Efek Animasi & Suara**: Mengetuk kartu atau tombol speaker memicu efek animasi membesar (*scale-up* 1.08x) dan memutar pelafalan bahasa Inggris secara otomatis via TTS.
* Tombol cepat navigasi: *"BACK TO MENU"* dan *"KUIS SEKARANG"*.

### 5. 🎯 Quiz Time & Score Screen (Layar Kuis & Hasil)
* 5 soal interaktif dengan pertanyaan: *"What is this? 🤔"*, visual objek, dan tombol petunjuk suara.
* 4 pilihan jawaban tombol warna-warni (A, B, C, D).
* **Jawaban Benar**: Animasi checkmark, banner `AWESOME! +10 ⭐`, suara lonceng kemenangan (*arpeggio chime*), dan pujian TTS berbahasa Inggris.
* **Jawaban Salah**: Nada lembut dengan teks penyemangat agar anak berani mencoba lagi.
* **Layar Skor Akhir (Your Score)**:
  * Piala Emas 🏆, confetti bintang ⭐, rating bintang (⭐⭐⭐), total bintang profil, tombol *"PLAY AGAIN"* dan *"HOME"*.

---

## 🔒 Parent Gate & Settings
Untuk memastikan anak tetap berada di dalam lingkungan bermain yang aman, area orang tua dilindungi dengan soal perkalian acak. Menu orang tua menyediakan:
* Statistik belajar anak (Total Bintang ⭐, Kata Dipelajari 📚, Kuis Diselesaikan 🎯).
* Slider pengaturan kecepatan suara pelafalan TTS (100 WPM s/d 200 WPM).
* Tombol reset progress belajar anak (kembali ke 0).

---

## 📁 Struktur Proyek (Modular)

```text
apk belajar bahasa inggris anak anak/
│
├── main.py                     # Entry point aplikasi Flet & Router navigasi
├── requirements.txt            # Daftar pustaka dependensi
├── run_app.bat                 # Shortcut launcher Windows (Double-click to run)
├── README.md                   # Dokumentasi lengkap aplikasi
│
├── app/
│   ├── __init__.py
│   ├── state.py                # State management aplikasi (profil, bintang, quest, suara)
│   ├── audio_manager.py        # Background thread queue untuk TTS (pyttsx3) & audio effects
│   ├── theme.py                # Design system jungle (warna cerah, border radius, bayangan, tombol)
│   ├── dialogs.py              # Modal Parent Gate, Settings, Daily Quests, & Achievements
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── avatars.py          # Data 6 karakter avatar hewan safari
│   │   ├── vocabulary.py       # Data kosakata 4 kategori (Animals, Fruits, Numbers, Colors)
│   │   └── quests.py           # Definisi target misi harian & 6 lencana prestasi
│   │
│   └── screens/
│       ├── __init__.py
│       ├── start_screen.py     # Layar 1: Halaman Awal & Parent Login
│       ├── avatar_screen.py    # Layar 2: Pemilihan Karakter & Nama Anak
│       ├── dashboard_screen.py # Layar 3: Dashboard Grid Kategori & Misi
│       ├── learn_screen.py     # Layar 4: Tap-and-Learn Card & Pelafalan TTS
│       └── quiz_screen.py      # Layar 5: Kuis Interaktif & Layar Skor
└── venv/                       # Virtual environment Python (flet, pyttsx3, gTTS, pywin32)
```

---

## 🚀 Cara Menjalankan Aplikasi

### Metode 1: Buka di Layar Desktop (Laptop / PC)
Cukup **klik ganda (double-click)** pada berkas:
```text
run_app.bat
```
*(atau jalankan `.\venv\Scripts\python.exe main.py` di PowerShell)*

### Metode 2: Buka di HP / Tablet (Android & iOS via Wi-Fi)
1. **Klik ganda berkas**:
   ```text
   run_for_hp.bat
   ```
2. Pastikan HP dan Laptop terhubung ke Wi-Fi yang sama.
3. Buka browser di HP (Chrome / Safari) lalu ketik:
   ```text
   http://192.168.1.20:8550
   ```
4. Suara pelafalan bahasa Inggris langsung terdengar melalui speaker HP menggunakan Web Speech API, dan tampilan otomatis responsif penuh 100% tanpa terpotong!
