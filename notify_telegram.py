import os
import requests
from datetime import datetime, timezone, timedelta
import argparse

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")  # single chat or channel id (@channelusername)

def _post(text: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        return True
    except Exception:
        return False

def notify_simple_report(status: str = "SUCCESS") -> bool:
    """Kirim pesan ringkas hasil PageSpeed ke Telegram."""
    wib = timezone(timedelta(hours=7))
    ts = datetime.now(wib).strftime("%d/%m/%Y %H:%M:%S WIB")
    lines = [
        "<b>Hasil Pengecekan PageSpeed</b>",
        f"Tanggal & Waktu: {ts}",
        f"Status: <b>{status}</b>",
        "Dashboard utama (UI):",
        "<a href=\"https://maazway.github.io/pagespeed-monitor-sgm/\">https://maazway.github.io/pagespeed-monitor-sgm/</a>",
        "",
        "History (gabungan semua run):",
        "<a href=\"https://maazway.github.io/pagespeed-monitor-sgm/history.json\">https://maazway.github.io/pagespeed-monitor-sgm/history.json</a>",
    ]
    return _post("\n".join(lines))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", default="SUCCESS", help="Status laporan (SUCCESS/FAILED)")
    args = parser.parse_args()

    notify_simple_report(
        status=args.status,
    )
