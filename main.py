import os
import sys
import socket
import requests
import time
import re
import pyfiglet
import concurrent.futures
from urllib.parse import urlparse
from colorama import init, Fore, Style

# Inisialisasi colorama
init(autoreset=True)

# Mengabaikan warning SSL
requests.packages.urllib3.disable_warnings()

# User-Agent acak biar ga gampang diblokir WAF
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"
]

def get_headers():
    import random
    return {"User-Agent": random.choice(USER_AGENTS)}

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    rojas = pyfiglet.figlet_format("ROJAS", font="slant")
    sakti = pyfiglet.figlet_format("SAKTI v4", font="small")
    
    print(Fore.RED + Style.BRIGHT + rojas)
    print(Fore.CYAN + Style.BRIGHT + sakti)
    print(Fore.YELLOW + "  ═══════════════════════════════════════════════════════")
    print(Fore.GREEN + Style.BRIGHT + "       [+] Pure Python Advanced Bug Hunter [+]")
    print(Fore.MAGENTA + "       [ No Wrappers. 100% Original Logic ]")
    print(Fore.YELLOW + "  ═══════════════════════════════════════════════════════\n")

def menu():
    print(Fore.MAGENTA + Style.BRIGHT + "  ╔══════════════════════════════════════════════════════╗")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║" + Fore.WHITE + "                 [ MAIN DASHBOARD ]                   " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ╠══════════════════════════════════════════════════════╣")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.YELLOW + "[1]" + Fore.WHITE + " Time-Based Blind SQLi Scanner                    " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.YELLOW + "[2]" + Fore.WHITE + " WAF & Security Header Analyzer                   " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.YELLOW + "[3]" + Fore.WHITE + " Threaded Subdomain Finder                        " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.YELLOW + "[4]" + Fore.WHITE + " Smart Port Scanner (Banner Grab)                 " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.YELLOW + "[5]" + Fore.WHITE + " XSS & Open Redirect Scanner                      " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ╠══════════════════════════════════════════════════════╣")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.LIGHTGREEN_EX + "[6]" + Fore.WHITE + " Broken Link Hijacking (BLH) Scanner              " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.LIGHTGREEN_EX + "[7]" + Fore.WHITE + " Sensitive File Disclosure Scanner                " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.LIGHTGREEN_EX + "[8]" + Fore.WHITE + " CORS Misconfiguration Scanner                    " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ╠══════════════════════════════════════════════════════╣")
    print(Fore.MAGENTA + Style.BRIGHT + "  ║ " + Fore.RED + "[0]" + Fore.WHITE + " Exit Rojas-Sakti                                 " + Fore.MAGENTA + Style.BRIGHT + "║")
    print(Fore.MAGENTA + Style.BRIGHT + "  ╚══════════════════════════════════════════════════════╝\n")

# ==========================================
# 1. TIME-BASED BLIND SQL INJECTION
# ==========================================
def run_time_sqli():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ TIME-BASED BLIND SQLi ] ──")
    target = input(Fore.CYAN + "  [?] Target URL (misal: http://site.com/page.php?id=1): " + Fore.WHITE)
    print(Fore.YELLOW + "  [*] Menguji Time-Based Blind SQLi. Mohon tunggu...")
    
    payload = "' AND (SELECT 1 FROM (SELECT SLEEP(5))a)--"
    test_url = target + payload
    
    try:
        start_time = time.time()
        r = requests.get(test_url, headers=get_headers(), timeout=10, verify=False)
        end_time = time.time()
        response_time = end_time - start_time
        
        if response_time >= 5:
            print(Fore.GREEN + Style.BRIGHT + f"\n  [!!!] RENTAN TIME-BASED SQLi DITEMUKAN!")
            print(Fore.WHITE + f"  ├── Waktu respons: {response_time:.2f} detik (Server tertunda!)")
            print(Fore.WHITE + f"  └── Payload: {payload}")
        else:
            print(Fore.RED + f"\n  [-] Aman. Waktu respons normal ({response_time:.2f} detik).")
    except requests.exceptions.Timeout:
        print(Fore.GREEN + Style.BRIGHT + "\n  [!!!] RENTAN! Request timeout (Kemungkinan SLEEP berhasil dieksekusi).")
    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ==========================================
# 2. WAF & HEADER ANALYZER
# ==========================================
def run_header_analyzer():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ WAF & HEADER ANALYZER ] ──")
    target = input(Fore.CYAN + "  [?] Target URL (misal: https://site.com): " + Fore.WHITE)
    print(Fore.YELLOW + "  [*] Menganalisis Header & WAF...")
    
    try:
        r = requests.get(target, headers=get_headers(), timeout=5, verify=False)
        headers = r.headers
        
        print(Fore.CYAN + "\n  [+] Informasi Server:")
        print(Fore.WHITE + f"  ├── Server       : {headers.get('Server', 'Tidak diketahui')}")
        print(Fore.WHITE + f"  └── X-Powered-By : {headers.get('X-Powered-By', 'Tidak diketahui')}")
        
        waf_detected = "Tidak terdeteksi"
        if "cloudflare" in str(headers).lower(): waf_detected = "Cloudflare"
        elif "akamai" in str(headers).lower(): waf_detected = "Akamai"
        elif "sucuri" in str(headers).lower(): waf_detected = "Sucuri"
        
        print(Fore.YELLOW + f"\n  [+] WAF Terdeteksi: {Fore.WHITE}{waf_detected}")
        
        print(Fore.CYAN + "\n  [+] Analisis Security Headers:")
        sec_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']
        for h in sec_headers:
            if h in headers:
                print(Fore.GREEN + f"  ├── [V] {h}")
            else:
                print(Fore.RED + f"  ├── [X] {h} (Tidak Ada! Rentan)")
        print(Fore.CYAN + "  └── Selesai.")
    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ==========================================
# 3. THREADED SUBDOMAIN FINDER
# ==========================================
def check_subdomain(sub, domain):
    target = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(target)
        return f"  ├── [V] {target:<25} -> {ip}"
    except:
        return None

def run_subdomain_finder():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ SUBDOMAIN FINDER ] ──")
    domain = input(Fore.CYAN + "  [?] Target Domain (misal: example.com): " + Fore.WHITE)
    print(Fore.YELLOW + f"  [*] Mencari subdomain untuk {domain} (Multi-threading)...")
    
    subdomains = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'staging', 'test', 'portal', 'blog', 'vpn', 'cpanel']
    found = False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_subdomain, sub, domain): sub for sub in subdomains}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(Fore.GREEN + result)
                found = True
                
    if not found:
        print(Fore.RED + "  [-] Tidak ada subdomain yang aktif dari wordlist.")
    else:
        print(Fore.CYAN + "  └── Pemindaian Subdomain Selesai.")

# ==========================================
# 4. SMART PORT SCANNER (BANNER GRAB)
# ==========================================
def scan_port_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                s.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').split('\n')[0]
            except:
                banner = "Service tidak mengirim banner."
            s.close()
            return f"  ├── [+] Port {port:<5} TERBUKA | Info: {banner.strip()[:40]}"
        s.close()
    except:
        pass
    return None

def run_port_scanner():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ SMART PORT SCANNER ] ──")
    target = input(Fore.CYAN + "  [?] Target Domain/IP: " + Fore.WHITE)
    try:
        ip = socket.gethostbyname(target)
        print(Fore.YELLOW + f"  [*] Memindai port pada {ip} & mencuri banner...")
        
        ports = [21, 22, 23, 80, 443, 3306, 3389, 8080]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scan_port_banner, ip, port): port for port in ports}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(Fore.GREEN + result)
        print(Fore.CYAN + "  └── Pemindaian Port Selesai.")
    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ==========================================
# 5. XSS & OPEN REDIRECT SCANNER
# ==========================================
def run_xss_redirect():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ XSS & OPEN REDIRECT ] ──")
    target = input(Fore.CYAN + "  [?] Target URL (misal: http://site.com/?q=test): " + Fore.WHITE)
    print(Fore.YELLOW + "  [*] Menguji XSS & Open Redirect...")
    
    payloads = {
        "XSS": "<script>alert('ROJAS')</script>",
        "Redirect": "https://evil.com"
    }
    
    try:
        for name, payload in payloads.items():
            test_url = target.rsplit('=', 1)[0] + '=' + payload
            r = requests.get(test_url, headers=get_headers(), timeout=5, verify=False, allow_redirects=False)
            
            if name == "XSS" and payload in r.text:
                print(Fore.GREEN + Style.BRIGHT + f"\n  [!!!] RENTAN XSS DITEMUKAN!")
                print(Fore.WHITE + f"  └── URL: {test_url}")
                
            if name == "Redirect" and r.status_code in [301, 302]:
                if "evil.com" in r.headers.get('Location', ''):
                    print(Fore.GREEN + Style.BRIGHT + f"\n  [!!!] RENTAN OPEN REDIRECT DITEMUKAN!")
                    print(Fore.WHITE + f"  └── URL: {test_url}")
                    
        print(Fore.CYAN + "\n  └── Pemindaian XSS/Redirect Selesai.")
    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ==========================================
# 6. BROKEN LINK HIJACKING (BLH) SCANNER
# ==========================================
def check_link(url):
    try:
        domain = urlparse(url).netloc
        if not domain: return None
        # Cek apakah domain masih hidup
        socket.gethostbyname(domain)
        return None # Domain hidup
    except socket.gaierror:
        # Jika error, berarti domain mati (potensi diambil alih)
        return f"  ├── [!!!] BROKEN LINK: {url} (Domain Mati!)"
    except:
        return None

def run_blh_scanner():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ BROKEN LINK HIJACKING SCANNER ] ──")
    target = input(Fore.CYAN + "  [?] Target URL (misal: https://site.com): " + Fore.WHITE)
    print(Fore.YELLOW + "  [*] Mengambil link dari halaman target...")
    
    try:
        r = requests.get(target, headers=get_headers(), timeout=5, verify=False)
        # Mencari semua URL di dalam HTML
        links = re.findall(r'href=["\'](https?://[^\s"\'<>]+)["\']', r.text)
        links = list(set(links)) # Hapus duplikat
        
        print(Fore.YELLOW + f"  [*] Ditemukan {len(links)} link. Memeriksa status domain...")
        
        found = False
        for link in links:
            result = check_link(link)
            if result:
                print(Fore.GREEN + Style.BRIGHT + result)
                found = True
                
        if not found:
            print(Fore.RED + "  [-] Tidak ada Broken Link (Domain mati) yang ditemukan.")
        else:
            print(Fore.WHITE + "\n  [!] PERINGATAN: Domain yang mati ini bisa dibeli oleh hacker")
            print(Fore.WHITE + "      dan digunakan untuk mencuri data pengguna website ini (BLH).")
            
        print(Fore.CYAN + "  └── Pemindaian BLH Selesai.")
    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ==========================================
# 7. SENSITIVE FILE DISCLOSURE SCANNER
# ==========================================
def run_sensitive_file():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ SENSITIVE FILE DISCLOSURE ] ──")
    target = input(Fore.CYAN + "  [?] Target URL (misal: https://site.com): " + Fore.WHITE).rstrip('/')
    print(Fore.YELLOW + "  [*] Memeriksa file-file rahasia yang terekspos...")
    
    # Daftar file rahasia yang sering bocor
    sensitive_files = [
        '.env', '.git/config', '.git/HEAD', 'backup.zip', 'backup.sql', 
        'config.php.bak', 'db.sql', 'wp-config.php', 'phpinfo.php', 
        'robots.txt', 'sitemap.xml', 'adminer.php'
    ]
    
    found = False
    for file in sensitive_files:
        url = f"{target}/{file}"
        try:
            r = requests.get(url, headers=get_headers(), timeout=3, verify=False)
            if r.status_code == 200:
                print(Fore.GREEN + Style.BRIGHT + f"  ├── [!!!] DITEMUKAN: {url} (Status: 200 OK)")
                found = True
        except:
            pass
            
    if not found:
        print(Fore.RED + "  [-] Tidak ada file sensitif yang terekspos.")
    print(Fore.CYAN + "  └── Pemindaian File Sensitif Selesai.")

# ==========================================
# 8. CORS MISCONFIGURATION SCANNER
# ==========================================
def run_cors_scanner():
    print(Fore.YELLOW + Style.BRIGHT + "\n  ── [ CORS MISCONFIGURATION ] ──")
    target = input(Fore.CYAN + "  [?] Target URL (misal: https://api.site.com): " + Fore.WHITE)
    print(Fore.YELLOW + "  [*] Menguji konfigurasi CORS...")
    
    # Header Origin palsu
    test_origin = "https://evil-attacker.com"
    headers = get_headers()
    headers["Origin"] = test_origin
    
    try:
        r = requests.get(target, headers=headers, timeout=5, verify=False)
        
        acao = r.headers.get('Access-Control-Allow-Origin')
        acac = r.headers.get('Access-Control-Allow-Credentials')
        
        if acao:
            print(Fore.CYAN + f"\n  [+] Access-Control-Allow-Origin: {acao}")
            if acao == test_origin or acao == "*":
                if acac and acac.lower() == 'true':
                    print(Fore.GREEN + Style.BRIGHT + "\n  [!!!] RENTAN CORS MISCONFIGURATION!")
                    print(Fore.WHITE + "  └── Penyerang bisa mencuri data sensitif pengguna!")
                else:
                    print(Fore.YELLOW + "\n  [!] CORS Terbuka, tapi Credentials tidak diizinkan (Risiko Rendah).")
            else:
                print(Fore.RED + "\n  [-] Konfigurasi CORS terlihat aman.")
        else:
            print(Fore.RED + "\n  [-] Header CORS tidak ditemukan.")
            
        print(Fore.CYAN + "  └── Pemindaian CORS Selesai.")
    except Exception as e:
        print(Fore.RED + f"  [!] Error: {e}")

# ==========================================
# MAIN LOOP
# ==========================================
def main():
    clear_screen()
    banner()
    
    while True:
        menu()
        pilihan = input(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "  └──[root@Rojas-Sakti]~# " + Fore.WHITE)
        
        if pilihan == '1': run_time_sqli()
        elif pilihan == '2': run_header_analyzer()
        elif pilihan == '3': run_subdomain_finder()
        elif pilihan == '4': run_port_scanner()
        elif pilihan == '5': run_xss_redirect()
        elif pilihan == '6': run_blh_scanner()
        elif pilihan == '7': run_sensitive_file()
        elif pilihan == '8': run_cors_scanner()
        elif pilihan == '0': 
            print(Fore.RED + Style.BRIGHT + "\n  [*] Keluar... Jadilah Hacker Sejati!\n"); 
            break
        else: 
            print(Fore.RED + "\n  [!] Pilihan tidak valid!")

if __name__ == "__main__":
    main()
