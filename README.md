# PageSpeed Monitor (CI-ready)

## Setup
1. Tambah target di `urls.csv` (kolom `url,strategy`).
2. Tambah **Actions Secrets** di GitHub Repo:
   - `PSI_API_KEY` (wajib)
   - `TELEGRAM_BOT_TOKEN` (opsional)
   - `TELEGRAM_CHAT_ID` (opsional)
3. Aktifkan GitHub Pages (Source: GitHub Actions).

## Run Local
```bash
pip install -r requirements.txt
cp .env.example .env  # isi PSI_API_KEY
python psi_csv_dashboard.py --csv urls.csv
# buka dashboard/dashboard.html
```

## CI (GitHub Actions)
- Jalan setiap hari **05:00 WIB**.
- Menghasilkan `dashboard/dashboard.html` dan memperbarui `dashboard/history.json` + `dashboard/history/YYYY-MM.json`.
- Commit ke `main` dan deploy ke GitHub Pages.
