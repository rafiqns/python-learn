# Python Learn

Aplikasi web pembelajaran Python dengan fitur premium dan sistem pembayaran terintegrasi.

## Fitur

- **Autentikasi Pengguna**: Login dan registrasi menggunakan Flask-Login
- **Materi Pembelajaran**: Struktur bab dan sub-bab dengan konten teks, gambar, dan kode
- **Fitur Free & Pro**: Pembatasan akses konten premium untuk pengguna gratis
- **Sistem Pembayaran**: Integrasi dengan Midtrans untuk pembayaran
- **Admin Panel**: Pengelolaan materi dan pengguna
- **Responsif**: Tampilan yang responsif menggunakan Bootstrap

## Teknologi

- Flask 2.3.3
- SQLite (Flask-SQLAlchemy)
- Flask-Login untuk autentikasi
- Flask-WTF untuk formulir
- Midtrans untuk pembayaran
- Bootstrap 5 untuk UI

## Instalasi

1. Clone repositori ini:
```
git clone https://github.com/username/python-learn.git
cd python-learn
```

2. Buat virtual environment dan aktifkan:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependensi:
```
pip install -r requirements.txt
```

4. Konfigurasi variabel lingkungan:
```
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your_secret_key
export MIDTRANS_SERVER_KEY=your_midtrans_server_key
export MIDTRANS_CLIENT_KEY=your_midtrans_client_key
export MIDTRANS_MERCHANT_ID=your_midtrans_merchant_id
```

5. Inisialisasi database:
```
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

6. Jalankan aplikasi:
```
flask run
```

## Struktur Proyek

```
python-learn/
├── app.py                  # File utama aplikasi
├── auth.py                 # Blueprint autentikasi
├── main.py                 # Blueprint halaman utama
├── admin.py                # Blueprint admin panel
├── payment.py              # Blueprint pembayaran
├── models.py               # Model database
├── forms.py                # Formulir WTForms
├── requirements.txt        # Dependensi
├── static/                 # Aset statis
│   ├── css/
│   ├── js/
│   └── images/
└── templates/              # Template Jinja2
    ├── auth/
    ├── admin/
    ├── payment/
    └── errors/
```

## Akun Admin Default

- Email: admin@pythonlearn.com
- Password: admin123

## Lisensi

MIT License 