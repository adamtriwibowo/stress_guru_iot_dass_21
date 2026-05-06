# 🚀 QUICK START GUIDE

## Sistem Informasi IoT - Uji Stress Guru Autis (DASS-21)

---

## 📦 INSTALASI (Sekali Saja)

### 1. Install Dependencies
Buka Command Prompt di folder project:
```bash
cd "D:\DATA MASTER\S2 ADAM\adamtriwibowo\ROADMAP\Internet Of Things\final_project"
pip install -r requirements.txt
```

---

## ▶️ CARA MENJALANKAN SISTEM

### 1. Start Server
```bash
python app.py
```

Server akan berjalan di: **http://localhost:5000**

### 2. Buka di Browser
Akses alamat: **http://localhost:5000**

---

## 🎯 CARA MENGGUNAKAN SISTEM

### **Opsi 1: Mulai Test Stress**
1. Klik tombol **"Mulai Test"** atau akses **http://localhost:5000/test**
2. **Step 1 - Data Diri:**
   - Isi kode responden (auto-generate: Rxxx)
   - Nama, usia, jenis kelamin, pengalaman mengajar
   - Klik "Lanjutkan"

3. **Step 2 - Data Sensor IoT:**
   - Masukkan data detak jantung (2x pengujian)
   - Masukkan data suhu tubuh (2x pengujian)
   - Klik "Lanjutkan"
   - *Note: Bisa dikosongkan jika tidak ada sensor*

4. **Step 3 - Kuesioner DASS-21:**
   - Jawab 7 pertanyaan stress
   - Pilih skala 0-3 untuk setiap pertanyaan:
     - 0 = Tidak Pernah
     - 1 = Kadang-kadang
     - 2 = Sering
     - 3 = Hampir Selalu
   - Progress bar akan menunjukkan progress
   - Klik "Submit Test" setelah semua terjawab

5. **Step 4 - Hasil Test:**
   - Sistem akan menampilkan:
     - Skor DASS-21 (angka besar)
     - Level stress (Normal/Mild/Moderate/Severe)
     - Deskripsi kondisi
     - Detail skor mentah dan kategori
   - Warna hasil sesuai level stress:
     - 🟢 Hijau = Normal
     - 🟡 Kuning = Mild
     - 🟠 Orange = Moderate
     - 🔴 Merah = Severe

### **Opsi 2: Lihat Dashboard**
1. Klik tombol **"Dashboard"** atau akses **http://localhost:5000/dashboard**
2. Dashboard menampilkan:
   - 📊 Statistik: Total responden, test, rata-rata skor
   - 📈 Grafik distribusi stress (bar chart)
   - 🥧 Presentase kategori (pie chart)
   - 📉 Distribusi skor (line chart)
   - 📋 Tabel lengkap semua hasil test

---

## 📊 CONTOH PENGGUNAAN

### Test Responden Baru:
```
Step 1:
- Kode: R55
- Nama: Siti Aminah
- Usia: 35
- Jenis Kelamin: Perempuan
- Pengalaman: 10 tahun

Step 2:
- Detak Jantung Test 1: 120 BPM
- Detak Jantung Test 2: 118 BPM
- Suhu Test 1: 31.5°C
- Suhu Test 2: 31.0°C

Step 3 (Jawaban):
1. Saya cenderung merasa mudah gelisah → 2 (Sering)
2. Saya merasa sulit untuk tenang → 1 (Kadang-kadang)
3. Saya merasa mudah tersinggung → 3 (Hampir Selalu)
4. Saya merasa cepat marah → 2 (Sering)
5. Saya merasa tegang → 2 (Sering)
6. Saya merasa tidak sabar → 1 (Kadang-kadang)
7. Saya merasa sulit untuk rileks → 2 (Sering)

PERHITUNGAN:
Skor Mentah = 2+1+3+2+2+1+2 = 13
Skor Akhir = 13 × 2 = 26
Kategori = 3 (Severe/Stress Berat) 🔴
```

---

## 🔌 INTEGRASI SENSOR IoT

### Kirim Data Sensor via API:
```bash
curl -X POST http://localhost:5000/api/iot/sensor \
  -H "Content-Type: application/json" \
  -d "{\"heart_rate\": 118, \"temperature\": 31.5}"
```

### Contoh Arduino/ESP32:
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void loop() {
  int heartRate = readHeartRate();  // Baca sensor
  float temperature = readTemperature();  // Baca sensor
  
  HTTPClient http;
  http.begin("http://192.168.1.100:5000/api/iot/sensor");
  http.addHeader("Content-Type", "application/json");
  
  String data = "{\"heart_rate\":" + String(heartRate) + 
                ",\"temperature\":" + String(temperature) + "}";
  
  http.POST(data);
  http.end();
  
  delay(5000);  // Kirim setiap 5 detik
}
```

---

## 🛑 TROUBLESHOOTING

### Error: "Address already in use"
Server sudah berjalan. Stop dulu:
```bash
# Windows - matikan process port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Error: "Module not found"
Install ulang dependencies:
```bash
pip install -r requirements.txt
```

### Database error
Database akan otomatis dibuat saat pertama kali running. File: `stress_test.db`

---

## 📁 STRUKTUR FILE

```
final_project/
├── app.py                    ← Server utama (Flask)
├── requirements.txt          ← Dependencies Python
├── stress_test.db           ← Database SQLite (auto-created)
├── README.md                ← Dokumentasi lengkap
├── QUICKSTART.md            ← Panduan ini
├── templates/
│   ├── index.html           ← Landing page
│   ├── test.html            ← Halaman test
│   └── dashboard.html       ← Dashboard analytics
└── DATA PENELITIAN.xlsx    ← Dataset referensi
```

---

## 🎯 FITUR YANG SUDAH BERFUNGSI

✅ Kuesioner DASS-21 dengan 7 pertanyaan stress
✅ Perhitungan skor otomatis (raw score × 2)
✅ Kategori stress: Normal/Mild/Moderate/Severe/Extremely Severe
✅ Input data sensor IoT (detak jantung & suhu)
✅ Dashboard dengan grafik interaktif
✅ Tabel hasil test lengkap
✅ Responsive design (mobile-friendly)
✅ RESTful API untuk integrasi
✅ Database SQLite untuk penyimpanan
✅ UI modern dengan gradient & animations

---

## 📞 BANTUAN

Jika ada pertanyaan atau masalah:
1. Cek README.md untuk dokumentasi lengkap
2. Cek konsol browser (F12) untuk error di frontend
3. Cek terminal untuk error di backend

---

**Selamat menggunakan! 🚀**
