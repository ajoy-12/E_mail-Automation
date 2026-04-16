from playwright.sync_api import sync_playwright
import csv
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ]
    )
    # Context তৈরি (real browser mimic)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1280, 'height': 720}
    )
    page = context.new_page()
    page.goto("https://mail.google.com")
    # Login
    page.fill("input[type='email']", "email")
    page.press("input[type='email']", "Enter")
    page.wait_for_timeout(3000)

    page.fill("input[type='password']", "password")
    page.press("input[type='password']", "Enter")
    page.wait_for_timeout(10000)
    # Wait inbox
    page.wait_for_selector("tr.zA", timeout=20000)
    # SCROLL FUNCTION (IMPORTANT)
    for _ in range(30):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1500)

    emails = page.query_selector_all("tr.zA")

    inbox_data = []
    read_count = 0
    unread_count = 0

    for email in emails:
        try:
            sender = email.query_selector(".yW span").inner_text()
            subject = email.query_selector(".bog").inner_text()
            time_text = email.query_selector("td.xW span").get_attribute("title")
            inbox_data.append([sender, subject, time_text])
            classes = email.get_attribute("class")
            if classes and "zE" in classes:
                unread_count += 1
            else:
                read_count += 1
        except:
            continue
    print("Read:", read_count)
    print("Unread:", unread_count)
    # SPAM
    page.goto("https://mail.google.com/mail/u/0/#spam")
    page.wait_for_timeout(5000)

    for _ in range(10):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1500)

    spam_emails = page.query_selector_all("tr.zA")

    spam_data = []
    for email in spam_emails:
        try:
            sender = email.query_selector(".yW span").inner_text()
            subject = email.query_selector(".bog").inner_text()
            spam_data.append([sender, subject])
        except:
            continue

    print("Spam:", len(spam_emails))

    # CSV SAVE (FIXED)
    with open("inbox_emails1.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Sender", "Subject", "Time"])
        writer.writerows(inbox_data)

    with open("spam_emails.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Sender", "Subject"])
        writer.writerows(spam_data)

        with open("read_emails.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["Sender", "Subject"])
            writer.writerows(spam_data)

    with open("unread_emails.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Sender", "Subject"])
        writer.writerows(spam_data)

    print("✅ CSV saved correctly")

    browser.close()