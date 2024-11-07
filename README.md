# How To Run ICMP Ping Program 

Sebelum menjalankan program ini, pastikan mempunyai akses ke Raspberry Pi (atau perangkat lain) sebagai contoh alamat IP `192.168.5.83`. Lalu memerlukan juga perlu memiliki akses `SUDO` untuk menjalankan program secara maksimal, karena program ini menggunakan soket raw yang memerlukan izin administratif.

Langkah Langkah untuk Menjalankan Program :

`1. Masuk Ke dalam Folder Program`
Pertama, buka terminal dan navigasikan ke folder tempat file Ping.py berada. Gunakan perintah cd untuk masuk ke direktori yang sesuai.

Sebagai contoh >>> `cd /path/to/your/folder`

Gantilah /path/to/your/folder dengan jalur yang sesuai di mana file Ping.py disimpan.


`2. Untuk Menjalankan Program`
Setelah berada dalam folder file, maka jalankan program dengan `SYNTAX` berikut :

SYNTAX >>>  `sudo python3 Ping.py`

`3. Program Berjalan`
Setelah menjalankan `SYNTAX` diatas Program akan mulai berjalan secara otomatis dan akan mulai mengirimkan paket ping ke server yang ditentukan.

`Mengganti Server ICMP`
Jika ingin mengganti `SERVER ICMP` yang akan di Ping, maka dapat merubah argumen dari baris berikut :

- `ping_loop = threading.Thread(target=ping, args=("google.com",))`
Gantilah "google.com" dengan alamat server ICMP yang ingin di gunakan, misalnya >>

- `ping_loop = threading.Thread(target=ping, args=("example.com",))`
Pastikan untuk menggunakan `ALAMAT DOMAIN` atau `ALAMAT IP` yang valid.

`Proses Loop dari Fungsi Ping`
Program ini berfungsi untuk mengirimkan paket Ping secara berulang ulang ke server yang telah ditentukan.

`FUNGSI PING`
```python
def ping(host, timeout=1):
    dest = gethostbyname(host) 
    print("Pinging " + dest + " using Python:")
    print("")
    
    while True:
        delay = doOnePing(dest, timeout)
        print("Ping " + host)
        print(f"Reply from {dest}: time = {delay*1000:.0f} ms\n " if isinstance(delay, float) else delay)
        time.sleep(1)
```

Penjelasan :

- Mendapatkan Alamat IP: Fungsi ini mengonversi nama host menjadi alamat IP menggunakan gethostbyname.

- Menampilkan Informasi: Program akan menampilkan informasi bahwa ping sedang dilakukan.

- Looping: Di dalam loop while True, program akan terus mengirimkan paket ping ke alamat tujuan.

- Mengirim Ping: Fungsi doOnePing dipanggil untuk mengirimkan paket ping dan menunggu balasan.

- Menampilkan Waktu Respons: Setelah menerima balasan, waktu respons (delay) akan ditampilkan dalam milidetik.

- Delay: Program akan menunggu selama 1 detik sebelum mengirim ping berikutnya.

`Menhentikan Program`
Untuk menghentikan program saat sedang berjalan, Pengguna dapat menekan Ctrl + C di terminal. Ini akan memicu sinyal interrupt (SIGINT) dan memanggil fungsi signout, yang akan mencetak pesan keluar dan menghentikan program.

```python
def signout(sig, frame):
    print("\nProgram Exit..")
    sys.exit(0)
```
