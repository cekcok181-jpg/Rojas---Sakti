# ⚡ Rojas-Sakti v4.0

Framework *Bug Hunting* dan *Vulnerability Scanner* murni berbasis Python. Dirancang untuk berjalan optimal di Termux maupun Linux tanpa memerlukan *wrapper* dari *tools* lain.

## ⚠️ DISCLAIMER (BACA DULU)
> **PERINGATAN KERAS:** 
> *Tool* ini dibuat murni untuk tujuan **Edukasi** dan **Ethical Hacking (Bug Bounty)**. 
> Segala bentuk penggunaan *tool* ini untuk menyerang, merusak, atau meretas sistem tanpa izin tertulis adalah **TANGGUNG JAWAB PENGGUNA SEPENUHNYA**. 
> **Penulis (cekcok181-jpg) TIDAK BERTANGGUNG JAWAB** atas segala kerusakan, kerugian, atau tuntutan hukum yang timbul akibat penyalahgunaan *tool* ini. Gunakan dengan bijak dan patuhi hukum yang berlaku!

## 🚀 Fitur
- **Time-Based Blind SQLi Scanner**: Mendeteksi SQL Injection meskipun tanpa pesan error.
- **WAF & Header Analyzer**: Menganalisis proteksi server dan header keamanan yang hilang.
- **Threaded Subdomain Finder**: Mencari subdomain rahasia dengan cepat.
- **Smart Port Scanner**: Memindai port dan mencuri banner service (Banner Grabbing).
- **XSS & Open Redirect Scanner**: Menguji kerentanan XSS dan Redirect.
- **Broken Link Hijacking (BLH)**: Mencari link domain mati yang berpotensi diambil alih.
- **Sensitive File Scanner**: Mendeteksi file rahasia yang terekspos (`.env`, `.git`, dll).
- **CORS Misconfiguration Scanner**: Menguji salah konfigurasi CORS yang berbahaya.

## 🛠️ Cara Instalasi (Termux/Linux)

Ikuti langkah-langkah berikut satu per satu:

**1. Update sistem dan instal Git & Python```

pkg update && pkg upgrade -y

pip install requests colorama pyfiglet

pkg install git python -y

git clone https://github.com/cekcok181-jpg/Rojas---Sakti.git

cd Rojas---Sakti

python main.py


💻 Contoh Penggunaan
Saat tools berjalan, Anda akan diminta memasukkan URL target. Gunakan target legal (seperti situs latihan http://testphp.vulnweb.com atau domain milik Anda sendiri).
