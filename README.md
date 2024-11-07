# How To Run ICMP 

Jika anda run program ini melalui SSH Raspberry Pi (192.168.5.83), maka anda harus mempunyai akses `SUDO`terlebih dahulu agar program ICMP ini dapat dijalankan dengan maksimal

`Pertama` Masuk ke folder yang ada program Ping.py

`Kedua` Lalu Run program dengan Syntax > sudo python Ping.py

`Ketiga` Maka Program akan berjalan dengan sendirinya

=============================================================

untuk mengganti `SERVER ICMP`
- ping_loop = threading.Thread(target=ping, args=("google.com",))
- ganti `SERVER ICMP` dari ("example.com")

=============================================================

untuk Proses `Loop` dari fungsi nya 

def ping(host, timeout=1):
    dest = gethostbyname(host) 
    print("Pinging " + dest + " using Python:")
    print("")
    
    while True:
        delay = doOnePing(dest, timeout)
        print("Ping " + host)
        print(f"Reply from {dest}: time = {delay*1000:.0f} ms\n " if isinstance(delay, float) else delay)
        time.sleep(1)
  
