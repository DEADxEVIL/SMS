#!/usr/bin/env python3
# DEADxOSINT - Termux Bulk Signup Page Launcher
# Opens official signup pages for manual use. It does NOT submit forms,
# request OTPs, read SMS, bypass CAPTCHAs, or automate account creation.

import json
import os
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

APP = "DEADxOSINT"
VERSION = "1.0"
BASE_DIR = Path.home() / ".deadxosint"
SETTINGS_FILE = BASE_DIR / "settings.json"
HISTORY_FILE = BASE_DIR / "launch_history.json"

# Directory links are entry points, not a guarantee that phone signup is supported.
SITES = [
    ("Facebook", "Social", "https://www.facebook.com/r.php"),
    ("Instagram", "Social", "https://www.instagram.com/accounts/emailsignup/"),
    ("X", "Social", "https://x.com/i/flow/signup"),
    ("TikTok", "Social", "https://www.tiktok.com/signup"),
    ("Snapchat", "Social", "https://www.snapchat.com/"),
    ("Telegram", "Messaging", "https://web.telegram.org/"),
    ("WhatsApp", "Messaging", "https://www.whatsapp.com/download"),
    ("Signal", "Messaging", "https://signal.org/download/"),
    ("Discord", "Social", "https://discord.com/register"),
    ("Reddit", "Social", "https://www.reddit.com/register/"),
    ("Pinterest", "Social", "https://www.pinterest.com/"),
    ("LinkedIn", "Professional", "https://www.linkedin.com/signup"),
    ("Tumblr", "Social", "https://www.tumblr.com/register"),
    ("VK", "Social", "https://vk.com/"),
    ("WeChat", "Messaging", "https://www.wechat.com/"),
    ("LINE", "Messaging", "https://line.me/"),
    ("Viber", "Messaging", "https://www.viber.com/"),
    ("KakaoTalk", "Messaging", "https://www.kakao.com/"),
    ("Zalo", "Messaging", "https://zalo.me/"),
    ("GroupMe", "Messaging", "https://groupme.com/"),
    ("TextNow", "Messaging", "https://www.textnow.com/"),
    ("TextFree", "Messaging", "https://www.textfree.us/"),
    ("Amazon India", "Shopping", "https://www.amazon.in/ap/register"),
    ("Amazon US", "Shopping", "https://www.amazon.com/ap/register"),
    ("eBay", "Shopping", "https://signup.ebay.com/pa/crte"),
    ("AliExpress", "Shopping", "https://login.aliexpress.com/"),
    ("Alibaba", "Shopping", "https://login.alibaba.com/"),
    ("Flipkart", "Shopping", "https://www.flipkart.com/account/login"),
    ("Myntra", "Shopping", "https://www.myntra.com/login"),
    ("Snapdeal", "Shopping", "https://www.snapdeal.com/"),
    ("Meesho", "Shopping", "https://www.meesho.com/"),
    ("Walmart", "Shopping", "https://www.walmart.com/account/signup"),
    ("Target", "Shopping", "https://www.target.com/account"),
    ("Best Buy", "Shopping", "https://www.bestbuy.com/identity/signin"),
    ("Etsy", "Shopping", "https://www.etsy.com/join"),
    ("Wayfair", "Shopping", "https://www.wayfair.com/"),
    ("Shopify", "Business", "https://www.shopify.com/signup"),
    ("Mercado Libre", "Shopping", "https://www.mercadolibre.com/"),
    ("Rakuten", "Shopping", "https://www.rakuten.com/"),
    ("Lazada", "Shopping", "https://www.lazada.com/"),
    ("Shopee", "Shopping", "https://shopee.com/"),
    ("Tokopedia", "Shopping", "https://www.tokopedia.com/"),
    ("Trendyol", "Shopping", "https://www.trendyol.com/"),
    ("PayPal", "Finance", "https://www.paypal.com/in/webapps/mpp/account-selection"),
    ("Google Pay", "Finance", "https://pay.google.com/"),
    ("PhonePe", "Finance", "https://www.phonepe.com/"),
    ("BHIM", "Finance", "https://www.bhimupi.org.in/"),
    ("Wise", "Finance", "https://wise.com/register"),
    ("Skrill", "Finance", "https://www.skrill.com/"),
    ("Neteller", "Finance", "https://www.neteller.com/"),
    ("Payoneer", "Finance", "https://www.payoneer.com/"),
    ("Western Union", "Finance", "https://www.westernunion.com/"),
    ("Xoom", "Finance", "https://www.xoom.com/"),
    ("Remitly", "Finance", "https://www.remitly.com/"),
    ("Razorpay", "Finance", "https://razorpay.com/"),
    ("MobiKwik", "Finance", "https://www.mobikwik.com/"),
    ("Uber", "Travel", "https://m.uber.com/looking"),
    ("Lyft", "Travel", "https://www.lyft.com/signup"),
    ("Ola", "Travel", "https://www.olacabs.com/"),
    ("Grab", "Travel", "https://www.grab.com/"),
    ("Airbnb", "Travel", "https://www.airbnb.com/"),
    ("Booking.com", "Travel", "https://www.booking.com/"),
    ("Agoda", "Travel", "https://www.agoda.com/"),
    ("Expedia", "Travel", "https://www.expedia.com/"),
    ("MakeMyTrip", "Travel", "https://www.makemytrip.com/"),
    ("Yatra", "Travel", "https://www.yatra.com/"),
    ("IRCTC", "Travel", "https://www.irctc.co.in/"),
    ("redBus", "Travel", "https://www.redbus.in/"),
    ("EaseMyTrip", "Travel", "https://www.easemytrip.com/"),
    ("Slack", "Productivity", "https://slack.com/get-started"),
    ("Zoom", "Productivity", "https://zoom.us/signup"),
    ("Trello", "Productivity", "https://trello.com/signup"),
    ("Asana", "Productivity", "https://asana.com/create-account"),
    ("Notion", "Productivity", "https://www.notion.so/signup"),
    ("Airtable", "Productivity", "https://airtable.com/signup"),
    ("ClickUp", "Productivity", "https://app.clickup.com/signup"),
    ("Zapier", "Productivity", "https://zapier.com/sign-up"),
    ("IFTTT", "Productivity", "https://ifttt.com/join"),
    ("Canva", "Productivity", "https://www.canva.com/signup"),
    ("Dropbox", "Productivity", "https://www.dropbox.com/register"),
    ("Box", "Productivity", "https://account.box.com/signup"),
    ("Evernote", "Productivity", "https://evernote.com/"),
    ("Todoist", "Productivity", "https://todoist.com/auth/signup"),
    ("Netflix", "Entertainment", "https://www.netflix.com/signup"),
    ("Spotify", "Entertainment", "https://www.spotify.com/signup"),
    ("YouTube", "Entertainment", "https://www.youtube.com/"),
    ("Disney+", "Entertainment", "https://www.disneyplus.com/sign-up"),
    ("Hulu", "Entertainment", "https://www.hulu.com/welcome"),
    ("Max", "Entertainment", "https://www.max.com/"),
    ("Prime Video", "Entertainment", "https://www.primevideo.com/"),
    ("SoundCloud", "Entertainment", "https://soundcloud.com/signup"),
    ("Twitch", "Entertainment", "https://www.twitch.tv/signup"),
    ("Vimeo", "Entertainment", "https://vimeo.com/join"),
    ("Dailymotion", "Entertainment", "https://www.dailymotion.com/signup"),
    ("Steam", "Gaming", "https://store.steampowered.com/join/"),
    ("Epic Games", "Gaming", "https://www.epicgames.com/id/register"),
    ("PlayStation", "Gaming", "https://www.playstation.com/"),
    ("Xbox", "Gaming", "https://www.xbox.com/"),
    ("Nintendo", "Gaming", "https://accounts.nintendo.com/register"),
    ("Roblox", "Gaming", "https://www.roblox.com/"),
    ("EA", "Gaming", "https://www.ea.com/"),
    ("Ubisoft", "Gaming", "https://ubisoftconnect.com/"),
    ("Garena", "Gaming", "https://account.garena.com/"),
    ("KRAFTON ID", "Gaming", "https://accounts.krafton.com/"),
    ("Tinder", "Dating", "https://tinder.com/"),
    ("Bumble", "Dating", "https://bumble.com/"),
    ("Badoo", "Dating", "https://badoo.com/"),
    ("OkCupid", "Dating", "https://www.okcupid.com/"),
    ("Match", "Dating", "https://www.match.com/"),
    ("Plenty of Fish", "Dating", "https://www.pof.com/"),
    ("Hinge", "Dating", "https://hinge.co/"),
    ("Coursera", "Education", "https://www.coursera.org/"),
    ("Udemy", "Education", "https://www.udemy.com/join/signup/"),
    ("edX", "Education", "https://www.edx.org/"),
    ("Khan Academy", "Education", "https://www.khanacademy.org/signup"),
    ("Skillshare", "Education", "https://www.skillshare.com/signup"),
    ("Duolingo", "Education", "https://www.duolingo.com/"),
    ("Unacademy", "Education", "https://unacademy.com/"),
    ("MyFitnessPal", "Fitness", "https://www.myfitnesspal.com/account/create"),
    ("Strava", "Fitness", "https://www.strava.com/register"),
    ("Headspace", "Wellness", "https://www.headspace.com/"),
    ("Calm", "Wellness", "https://www.calm.com/"),
    ("Practo", "Health services", "https://www.practo.com/"),
    ("Tata 1mg", "Health services", "https://www.1mg.com/"),
]

# ANSI colors work in most Termux terminals.
C = {
    "reset": "\033[0m", "cyan": "\033[96m", "green": "\033[92m",
    "yellow": "\033[93m", "red": "\033[91m", "magenta": "\033[95m",
    "bold": "\033[1m", "dim": "\033[2m"
}

def color(text, name):
    return f"{C.get(name, '')}{text}{C['reset']}"

def clear():
    os.system("clear")

def slow_print(text, delay=0.012):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def spinner(message, duration=1.0):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r{color(frames[i % len(frames)], 'cyan')} {message}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r" + " " * (len(message) + 4) + "\r", end="", flush=True)

def banner():
    clear()
    art = r"""
 ____  _____ ____  ____  __   __
|  _ \| ____|  _ \|  _ \ \ \ / /
| | | |  _| | | | | |_) | \ V /
| |_| | |___| |_| |  __/   | |
|____/|_____|____/|_|      |_|
"""
    print(color(art, "cyan"))
    print(color("        PHONE SIGNUP PAGE LAUNCHER", "magenta"))
    print(color(f"        Version {VERSION} | Termux / Android", "dim"))
    print(color("─" * 48, "cyan"))
    print(color("Manual signup only • No automatic OTP requests", "yellow"))
    print()

def ensure_data():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path, default):
    ensure_data()
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default

def save_json(path, data):
    ensure_data()
    temp = path.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    temp.replace(path)

def get_settings():
    settings = load_json(SETTINGS_FILE, {})
    return {"interval": settings.get("interval", 5), "launch_mode": settings.get("launch_mode", "interval")}

def open_url(url):
    # Android intent opens the user's default browser from Termux.
    if shutil.which("am"):
        try:
            result = subprocess.run(
                ["am", "start", "-a", "android.intent.action.VIEW", "-d", url],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, OSError):
            pass
    try:
        return bool(webbrowser.open_new_tab(url))
    except Exception:
        return False

def show_sites(items):
    if not items:
        print(color("No websites found.", "yellow"))
        return
    for i, (name, category, url) in enumerate(items, 1):
        print(f"{color(f'{i:03}', 'cyan')}  {color(name, 'bold')} {color('[' + category + ']', 'dim')}")
        print(f"     {color(url, 'dim')}")

def select_by_numbers(items):
    show_sites(items)
    if not items:
        return []
    raw = input("\nSelect numbers (e.g. 1,3,5) or A for all: ").strip().lower()
    if raw == "a":
        return list(items)
    selected = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(items):
            selected.append(items[int(part) - 1])
    # unique, preserve order
    seen, result = set(), []
    for site in selected:
        if site[0] not in seen:
            result.append(site)
            seen.add(site[0])
    return result

def launch_batch(items, settings):
    if not items:
        print(color("Nothing selected.", "yellow"))
        return
    interval = settings["interval"]
    print(color(f"\nReady to open {len(items)} signup pages.", "cyan"))
    print(color("The script only opens pages. It does not enter numbers, click Send OTP, or submit forms.", "yellow"))
    confirm = input("Continue? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    history = load_json(HISTORY_FILE, [])
    opened = 0
    failed = 0
    for index, (name, category, url) in enumerate(items, 1):
        print(f"\n{color(f'[{index}/{len(items)}]', 'cyan')} Opening {color(name, 'bold')}...")
        ok = open_url(url)
        if ok:
            opened += 1
            print(color("  Browser launch requested.", "green"))
            history.append({
                "site": name, "url": url,
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "result": "launched"
            })
        else:
            failed += 1
            print(color("  Could not launch automatically. Open this URL manually:", "red"))
            print(url)
            history.append({
                "site": name, "url": url,
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "result": "launch_failed"
            })
        save_json(HISTORY_FILE, history[-500:])
        if index < len(items):
            if interval == 0:
                continue
            for remaining in range(interval, 0, -1):
                print(f"\rNext page in {remaining}s... (Ctrl+C to stop)", end="", flush=True)
                time.sleep(1)
            print()
    print(color("\nLaunch batch finished.", "green"))
    print(f"Opened/requested: {opened} | Failed: {failed}")
    print("Complete signup and OTP verification manually in the browser.")

def search_sites():
    term = input("Search website/category: ").strip().lower()
    if not term:
        return
    matches = [s for s in SITES if term in s[0].lower() or term in s[1].lower()]
    show_sites(matches)
    input("\nPress Enter to continue...")

def category_menu():
    cats = sorted({s[1] for s in SITES})
    print("\nCategories:")
    for i, cat in enumerate(cats, 1):
        count = sum(1 for s in SITES if s[1] == cat)
        print(f"{i:2}. {cat} ({count})")
    raw = input("Choose category number: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(cats):
        return [s for s in SITES if s[1] == cats[int(raw) - 1]]
    print(color("Invalid category.", "red"))
    return []

def settings_menu(settings):
    print("\nLaunch interval:")
    print("0. Open pages without delay")
    print("5. 5 seconds (default)")
    print("10. 10 seconds")
    print("30. 30 seconds")
    raw = input(f"Choose seconds [current {settings['interval']}]: ").strip()
    if raw:
        try:
            value = int(raw)
            if value not in (0, 5, 10, 30):
                raise ValueError
            settings["interval"] = value
            save_json(SETTINGS_FILE, settings)
            print(color("Settings saved.", "green"))
        except ValueError:
            print(color("Choose 0, 5, 10, or 30.", "red"))
    input("Press Enter to continue...")

def main():
    settings = get_settings()
    while True:
        banner()
        print(f"Website directory: {color(str(len(SITES)), 'green')} entries")
        print(f"Delay between launches: {color(str(settings['interval']) + ' seconds', 'cyan')}")
        print()
        print(color("[1]", "cyan"), "Open ALL websites")
        print(color("[2]", "cyan"), "Select websites to open")
        print(color("[3]", "cyan"), "Open a category")
        print(color("[4]", "cyan"), "Search website directory")
        print(color("[5]", "cyan"), "View all websites")
        print(color("[6]", "cyan"), "Change launch interval")
        print(color("[7]", "cyan"), "View launch history")
        print(color("[0]", "red"), "Exit")
        choice = input("\nDEADxOSINT > ").strip()

        if choice == "1":
            launch_batch(SITES, settings)
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            selected = select_by_numbers(SITES)
            launch_batch(selected, settings)
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            selected = category_menu()
            if selected:
                launch_batch(selected, settings)
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            search_sites()
        elif choice == "5":
            banner()
            show_sites(SITES)
            input("\nPress Enter to return to menu...")
        elif choice == "6":
            settings_menu(settings)
        elif choice == "7":
            history = load_json(HISTORY_FILE, [])
            print("\nRecent launch history:")
            for row in history[-30:]:
                print(f"{row.get('time')} | {row.get('site')} | {row.get('result')}")
            if not history:
                print("No launch history yet.")
            input("\nPress Enter to continue...")
        elif choice == "0":
            print(color("Exiting DEADxOSINT.", "cyan"))
            break
        else:
            print(color("Invalid option.", "red"))
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + color("Stopped by user.", "yellow"))
        sys.exit(0)
