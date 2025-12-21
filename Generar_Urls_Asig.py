#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import requests
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import WebDriverException


# ============================================================
#  BROWSER (SEB STYLE)
# ============================================================

def create_driver():
    # Try Firefox first
    try:
        fo = FirefoxOptions()
        fo.add_argument("--width=1600")
        fo.add_argument("--height=900")
        driver = webdriver.Firefox(options=fo)
        print("[+] Using Firefox (Selenium)")
        return driver
    except WebDriverException as e:
        print("[WARN] Could not start Firefox: %s" % getattr(e, "msg", "unknown error"))
    except Exception:
        print("[WARN] Could not start Firefox (unknown error)")

    # If Firefox fails, try Chrome
    try:
        co = ChromeOptions()
        co.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=co)
        print("[+] Using Chrome (Selenium)")
        return driver
    except WebDriverException as e:
        print("[WARN] Could not start Chrome: %s" % getattr(e, "msg", "unknown error"))
    except Exception:
        print("[WARN] Could not start Chrome (unknown error)")

    print("[ERR] No browser available. Install Firefox or Chrome and their drivers.")
    sys.exit(1)


# ============================================================
#  ARGUMENTS
# ============================================================

def parse_args():
    if len(sys.argv) < 3:
        print("USAGE: python Urls_Asig_Mix.py <domain> <course_id> [-fire]")
        print("Example: python Urls_Asig_Mix.py mop 21232 -fire")
        sys.exit(1)

    domain = sys.argv[1].lower()
    course_id = sys.argv[2]

    use_fire = False

    for opt in sys.argv[3:]:
        if opt == "-fire":
            use_fire = True
        else:
            print("Unknown option:", opt)
            print("Allowed options: -fire")
            sys.exit(1)

    base = "%s.cv.uma.es" % domain

    print("[+] Domain: %s" % base)
    print("[+] Course id: %s" % course_id)
    print("[+] Assignments: ALWAYS enabled (assign index will be scanned)")
    if use_fire:
        print("[+] Option -fire: also adding FIRE fixed URLs (SSO, login, etc.)")
    else:
        print("[+] Without -fire: only SEB style URLs")

    return base, course_id, use_fire


# ============================================================
#  LOGIN WITH SELENIUM (SEB)
# ============================================================

def login_and_get_cookies(base, course_id):
    login_url = "https://%s/course/view.php?id=%s" % (base, course_id)

    print("\n[+] Opening browser for login ...")
    print("[*] URL: %s" % login_url)

    driver = create_driver()

    try:
        driver.get(login_url)
        input(
            "\n>>> Do the full login in the browser window.\n"
            ">>> When you can see the course page, press ENTER here <<<\n"
        )
        selenium_cookies = driver.get_cookies()
    finally:
        driver.quit()

    jar = requests.cookies.RequestsCookieJar()
    count = 0
    for c in selenium_cookies:
        name = c.get("name")
        value = c.get("value")
        domain = c.get("domain") or base
        path = c.get("path") or "/"
        jar.set(name, value, domain=domain, path=path)
        count += 1

    print("[+] %d cookies captured from browser session" % count)
    if count == 0:
        print("[WARN] No cookies captured. Login probably failed.")
    return jar


# ============================================================
#  SCRAP UTILS (SEB STYLE URLS)
# ============================================================

def fetch_html(url, cookies):
    r = requests.get(url, cookies=cookies)
    r.raise_for_status()
    return r.text


def extract_hrefs(html):
    return re.findall(r'href=\"([^\"]+)\"', html)


def filter_moodle_urls(hrefs, base_url):
    patterns = [
        "/mod/resource/view.php",
        "/mod/folder/view.php",
        "/mod/url/view.php",
        "/mod/assign/view.php",
        "/mod/page/view.php",
        "/pluginfile.php",
    ]

    urls = set()

    for h in hrefs:
        abs_url = urljoin(base_url, h)
        p = urlparse(abs_url)
        clean = "*://%s%s" % (p.netloc, p.path)
        if p.query:
            clean += "?%s" % p.query

        for patt in patterns:
            if patt in clean:
                urls.add(clean + "*")
                break

    return urls


# ============================================================
#  FIXED SEB URLS (ALWAYS INCLUDE ASSIGNMENTS)
# ============================================================

def generar_urls_fijas_seb(base, course_id):
    esenciales = [
        "*://%s/course/view.php?id=%s*" % (base, course_id),
        "*://%s/course/resources.php?id=%s*" % (base, course_id),
        "*://%s/pluginfile.php/*" % base,               # View PDFs, etc.
        "*://%s/mod/assign/view.php*" % base,           # Submit assignments (POST + query)
        "*://%s/mod/assign/index.php?id=%s*" % (base, course_id),  # Assignment index
    ]
    return set(esenciales)


# ============================================================
#  FIXED FIRE URLS (ONLY IF -fire)
# ============================================================

def generar_urls_fijas_fire(base, course_id):
    esenciales = [
        "*://%s/course/view.php?id=%s*" % (base, course_id),
        "*://%s/course/resources.php?id=%s*" % (base, course_id),
        "*://%s/mod/assign/index.php?id=%s*" % (base, course_id),
    ]

    comunes = [
        "*://idpbridge.cv.uma.es/*",
        "*://idp.uma.es/*",
        "*://sso.uma.es/*",
        "*://login.uma.es/*",
        "*://autenticacion.uma.es/*",
        "*://auth.uma.es/*",
        "*://shibboleth.uma.es/*",
        "*://%s/login/*" % base,
        "*://%s/theme/*" % base,
        "*://%s/lib/*" % base,
        "*://%s/pluginfile.php/*" % base,
        "*://%s/auth/*" % base,
        "*://%s/simplesaml/*" % base,
        "*://%s/course/switchrole.php*" % base,
        "*://%s/mod/assign/view.php" % base,
    ]

    return set(esenciales + comunes)


# ============================================================
#  SCRAP COURSE (ALWAYS SCAN ASSIGN INDEX)
# ============================================================

def scrape_course(base, course_id, cookies):
    base_url = "https://%s" % base

    pages = [
        "%s/course/view.php?id=%s" % (base_url, course_id),
        "%s/course/resources.php?id=%s" % (base_url, course_id),
        "%s/mod/assign/index.php?id=%s" % (base_url, course_id),
    ]

    urls = set()

    for p in pages:
        try:
            html = fetch_html(p, cookies)
            hrefs = extract_hrefs(html)
            urls.update(filter_moodle_urls(hrefs, base_url))
            print("[OK] Analysed: %s" % p)
        except Exception as e:
            print("[ERR] Could not access %s: %s" % (p, e))

    return urls


# ============================================================
#  SAVE FILE (SEB FORMAT, NO QUOTES, NO COMMAS)
# ============================================================

def save_lines(lines, course_id):
    name = "URLs_%s.txt" % course_id
    with open(name, "w") as f:
        for line in sorted(lines):
            f.write("%s\n" % line)
    print("\n[+] Saved to %s" % name)


# ============================================================
#  MAIN
# ============================================================

def main():
    base, course_id, use_fire = parse_args()

    cookies = login_and_get_cookies(base, course_id)

    urls_fijas_seb = generar_urls_fijas_seb(base, course_id)
    urls_scrap = scrape_course(base, course_id, cookies)

    all_urls = urls_fijas_seb.union(urls_scrap)

    if use_fire:
        urls_fire = generar_urls_fijas_fire(base, course_id)
        all_urls = all_urls.union(urls_fire)

    save_lines(all_urls, course_id)


if __name__ == "__main__":
    main()
