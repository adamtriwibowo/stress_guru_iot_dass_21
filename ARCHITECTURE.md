# 🏗️ System Architecture

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Landing Page│  │  Test Page   │  │  Dashboard   │       │
│  │   (Home)     │  │  (/test)     │  │ (/dashboard) │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                  │               │
└─────────┼──────────────────┼──────────────────┼───────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│                     Flask Backend (Python)                    │
│                                                               │
│  ┌────────────────────────────────────────────────────┐      │
│  │              RESTful API Endpoints                  │      │
│  │                                                     │      │
│  │  GET  /api/respondents     - Data responden        │      │
│  │  POST /api/respondents     - Simpan responden      │      │
│  │  GET  /api/questions       - Pertanyaan DASS-21    │      │
│  │  POST /api/test            - Submit test           │      │
│  │  GET  /api/results         - Hasil test            │      │
│  │  GET  /api/statistics      - Statistik             │      │
│  │  POST /api/iot/sensor      - Data sensor IoT       │      │
│  └────────────────────────────────────────────────────┘      │
│                           │                                    │
│  ┌────────────────────────────────────────────────────┐      │
│  │           Business Logic Layer                      │      │
│  │                                                     │      │
│  │  • DASS-21 Scoring Engine                           │      │
│  │  • Stress Category Calculator                       │      │
│  │  • Data Validation                                  │      │
│  │  • IoT Data Processor                               │      │
│  └────────────────────────────────────────────────────┘      │
│                           │                                    │
└───────────────────────────┼───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────┐        │
│  │          SQLite Database (stress_test.db)         │        │
│  │                                                   │        │
│  │  Tables:                                          │        │
│  │  • respondents     - Data peserta test           │        │
│  │  • test_results    - Hasil test lengkap          │        │
│  │  • dass21_questions - Pertanyaan kuesioner       │        │
│  └──────────────────────────────────────────────────┘        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌───────────────────────────┴───────────────────────────────────┐
│                  IoT DEVICES LAYER                             │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐    ┌──────────────────────┐         │
│  │  Heart Rate Sensor   │    │  Temperature Sensor  │         │
│  │   (Pulse Sensor)     │    │   (DHT11/DHT22)      │         │
│  └──────────────────────┘    └──────────────────────┘         │
│           │                                │                   │
│           └────────┐              ┌────────┘                   │
│                    ▼              ▼                             │
│         ┌──────────────────────────────────┐                   │
│         │    Microcontroller (ESP32)       │                   │
│         │  • Read sensor data              │                   │
│         │  • Send data via WiFi            │                   │
│         │  • POST to /api/iot/sensor       │                   │
│         └──────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Test Flow
```
User Access Web App
        │
        ▼
┌───────────────────┐
│ Step 1: Input Data│
│   Responden       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Step 2: Input Data│
│   Sensor IoT      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Step 3: Kuesioner │
│   DASS-21 (7 Q)   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Calculate Score   │
│ Raw Score × 2     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Determine Category│
│ (0-4 Level)       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Save to Database  │
│ (test_results)    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Show Result Page  │
│ (Score + Level)   │
└───────────────────┘
```

### DASS-21 Scoring Algorithm
```
┌─────────────────────┐
│ User Answers (0-3)  │
│ for 7 Questions     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Sum All Answers     │
│ Raw Score = Σ       │
│ Range: 0-21         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Multiply by 2       │
│ Final Score = Raw×2 │
│ Range: 0-42         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Check Category:     │
│ 0-14  → Cat 0       │
│ 15-18 → Cat 1       │
│ 19-25 → Cat 2       │
│ 26-33 → Cat 3       │
│ 34+   → Cat 4       │
└─────────────────────┘
```

---

## Technology Stack

```
FRONTEND              BACKEND               DATABASE
┌────────────┐       ┌────────────┐        ┌────────────┐
│ Bootstrap 5│       │ Python 3   │        │  SQLite 3  │
│ Chart.js   │  ◄──► │ Flask 3.0  │  ◄──►  │  Local DB  │
│ FontAwesome│       │ Flask-CORS │        │  .db file  │
│ JavaScript │       │ REST API   │        │            │
└────────────┘       └────────────┘        └────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Measures                │
├─────────────────────────────────────────┤
│  ✓ SQL Injection Prevention              │
│    - Parameterized queries               │
│    - Input sanitization                  │
│                                         │
│  ✓ CORS Configuration                    │
│    - Controlled API access               │
│    - Origin validation                   │
│                                         │
│  ✓ Input Validation                      │
│    - Frontend validation                 │
│    - Backend validation                  │
│    - Type checking                       │
│                                         │
│  ✓ Error Handling                        │
│    - Try-catch blocks                    │
│    - User-friendly error messages        │
│    - Logging for debugging               │
└─────────────────────────────────────────┘
```

---

## File Structure
```
final_project/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── stress_test.db                  # SQLite database
│
├── templates/
│   ├── index.html                  # Landing page
│   ├── test.html                   # Test wizard page
│   └── dashboard.html              # Analytics dashboard
│
├── README.md                       # Full documentation
├── QUICKSTART.md                   # Quick start guide
├── ARCHITECTURE.md                 # This file
│
├── DATA PENELITIAN.xlsx           # Reference dataset
├── read_excel.py                   # Excel reader script
├── analyze_dass21.py               # DASS-21 analysis script
└── test_app.py                     # Test script
```

---

## Deployment Options

### Option 1: Local Development
```bash
python app.py
# Server: http://localhost:5000
```

### Option 2: Network Deployment
```bash
# Get IP address
ipconfig  # Windows

# Run with network access
python app.py
# Access from other devices: http://YOUR_IP:5000
```

### Option 3: Cloud Deployment (Future)
- Deploy to Heroku, AWS, or GCP
- Use PostgreSQL instead of SQLite
- Add domain and SSL certificate

---

## API Documentation

### Respondents API
```
GET  /api/respondents
Response: [{id, code, name, age, gender, teaching_experience, created_at}]

POST /api/respondents
Body: {code, name, age, gender, teaching_experience}
Response: {id, message}
```

### Test API
```
POST /api/test
Body: {
  respondent_id,
  heart_rate_test1, heart_rate_test2,
  temperature_test1, temperature_test2,
  answers: {question_id: value}
}
Response: {message, score, category, level, description, color}
```

### Results API
```
GET  /api/results
Response: [{id, respondent_id, test_date, scores..., stress_category, stress_level}]

GET  /api/results/<respondent_id>
Response: [results for specific respondent]
```

### Statistics API
```
GET  /api/statistics
Response: {
  total_respondents,
  total_tests,
  average_score,
  min_score,
  max_score,
  category_distribution: [{category, count, avg_score}]
}
```

### IoT Sensor API
```
POST /api/iot/sensor
Body: {heart_rate, temperature, timestamp}
Response: {message, heart_rate, temperature, timestamp}
```

---

**System designed for scalability and maintainability** 🚀
