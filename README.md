# trtntest

Kerangka Android APK berbasis transport Appium dari appstest. Tidak ada test case
fungsional, locator, credential, endpoint backend atau alur aplikasi.
Lihat [audit sumber](docs/SOURCE_AUDIT.md) untuk bukti dan keputusan migrasi.

## Prasyarat dan dependensi
Python >=3.10 (stdlib), Node yang kompatibel dengan versi Appium pilihan,
Appium + UiAutomator2, JDK, Android SDK/platform-tools dan perangkat/emulator Android.
Mesin ini sudah memiliki Appium 2.19.0 dan UiAutomator2 4.2.9; tidak perlu memasang
ulang atau meng-upgrade otomatis. Tidak ada paket pip wajib:

```bash
cd /home/icun/Project/trtntest
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Hanya jika menyiapkan mesin lain dengan versi yang sama (periksa kompatibilitas
Node/JDK/Android berdasarkan dokumentasi driver lebih dahulu):

```bash
npm install -g appium@2.19.0
appium driver install uiautomator2@4.2.9
```

Jangan gunakan install global ini untuk menimpa versi yang sudah ada.

## APK dan konfigurasi
APK belum ditemukan dalam lokasi yang diperiksa. Salin APK Anda ke folder
`/home/icun/Project/trtntest/apks/`. Tidak ada nama APK yang diasumsikan.
Buat konfigurasi lokal tanpa menimpa file yang ada:

```bash
cp -n config/example.json config/local.json
```

Isi `apk_path` dengan path aktual APK (relatif terhadap root proyek atau absolut),
`udid` dengan serial aktual, dan `appium_url` alamat server lokal. Nilai contoh
APK/UDID sengaja kosong. Package/activity tidak ditebak: driver dapat membaca
manifest APK; jika deteksi gagal, konfirmasi metadata APK sebelum memperluas config.

## Emulator/perangkat dan pemeriksaan awal
Buat/pilih AVD melalui Android Studio sesuai ABI/minimum Android APK aktual.
Untuk perangkat fisik, aktifkan USB debugging dan izinkan komputer ini.
Pilih satu serial secara eksplisit; jangan otomatis memakai perangkat pertama.
Pemeriksaan berikut tidak menginstal APK atau membuka sesi aplikasi:

```bash
cd /home/icun/Project/trtntest
python3 -m compileall -q framework scripts run_tests.py
python3 scripts/preflight.py --config config/local.json
appium driver list --installed
appium driver doctor uiautomator2
adb devices -l
```

Preflight exit 1 jika config/APK/tool belum siap; ini bukan kegagalan test aplikasi.
Preflight hanya memeriksa keberadaan tool dan konfigurasi, bukan koneksi server,
kesehatan device, integritas APK atau kelengkapan SDK. `adb devices` dapat memulai
ADB daemon lokal. Pemeriksaan doctor/device belum dijalankan saat setup ini.

## Menambahkan dan menjalankan test
Berikan skenario, precondition, langkah, expected result, environment yang
boleh diuji dan efek yang diizinkan sebelum menambah `tests/test_*.py` berupa
`unittest.TestCase`. Framework tidak otomatis membuka sesi; test yang disetujui
kelak dapat memakai `framework.config.load` dan context manager
`framework.appium_client.Appium`.

Setelah APK, environment dan skenario disetujui, jalankan server lokal:

```bash
appium --address 127.0.0.1 --port 4723
```

Di terminal lain, hanya setelah instruksi eksplisit untuk menjalankan test:

```bash
cd /home/icun/Project/trtntest
python3 run_tests.py --execute-approved
```

Saat ini runner menolak suite kosong dengan exit 2, bukan mengklaim lulus.
Tanpa flag runner juga menolak eksekusi. Flag bukan pengganti persetujuan pengguna.
Pembukaan sesi kelak dapat menginstal APK/server helper dan meluncurkan aplikasi;
startup aplikasi sendiri bisa menghubungi backend. `noReset=true`, `fullReset=false`
dan `autoGrantPermissions=false` bukan jaminan tanpa perubahan data.

## Laporan dan batasan
Runner menyediakan `reports/<timestamp UTC>/runner.log` dan `summary.json` untuk
suite yang benar-benar dijalankan. Tidak ada laporan hasil aplikasi saat ini.
Jangan masukkan credential ke pesan assertion/log. Screenshot, logcat dan upload
APK tidak dikumpulkan otomatis.

UiAutomator2 mengakses UI Android yang diekspos melalui accessibility. Pada Flutter,
ketersediaan Semantics/label/identifier harus diperiksa di APK aktual sebelum
memilih locator. Tidak ada jaminan semua widget dapat diakses. Lihat
[dokumentasi driver](https://github.com/appium/appium-uiautomator2-driver) dan
[pengujian aksesibilitas Flutter](https://docs.flutter.dev/ui/accessibility/accessibility-testing).

Masih dibutuhkan: APK aktual dan build/versinya, perangkat/AVD dan ABI/API yang
sesuai, environment backend yang diizinkan, skenario serta expected result,
kebutuhan akun (jika ada, sediakan melalui mekanisme lokal aman), dan izin
instalasi/peluncuran sebelum pemeriksaan runtime. Tidak ada test aplikasi,
instalasi APK, perubahan backend atau pengiriman ke layanan eksternal dilakukan.

## Pemeriksaan runtime 2 Oktober 2026
APK aktual `apks/Trantara DEV v1.0.3-b27.apk` ditemukan (package
`com.prahu.trantara.dev`, versionName `1.0.3-b27`, minSdk 24). Pengguna menyatakan
backend staging dan menginstruksikan eksekusi instalasi/pembukaan. Perangkat
Samsung SM-A528B Android 14 arm64-v8a sudah terotorisasi. `config/local.json`
dibuat berdasarkan APK dan UDID aktual. Doctor UiAutomator2: 0 required fixes;
bundletool merupakan temuan opsional.

Perintah observasi awal yang benar-benar dijalankan:
```bash
python3 scripts/inspect_initial_ui.py --install-launch-approved
```
Sesi berhasil, APK dibuka dan UI XML dibaca; layar tertutup dialog izin
notifikasi Android. Tidak memilih izin, tidak mengisi form dan tidak menekan
tombol aplikasi. Hasil tersimpan di
`reports/initial-ui-20261002T035015.919331Z/`. Jumlah test fungsional = 0.
Semantics widget Flutter dan alur aplikasi masih belum terverifikasi. Script
observasi dapat memasang/membuka APK; jalankan hanya dengan instruksi eksplisit.
Server Appium lokal yang digunakan untuk observasi dihentikan setelah selesai.

## Eksplorasi tanpa akun
Atas instruksi pengguna `explore`, navigasi non-transaksi dijalankan. Laporan
observasi, screenshot dan XML: [exploration.md](reports/explore-20261002T035257Z/exploration.md).
Tidak ada test fungsional atau login. Banyak content-desc Flutter terbaca,
tetapi field input/ikon masih membutuhkan identifier yang stabil.
