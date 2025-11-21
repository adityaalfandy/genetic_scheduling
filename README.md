# 🧬 Genetic Algorithm Scheduling System

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-00758F.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Sistem Penjadwalan Mata Kuliah Otomatis Berbasis Algoritma Genetika**

[Demo](#demo) • [Fitur](#-fitur-utama) • [Instalasi](#-instalasi) • [Dokumentasi](#-dokumentasi-api)

</div>

---

## 📋 Daftar Isi

- [Tentang Projekt](#-tentang-project)
- [Fitur Utama](#-fitur-utama)
- [Teknologi](#-teknologi)
- [Instalasi](#-instalasi)
- [Cara Menggunakan](#-cara-menggunakan)
- [Algoritma Genetika](#-algoritma-genetika)
- [Dokumentasi API](#-dokumentasi-api)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---

## 🎯 Tentang Project

Sistem penjadwalan mata kuliah yang menggunakan **Algoritma Genetika** untuk menghasilkan jadwal optimal tanpa bentrok waktu dosen, ruangan, dan mahasiswa. Sistem ini dilengkapi dengan **AI Explanation** yang menjelaskan setiap keputusan penjadwalan dan fitur **Auto-Fix** untuk memperbaiki konflik secara otomatis.

## ✨ Fitur Utama

### 🤖 Intelligent Scheduling
- ✅ Generate jadwal otomatis menggunakan Genetic Algorithm
- ✅ Fitness function dengan 9+ kriteria scoring
- ✅ Multi-constraint optimization (dosen, ruangan, waktu)
- ✅ Elitism dan adaptive mutation

### 💡 AI Explanation
- ✅ Penjelasan detail scoring setiap mata kuliah
- ✅ Identifikasi konflik dengan alasan spesifik
- ✅ Rekomendasi perbaikan otomatis

### 🔧 Smart Features
- ✅ **Manual Edit**: Edit jadwal dengan deteksi konflik real-time
- ✅ **Auto-Fix**: Perbaikan konflik otomatis tanpa regenerate
- ✅ **History Tracking**: Riwayat generasi dan fitness progression
- ✅ **Persistent Storage**: Data tersimpan permanen di database

### 🎨 User Interface
- ✅ Web-based interface dengan Tailwind CSS
- ✅ Real-time notifications
- ✅ Interactive modals dan loading indicators
- ✅ Responsive design

---

## 🛠️ Teknologi

| Kategori | Stack |
|----------|-------|
| **Backend** | FastAPI, Python 3.8+ |
| **Database** | MySQL 8.0+, SQLAlchemy, Alembic |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript |
| **Algorithm** | Custom Genetic Algorithm (no external GA library) |
| **API Docs** | Swagger UI, ReDoc |

---

## 📦 Instalasi

### Prasyarat

Pastikan sudah terinstall:
- Python 3.8 atau lebih tinggi
- MySQL 8.0 atau lebih tinggi
- pip (Python package manager)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/genetic-scheduling.git
cd genetic-scheduling
```

### 2️⃣ Buat Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**File `requirements.txt`:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pymysql==1.1.0
cryptography==41.0.7
python-dotenv==1.0.0
pydantic==1.10.13
jinja2==3.1.2
```

> ⚠️ **Note**: Jika error saat install pydantic 2.5.0, gunakan versi 1.10.13

### 4️⃣ Setup Database

```sql
-- Login ke MySQL
mysql -u root -p

-- Buat database
CREATE DATABASE genetic_scheduling;
EXIT;
```

### 5️⃣ Konfigurasi Environment

Buat file `.env` di root folder:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/genetic_scheduling
SECRET_KEY=your-secret-key-here
```

> 🔐 **Penting**: Ganti `your_password` dengan password MySQL Anda!

### 6️⃣ Jalankan Aplikasi

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di: **http://localhost:8000**

---

## 🎮 Cara Menggunakan

### Quick Start

1. **Buka aplikasi**: http://localhost:8000
2. **Import data dummy**: Klik tombol "📥 Import Data Dummy"
3. **Generate jadwal**: Klik "🚀 Generate Jadwal"
4. **Lihat hasil**: Jadwal akan tampil di tabel

### Step-by-Step Guide

#### 1. Import Data Dummy
```
- Klik tombol "📥 Import Data Dummy"
- Sistem akan mengisi database dengan:
  ✅ 8-10 Mata Kuliah
  ✅ 5-7 Dosen dengan preferensi waktu
  ✅ 7-10 Ruangan dengan fasilitas
```

#### 2. Generate Jadwal

```
- Klik "🚀 Generate Jadwal"
- Atur parameter (optional):
  • Population Size: 50 (default)
  • Max Generations: 100 (default)
  • Mutation Rate: 0.1 (default)
- Klik "Generate"
- Tunggu 5-30 detik
```

#### 3. Lihat Fitness Explanation

```
- Klik "📊 Lihat Fitness Explanation"
- Lihat detail scoring per mata kuliah
- Identifikasi konflik (ditandai merah)
```

#### 4. Edit Manual (Optional)

```
- Klik "Edit" pada jadwal tertentu
- Ubah hari/jam
- Sistem akan deteksi konflik otomatis
```

#### 5. Auto Fix Konflik

```
- Jika ada konflik setelah edit
- Klik "🔧 Auto Fix Konflik"
- GA akan memperbaiki jadwal bermasalah
```

---

## 🧬 Algoritma Genetika

### Representasi Kromosom

```python
Chromosome = [
    Gene(matkul=CS101, dosen=1, ruangan=A101, hari=Senin, jam=07:00-09:00),
    Gene(matkul=CS102, dosen=2, ruangan=Lab1, hari=Selasa, jam=09:00-11:00),
    ...
]
```

### Fitness Function

| Kondisi | Skor |
|---------|------|
| ✅ Tidak ada tabrakan waktu dosen | **+20** |
| ✅ Tidak ada tabrakan ruangan | **+20** |
| ✅ Tidak ada kelas paralel bertumpuk | **+15** |
| ✅ Sesuai preferensi dosen | **+5** |
| ✅ Fasilitas ruangan cocok | **+10** |
| ✅ Waktu efisien (07:00-19:00) | **+5** |
| ✅ Kapasitas ruangan cukup | **+5** |
| ❌ Tabrakan jadwal | **-50** |
| ❌ Kapasitas kurang | **-15** |
| ❌ Dosen mengajar >3 jam berturut | **-10** |

### Proses Evolusi

```mermaid
graph LR
    A[Inisialisasi<br/>Populasi] --> B[Evaluasi<br/>Fitness]
    B --> C[Seleksi<br/>Tournament]
    C --> D[Crossover<br/>Two-Point]
    D --> E[Mutasi<br/>Random/Smart]
    E --> F{Kondisi<br/>Terpenuhi?}
    F -->|Tidak| B
    F -->|Ya| G[Solusi<br/>Terbaik]
```

### Operators

#### 1. Selection: Tournament Selection
```python
- Pilih 3 kromosom random
- Ambil yang fitness tertinggi
- Tournament size: 3
```

#### 2. Crossover: Two-Point Crossover
```python
- Tukar segmen gen antara 2 parent
- Rate: 80%
- Preserve gene structure
```

#### 3. Mutation: Adaptive Mutation
```python
- Random mutation: waktu, ruangan, hari
- Smart mutation: fokus pada gen bermasalah
- Rate: 10% (normal), 20% (smart)
```

#### 4. Elitism
```python
- Simpan 2 kromosom terbaik
- Langsung ke generasi berikutnya
```

---

## 📚 Dokumentasi API

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 📥 Data Management

<details>
<summary><b>POST</b> <code>/api/data/import-dummy</code> - Import data dummy</summary>

**Response:**
```json
{
  "message": "Data dummy berhasil diimport"
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/data/mata-kuliah</code> - Tambah mata kuliah</summary>

**Request Body:**
```json
{
  "nama": "Struktur Data",
  "kode": "CS101",
  "sks": 3,
  "semester": 3
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/data/dosen</code> - Tambah dosen</summary>

**Request Body:**
```json
{
  "nama": "Dr. Ahmad Fauzi",
  "preferensi_waktu": "Senin-Rabu pagi"
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/data/ruangan</code> - Tambah ruangan</summary>

**Request Body:**
```json
{
  "nama": "Lab Komputer 1",
  "kapasitas": 30,
  "fasilitas": "Komputer, Proyektor, AC"
}
```
</details>

#### 📅 Jadwal Management

<details>
<summary><b>POST</b> <code>/api/jadwal/generate</code> - Generate jadwal</summary>

**Request Body:**
```json
{
  "population_size": 50,
  "max_generations": 100,
  "mutation_rate": 0.1
}
```

**Response:**
```json
{
  "message": "Jadwal berhasil digenerate",
  "fitness": 450,
  "generations": 100,
  "fitness_history": [420, 430, 440, 445, 450]
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/jadwal/list</code> - Ambil semua jadwal</summary>

**Response:**
```json
{
  "jadwal": [
    {
      "id": 1,
      "matkul_nama": "Struktur Data",
      "matkul_kode": "CS101",
      "dosen_nama": "Dr. Ahmad",
      "ruangan_nama": "A101",
      "hari": "Senin",
      "jam_mulai": "07:00",
      "jam_selesai": "09:00"
    }
  ],
  "total": 8
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/jadwal/edit</code> - Edit jadwal manual</summary>

**Request Body:**
```json
{
  "jadwal_id": 1,
  "hari": "Selasa",
  "jam_mulai": "09:00",
  "jam_selesai": "11:00"
}
```

**Response:**
```json
{
  "message": "Jadwal berhasil diupdate",
  "jadwal_id": 1,
  "conflicts": [],
  "has_conflicts": false
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/jadwal/auto-fix</code> - Auto fix konflik</summary>

**Response:**
```json
{
  "message": "Konflik berhasil diperbaiki",
  "fitness": 380
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/jadwal/fitness-explanation</code> - Lihat fitness explanation</summary>

**Response:**
```json
{
  "fitness_total": 320,
  "penjelasan": [
    {
      "matkul": "Struktur Data",
      "kode": "CS101",
      "penyebab": "Tidak ada tabrakan, dosen sesuai preferensi",
      "skor": 45
    }
  ]
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/jadwal/history</code> - Riwayat generasi</summary>

**Response:**
```json
{
  "riwayat": [
    {
      "id": 1,
      "generation_number": 100,
      "best_fitness": 450,
      "jadwal": {...}
    }
  ]
}
```
</details>

### Swagger UI

Dokumentasi interaktif tersedia di: **http://localhost:8000/docs**

---

## 🔧 Troubleshooting

### ❌ Error: Module Not Found

**Solusi:**
```bash
pip install -r requirements.txt
```

### ❌ Error: Can't connect to MySQL

**Solusi:**
1. Pastikan MySQL running
2. Cek `.env` - username/password benar
3. Cek database sudah dibuat: `CREATE DATABASE genetic_scheduling;`

```bash
# Cek status MySQL
# Windows (Services)
# Linux/Mac
sudo service mysql status
```

### ❌ Error: Port 8000 already in use

**Solusi:**
```bash
# Gunakan port lain
uvicorn app.main:app --reload --port 8001

# Atau kill process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### ❌ Error: pydantic-core compilation failed

**Solusi:**
```bash
# Downgrade pydantic
pip uninstall pydantic pydantic-core -y
pip install pydantic==1.10.13
```

### ⚠️ Fitness Score Rendah (< 100)

**Solusi:**
- Tambah `max_generations` → 200
- Tambah `population_size` → 100
- Kurangi `mutation_rate` → 0.05

### 📊 Database Tables Not Created

**Solusi:**
```python
# Buat file create_tables.py
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")

# Jalankan
python create_tables.py
```

---

## 📂 Struktur Project

```
genetic_scheduling/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   ├── database.py                  # Database configuration
│   ├── models/                      # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── mata_kuliah.py
│   │   ├── dosen.py
│   │   ├── ruangan.py
│   │   └── jadwal.py
│   ├── schemas/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── jadwal_service.py
│   │   └── data_service.py
│   ├── genetic_algorithm/           # GA implementation
│   │   ├── __init__.py
│   │   ├── chromosome.py
│   │   ├── population.py
│   │   ├── fitness.py
│   │   ├── selection.py
│   │   ├── crossover.py
│   │   └── mutation.py
│   ├── routes/                      # API routes
│   │   ├── __init__.py
│   │   ├── jadwal_routes.py
│   │   └── data_routes.py
│   └── static/                      # Frontend
│       └── index.html
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🧪 Testing

### Manual Testing

```bash
# 1. Import data dummy
curl -X POST http://localhost:8000/api/data/import-dummy

# 2. Generate jadwal
curl -X POST http://localhost:8000/api/jadwal/generate \
  -H "Content-Type: application/json" \
  -d '{"population_size": 50, "max_generations": 100, "mutation_rate": 0.1}'

# 3. Get jadwal
curl http://localhost:8000/api/jadwal/list

# 4. Fitness explanation
curl http://localhost:8000/api/jadwal/fitness-explanation
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Generation Time** | 5-30 detik (tergantung parameter) |
| **Average Fitness** | 300-500 (dari max ~600) |
| **Success Rate** | >95% (jadwal tanpa konflik kritis) |
| **Database Size** | ~2-5 MB (100 jadwal + history) |
| **API Response Time** | <200ms (endpoint non-GA) |

---

## 🚀 Deployment

### Docker (Coming Soon)

```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Checklist

- [ ] Ganti `SECRET_KEY` di `.env`
- [ ] Set `reload=False` di production
- [ ] Gunakan reverse proxy (Nginx)
- [ ] Enable HTTPS
- [ ] Backup database regular
- [ ] Monitor logging
- [ ] Rate limiting untuk API

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Development Guidelines

- Ikuti PEP8 style guide
- Tambahkan docstring untuk function baru
- Update README jika ada fitur baru
- Test sebelum commit

---

## 📝 Roadmap

- [x] Basic GA implementation
- [x] Web interface
- [x] Auto-fix feature
- [x] Fitness explanation
- [ ] Export jadwal ke PDF/Excel
- [ ] Multi-semester scheduling
- [ ] User authentication
- [ ] Email notifications
- [ ] Mobile responsive improvement
- [ ] Docker deployment
- [ ] Unit tests

---

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Your Name**
- GitHub: [@adityaalfandy](https://github.com/adityaalfandy)
- Email: adityaalfandy04@gmail.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- Genetic Algorithm inspiration from research papers

---

## 📞 Support

Jika ada pertanyaan atau masalah:
- 📧 Email: adityaalfandy04@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/adityaalfandy/genetic_scheduling)

---

<div align="center">

**⭐ Star project ini jika bermanfaat!**

Made with ❤️ using FastAPI & Genetic Algorithm

[⬆ Back to Top](#-genetic-algorithm-scheduling-system)

</div>
