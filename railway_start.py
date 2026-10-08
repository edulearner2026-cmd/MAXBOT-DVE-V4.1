"""
MAX BOT Supervisor V2
يشغل البوت + الموقع في عملية واحدة مع إعادة تشغيل آمنة
"""
import subprocess
import threading
import os
import sys
import time
import signal

# إصلاح: بناء SITE_URL بشكل صحيح
domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
if domain and not os.environ.get("SITE_URL"):
    os.environ["SITE_URL"] = f"https://{domain}"
    print(f"[STARTUP] SITE_URL auto-set to: {os.environ['SITE_URL']}")

port = os.environ.get("PORT", "5001")
web_proc = None
bot_proc = None


def run_dashboard():
    global web_proc
    print("[STARTUP] Starting Dashboard...", flush=True)
    web_proc = subprocess.Popen([
        sys.executable, "-m", "gunicorn", "app:app",
        "--bind", f"0.0.0.0:{port}",
        "--workers", "2",
        "--threads", "4",
        "--timeout", "120"
    ])


def run_bot():
    global bot_proc
    print("[STARTUP] Starting Discord bot...", flush=True)
    bot_proc = subprocess.Popen([sys.executable, "-u", "main.py"])


def handle_sigterm(signum, frame):
    print("[SHUTDOWN] Received SIGTERM, stopping...", flush=True)
    for proc in [bot_proc, web_proc]:
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except:
                proc.kill()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)

    print("=" * 50)
    print("  MAX BOT - Starting on Railway...")
    print("=" * 50)

    # تشغيل الموقع في thread منفصل
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()

    # تشغيل البوت في العملية الرئيسية
    while True:
        run_bot()
        print("[BOT] Bot died — restarting in 5 seconds...", flush=True)
        time.sleep(5)
