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

def notify_run(results, title: str = "PageSpeed Report") -> bool:
    """Send a compact summary to Telegram."""
    if not isinstance(results, list) or not results:
        return False

    lines = [f"<b>{title}</b>"]
    for r in results:
        url = r.get("url","");
        st  = r.get("strategy","");
        p   = r.get("performance", 0);
        a   = r.get("accessibility", 0);
        b   = r.get("best_practices", 0);
        s   = r.get("seo", 0);
        err = r.get("error");
        if err:
            lines.append(f"• <code>{st}</code> — {url}\n  ❗ <i>{err}</i>")
        else:
            lines.append(f"• <code>{st}</code> — {url}\n  P:{p} A:{a} BP:{b} SEO:{s}")
    wib = timezone(timedelta(hours=7))
    ts = datetime.now(wib).strftime("%d/%m/%Y %H:%M WIB")
    lines.append(f"\n<i>Generated {ts}</i>")
    return _post("\n".join(lines))
