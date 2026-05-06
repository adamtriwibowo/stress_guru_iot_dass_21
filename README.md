# 🚀 Sistem Informasi IoT untuk Uji Stress Guru Autis

Sistem informasi berbasis web menggunakan metode **Internet of Things (IoT)** dan **DASS-21** untuk mengukur tingkat stress pada guru autis.

## 📋 Fitur Utama

### ✅ **1. Kuesioner DASS-21**
- 7 pertanyaan stress terstandarisasi
- Skala Likert 0-3 (Tidak Pernah sampai Hampir Selalu)
- Perhitungan skor otomatis sesuai standar DASS-21

### ✅ **2. Integrasi Sensor IoT**
- **Detak Jantung** (Heart Rate Monitor) - 2x pengujian
- **Suhu Tubuh** (Temperature Sensor) - 2x pengujian
- Endpoint API untuk koneksi sensor real-time

### ✅ **3. Scoring Otomatis**
Perhitungan skor DASS-21 dengan kategori:
- **Category 0 - Normal**: Skor 0-14 ✅
- **Category 1 - Mild**: Skor 15-18 ⚠️
- **Category 2 - Moderate**: Skor 19-25 🔶
- **Category 3 - Severe**: Skor 26-33 🔴
- **Category 4 - Extremely Severe**: Skor 34+ 🔴🔴

### ✅ **4. Dashboard Analytics**
- Grafik distribusi stress
- Statistik real-time
- Tabel hasil test lengkap
- Visualisasi interaktif dengan Chart.js

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python Flask** - Web framework
- **SQLite** - Database
- **RESTful API** - Arsitektur API

### Frontend
- **Bootstrap 5** - UI framework
- **Chart.js** - Visualisasi data
- **Font Awesome** - Icon
- **Vanilla JavaScript** - Interaktivitas

## 📦 Instalasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Server
```bash
python app.py
```

Server akan berjalan di: **http://localhost:5000**

## 🌐 Halaman Web

### 1. **Beranda** (`/`)
- Landing page dengan informasi sistem
- Statistik overview
- Penjelasan kategori stress

### 2. **Mulai Test** (`/test`)
- Step 1: Input data responden
- Step 2: Input data sensor IoT
- Step 3: Kuesioner DASS-21 (7 pertanyaan)
- Step 4: Hasil test dengan rekomendasi

### 3. **Dashboard** (`/dashboard`)
- Statistik lengkap
- Grafik bar, pie, dan line chart
- Tabel hasil semua test
- Filter dan sorting data

## 🔌 API Endpoints

### Respondents
```
GET    /api/respondents          - Ambil semua responden
POST   /api/respondents          - Tambah responden baru
```

### Questions
```
GET    /api/questions            - Ambil pertanyaan DASS-21
```

### Test
```
POST   /api/test                 - Submit hasil test
```

### Results
```
GET    /api/results              - Ambil semua hasil test
GET    /api/results/<id>         - Ambil hasil test per responden
```

### Statistics
```
GET    /api/statistics           - Ambil statistik lengkap
```

### IoT Sensor
```
POST   /api/iot/sensor           - Terima data dari sensor IoT
```

## 📊 Cara Perhitungan DASS-21

### Langkah 1: Jawab Pertanyaan
Setiap pertanyaan memiliki skala:
- **0** = Tidak Pernah
- **1** = Kadang-kadang
- **2** = Sering
- **3** = Hampir Selalu

### Langkah 2: Hitung Skor Mentah
```
Skor Mentah = Jumlah semua jawaban (0-21)
```

### Langkah 3: Konversi ke Skor DASS-21
```
Skor Akhir = Skor Mentah × 2
```
*Perkalian 2 untuk equivalen dengan DASS-42*

### Langkah 4: Tentukan Kategori
```
Jika Skor <= 14  → Category 0 (Normal)
Jika Skor 15-18  → Category 1 (Mild)
Jika Skor 19-25  → Category 2 (Moderate)
Jika Skor 26-33  → Category 3 (Severe)
Jika Skor >= 34  → Category 4 (Extremely Severe)
```

### Contoh Perhitungan
```
Jawaban: [2, 1, 3, 2, 1, 2, 2]
Skor Mentah = 2+1+3+2+1+2+2 = 13
Skor Akhir = 13 × 2 = 26
Kategori = 3 (Severe/Stress Berat)
```

## 🔧 Koneksi Sensor IoT

Untuk menghubungkan sensor IoT nyata:

### 1. Endpoint Sensor
Kirim data sensor ke:
```
POST http://localhost:5000/api/iot/sensor
Content-Type: application/json

{
  "heart_rate": 118,
  "temperature": 31.5,
  "timestamp": "2026-04-14T10:30:00"
}
```

### 2. Contoh Arduino/ESP32 Code
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void sendSensorData() {
  WiFiClient client;
  HTTPClient http;
  
  http.begin(client, "http://YOUR_IP:5000/api/iot/sensor");
  http.addHeader("Content-Type", "application/json");
  
  String jsonData = "{\"heart_rate\":" + String(heartRate) + 
                    ",\"temperature\":" + String(temperature) + "}";
  
  int httpResponseCode = http.POST(jsonData);
  http.end();
}
```

## 📁 Struktur File

```
final_project/
├── app.py                      # Backend Flask application
├── requirements.txt            # Python dependencies
├── stress_test.db             # SQLite database (auto-created)
├── templates/
│   ├── index.html             # Landing page
│   ├── test.html              # Test page dengan kuesioner
│   └── dashboard.html         # Dashboard analytics
├── DATA PENELITIAN.xlsx      # Dataset referensi
├── README.md                  # Dokumentasi ini
├── read_excel.py              # Script baca Excel
└── analyze_dass21.py          # Script analisis DASS-21
```

## 🎨 Desain UI

Sistem menggunakan desain modern dengan:
- ✅ Gradient background yang menarik
- ✅ Card-based layout
- ✅ Smooth animations dan transitions
- ✅ Responsive design (mobile-friendly)
- ✅ Interactive charts dan graphs
- ✅ Color-coded stress categories
- ✅ Step-by-step wizard untuk test

## 🔒 Keamanan

- SQL Injection prevention dengan parameterized queries
- CORS enabled untuk API access
- Input validation di frontend dan backend
- SQLite database terproteksi

## 📈 Development

Untuk development lebih lanjut:

### Tambah Pertanyaan DASS-21
Edit di `app.py`:
```python
DASS21_STRESS_QUESTIONS = [
    # Tambah pertanyaan baru di sini
]
```

### Ubah Threshold Kategori
Edit fungsi `calculate_stress_category()` di `app.py`

### Tambah Fitur
- Export data ke Excel
- Email notification
- User authentication
- Real-time WebSocket untuk sensor
- Machine learning prediction

## 📞 Support

Untuk pertanyaan atau masalah, silakan buat issue atau hubungi developer.

## 📄 License

MIT License - Free to use and modify

---

**Dibuat dengan ❤️ untuk penelitian IoT dan kesehatan mental**

© 2026 IoT Stress Test System
