import os
import requests
from datetime import datetime, timezone, timedelta

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

def notify_simple_report(dashboard_url: str, workflow_url: str = "", status: str = "SUCCESS") -> bool:
    """Kirim pesan ringkas hasil PageSpeed ke Telegram."""
    wib = timezone(timedelta(hours=7))
    ts = datetime.now(wib).strftime("%d/%m/%Y %H:%M:%S WIB")
    lines = [
        "<b>Hasil Pengecekan PageSpeed</b>",
        f"Tanggal & Waktu: {ts}",
        f"Status: <b>{status}</b>",
        f"Dashboard Report: <a href=\"{dashboard_url}\">{dashboard_url}</a>",
    ]
    if workflow_url:
        lines.append(f"\nWorkflow run: <a href=\"{workflow_url}\">{workflow_url}</a>")
    return _post("\n".join(lines))

notify_simple_report(
    dashboard_url="https://maazway.github.io/pagespeed-monitor-sgm/",
    workflow_url="https://github.com/maazway/pagespeed-monitor-sgm/actions/runs/...",
    status="SUCCESS"
)
