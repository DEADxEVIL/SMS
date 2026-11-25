#!/usr/bin/env python3
"""
DEADxOSINT Phone Signup Manager
A local directory, browser launcher, and manual OTP tracker.
Does NOT submit phone numbers or request/send OTPs automatically.
"""

import json
import os
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

APP_NAME = "DEADxOSINT Phone Signup Manager"
DATA_DIR = Path.home() / ".deadxosint_phone_manager"
DATA_FILE = DATA_DIR / "records.json"

# Directory links are starting points only. A service may require email,
# an app, regional eligibility, or additional verification.
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
    (" redBus", "Travel", "https://www.redbus.in/"),
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

STATUSES = ("Pending", "Received", "Verified", "Not required")


def load_records():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        return {}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read saved records; starting with an empty tracker.")
        return {}


def save_records(records):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp = DATA_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    temp.replace(DATA_FILE)


def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value


def show_sites(items):
    if not items:
        print("No matching websites.")
        return
    for idx, (name, category, url) in enumerate(items, 1):
        print(f"{idx:3}. [{category}] {name} — {url}")


def choose_sites(items):
    show_sites(items)
    if not items:
        return []
    raw = input("\nEnter numbers separated by commas (e.g. 1,3,5), or 'a' for all: ").strip().lower()
    if raw == "a":
        return items
    chosen = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(items):
            chosen.append(items[int(part) - 1])
    # preserve order, remove duplicates
    unique = []
    seen = set()
    for item in chosen:
        if item[0] not in seen:
            unique.append(item)
            seen.add(item[0])
    return unique


def open_sites(items):
    if not items:
        return
    print(f"\nOpening {len(items)} selected signup page(s) in your browser...")
    for name, _, url in items:
        try:
            opened = webbrowser.open_new_tab(url)
            print(f"  {'Opened' if opened else 'Tried'}: {name}")
        except Exception as exc:
            print(f"  Could not open {name}: {exc}")
    print("Complete any signup and OTP step yourself on each official website.")


def add_or_update_record(records):
    site = input_nonempty("Website/service name: ")
    phone = input_nonempty("Your phone number (include country code): ")
    if len(phone) > 40:
        print("Phone entry is too long.")
        return
    status = input("Status [Pending/Received/Verified/Not required] (default Pending): ").strip().title() or "Pending"
    if status not in STATUSES:
        print("Invalid status.")
        return
    otp = ""
    if status in ("Received", "Verified"):
        otp = input("OTP (optional; stored locally in plain text): ").strip()
    note = input("Note (optional): ").strip()
    records[site.lower()] = {
        "site": site,
        "phone": phone,
        "status": status,
        "otp": otp,
        "note": note,
        "updated": datetime.now().isoformat(timespec="seconds"),
    }
    save_records(records)
    print("Record saved locally.")


def list_records(records):
    if not records:
        print("No tracked records yet.")
        return
    print("\nSaved records:")
    for entry in sorted(records.values(), key=lambda x: x.get("site", "").lower()):
        print(f"- {entry.get('site')} | {entry.get('phone')} | {entry.get('status')} | updated {entry.get('updated')}")
        if entry.get("otp"):
            print(f"    OTP: {entry['otp']}")
        if entry.get("note"):
            print(f"    Note: {entry['note']}")


def delete_record(records):
    if not records:
        print("No records to delete.")
        return
    list_records(records)
    key = input_nonempty("\nEnter exact website/service name to delete: ").lower()
    if key in records:
        del records[key]
        save_records(records)
        print("Record deleted.")
    else:
        print("No matching record.")


def main():
    records = load_records()
    while True:
        print(f"\n=== {APP_NAME} ===")
        print(f"Website directory: {len(SITES)} entries")
        print("1. List all websites")
        print("2. Search websites")
        print("3. Filter by category")
        print("4. Open selected signup pages")
        print("5. Add/update manual OTP record")
        print("6. View saved records")
        print("7. Delete a saved record")
        print("0. Exit")
        choice = input("\nSelect: ").strip()

        if choice == "1":
            show_sites(SITES)
        elif choice == "2":
            term = input_nonempty("Search name/category: ").lower()
            matches = [s for s in SITES if term in s[0].lower() or term in s[1].lower()]
            show_sites(matches)
        elif choice == "3":
            categories = sorted({s[1] for s in SITES})
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            raw = input("Category number: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(categories):
                show_sites([s for s in SITES if s[1] == categories[int(raw) - 1]])
            else:
                print("Invalid category.")
        elif choice == "4":
            selected = choose_sites(SITES)
            open_sites(selected)
        elif choice == "5":
            add_or_update_record(records)
        elif choice == "6":
            list_records(records)
        elif choice == "7":
            delete_record(records)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        sys.exit(0)
