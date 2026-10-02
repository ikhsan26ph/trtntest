# Audit sumber — 2 Oktober 2026

## Fakta terverifikasi
- Tujuan `/home/icun/Project/trtntest` kosong saat pemeriksaan awal.
- Sumber lokal `/home/icun/Project/appstest`; remote origin `https://github.com/ikhsan26ph/appstest.git`.
- HEAD `a8a7bc0b589b72f40abea00e169d9ec38789a224`; `git status --short` kosong. Tidak melakukan fetch; kesamaan dengan HEAD remote terbaru belum diverifikasi.
- Bahasa Python. Runner sumber berupa CLI dan fungsi test dengan loop custom serta penghitung assertion; tidak ada konfigurasi pytest/unittest khusus.
- Struktur: modul di root, `tests/fixtures/` XML aplikasi lama, `analysis/` hasil analisis/temuan, `report/` Excel, `.venv/`, `.claude/`.
- README sumber: `python3 apk_analyzer.py <apk> --out analysis`; `python3 qa_agent.py --apk <apk> --goal <goal> --max-steps <n>`.
- Unit test sumber dapat dipanggil sebagai `python3 tests/test_uitree.py`, `python3 tests/test_formtest.py`, `python3 tests/test_oracle.py` (tidak dijalankan).
- `qa_agent.py` menggunakan Appium Python Client, UiAutomator2 dan Claude; APK diteruskan lewat capability app. `appium_client.py` menyediakan transport W3C melalui urllib.
- Pelaporan: JSON eksplorasi/crash, JSON dan Markdown analyzer, Excel berisi temuan hardcoded. Logging crash/logcat ada dalam agen.
- Dependensi deklaratif: androguard>=4.1, Appium-Python-Client>=4.0, anthropic>=0.40, openpyxl>=3.1. `oracle.py` juga mengimpor yaml tetapi PyYAML tidak tercantum langsung.
- Konfigurasi: APPIUM_URL, ANTHROPIC_API_KEY, CLAUDE_MODEL, argumen CLI dan aturan YAML; beberapa CLI memuat package/activity/UDID lama.

## Keputusan migrasi
Sumber mendukung Android APK melalui Appium/UiAutomator2. Bukan framework browser.
Diambil metode transport umum dari `appium_client.py`: request, sesi, source,
back, tap, clear, type_into, hide_keyboard dan context manager. Konstruktor/start
diadaptasi untuk capabilities eksplisit dari konfigurasi APK lokal. Metode
editable dengan XPath/indeks, komentar data lama, timeout Galaxy, package/activity
lama tidak dibawa. Runner baru memakai unittest stdlib, dengan log teks dan
ringkasan JSON per run; tidak ada dependensi Python tambahan.

Tidak disalin: tests/fixtures, oracle/rules/formtest, uitree (heuristik geometris
berdasarkan layar lama), tms_web/tms_seed/selesaikan_order (API/data/flow lama),
buat_laporan (temuan hardcoded), output analysis/report, .venv/.git/.claude/CLAUDE,
qa_agent (eksplorasi otonom dan pengiriman layar ke LLM), apk_analyzer (inferensi
fitur serta pembuatan test plan). Tidak ada secret atau environment lama dibawa.

## Batasan dan observasi runtime
Python 3.12.3, Node 26.8.1, Appium 2.19.0, UiAutomator2 4.2.9, adb 36.0.0 ditemukan.
Appium memberi warning peer dependency Appium 3 pada xcuitest dan beberapa
plugin global. Instalasi global tidak diubah. Tidak ada APK di tujuan atau sumber
(maxdepth 2 untuk sumber). Pencarian tidak mencakup seluruh komputer.
Kesiapan JDK/SDK, perangkat, server, kompatibilitas APK dan akses backend belum
terverifikasi melalui sesi. Tidak ada test aplikasi atau test sumber dijalankan.

## Referensi teknis
- https://github.com/appium/appium-uiautomator2-driver (capabilities, persyaratan dan doctor)
- https://docs.flutter.dev/ui/accessibility/accessibility-testing (aksesibilitas Flutter)
UiAutomator2 dipilih sebagai titik awal Android; akses elemen Flutter harus
terverifikasi pada APK aktual. Jika semantics tidak memadai, diperlukan bantuan
developer/build yang mendukung instrumentasi; tidak otomatis beralih ke driver
Flutter atau menebak locator koordinat.

## Pemeriksaan kerangka yang dijalankan
- compileall dan parsing AST seluruh file Python: berhasil.
- preflight config/example.json: exit 1 karena UDID kosong; tool adb/appium/node/java ditemukan dan APK proyek = 0.
- run_tests.py --execute-approved: exit 2 karena suite kosong, tanpa sesi aplikasi. Ini pemeriksaan pengaman runner, bukan hasil test aplikasi.
- git status sumber setelah pekerjaan: tetap kosong.

## Pembaruan runtime
Lihat bagian pemeriksaan runtime di README: APK baru tersedia, perangkat terotorisasi, instalasi/pembukaan dan pembacaan UI awal berhasil. Layar masih dialog notifikasi sistem; tidak ada test fungsional. Temuan sebelumnya mengenai APK/perangkat belum tersedia adalah kondisi saat setup awal.
