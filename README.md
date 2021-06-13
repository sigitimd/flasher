# flasher
A simple, fast flash sale bot for Shopee without web automation

# Bahan-Bahan
### PC/Laptop
- Python 3.8.x

Download Python di https://www.python.org/downloads/
### Android
- Termux
- Python 3.8.x

Install Termux di play store lalu install Python dengan perintah berikut:
```
pkg install python
```

# Penggunaan
Pertama, clone repo ini dulu
```
git clone https://github.com/bro-11/flasher
```
Selanjutnya masuk ke direktori `flasher` dengan perintah `cd flasher` (buat yg blm tau)

Jika belum install modul `requests` dan `colorama`, silahkan install terlebih dahulu
```
pip install requests colorama
```
Setelah itu login dengan mengetikkan perintah berikut
```
python main.py login
```
Jika berhasil login, Informasi login akan disimpan di file `cookie`, jadi tidak perlu susah payah login ulang setiap kali mau pake.

nah selanjutnya bisa langsung pakai botnya
```
python main.py
```
untuk speed, klo saya paling cepet `1.617 detik` menggunakan koneksi internet biasa (kartu 3).

# Opsi Checkout
Mungkin ada yg ingin mengganti opsi checkout seperti penggunaan kode voucher, channel logistik, dropshipping, dll.

Nama | Keterangan
-----|-----------
enable_dropshipping|Mengaktifkan fitur dropshipping
disable_dropshipping|menonaktifkan fitur dropshipping
logistic|mengganti channel logistik
payment|mengganti metode pembayaran
use_coins|mengaktifkan/menonaktifkan penggunaan koin
free_shipping_voucher|menggunakan voucher pengiriman

Catatan: opsi diatas hanyalah pilihan dan belum tentu work jika diubah, saran saya gunakan opsi default saja karena menurut saya itu yg lebih berpeluang work di segala kondisi

# Notifikasi Telegram
Biasanya ada yg nanya, bisa gk dikasih notif telegram?\
nah jadi gini cara buat notif telegramnya.

Jika blm install modul `python-telegram-bot`, bisa install dulu dengan perintah dibawah
```
pip install python-telegram-bot
```

Pertama, Jalankan script `telegraminit.py` dengan argumen token bot telegram yang akan digunakan, contohnya seperti dibawah
```
python telegraminit.py 1416918954:UhIPbRilKWBMrSzxyHmVQY1l0rTBIiFefCV
```
Setelah itu masuk ke aplikasi Telegram, lalu kirim pesan teks apapun ke bot anda. Karena `chatid` diperlukan agar bot dapat mengirim pesan.\
Jika menerima balasan `Inisialisasi Sukses` maka notif telegram sudah siap digunakan.

Untuk menonaktifkan notif Telegram, simpel saja, tinggal hapus file `telegramdata`

# Donasi
Bagi yg mau donasi atau request fitur, bisa chat Telegram saya dibawah (fast respon klo lagi ada)

[<img src="https://img.shields.io/badge/telegram-mikeytzyw-blue?style=flat&logo=telegram">](https://t.me/mikeytzyw)

Seikhlasnya saja :)

# FAQ
**Kok speednya gak sesuai sama yg di youtube?**\
Ya jangan salahin scriptnya, salahin koneksi internet lo bambank.\
dan yg di youtube itu bukan saya ya, jdi jangan salah paham

**Gak dapet kode otp**\
Ya harus gimana lagi, saya coba udh work, mungkin anda belum beruntung

**CheckoutError: metode pembayaran yang anda pilih tidak tersedia**\
Lihat issue [#14](https://github.com/bro-11/flasher/issues/14)

**Login error: username/password tidak valid**\
Jika login menggunakan nomor telepon, harus di awali dengan 62 bukan 0, contoh `6289999999`

**Kenapa lumba-lumba loncatnya rame-rame?**\
Karena lo wibu
