#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException


# ============================================================
#  CONFIG
# ============================================================

CONTENT_PATHS = set([
    "/mod/assign/view.php",
    "/mod/page/view.php",
    "/mod/folder/view.php",
    "/mod/resource/view.php",
    "/mod/url/view.php",
])


# ============================================================
#  BROWSER (LOGIN)
# ============================================================

def create_driver():
    try:
        fo = FirefoxOptions()
        fo.add_argument("--width=1600")
        fo.add_argument("--height=900")
        driver = webdriver.Firefox(options=fo)
        print("[+] Using Firefox (Selenium)")
        return driver
    except Exception:
        pass

    try:
        co = ChromeOptions()
        co.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=co)
        print("[+] Using Chrome (Selenium)")
        return driver
    except Exception:
        pass

    print("[ERR] No browser available")
    sys.exit(1)


# ============================================================
#  ARGUMENTS
# ============================================================

def parse_args():
    if len(sys.argv) < 3:
        print("USAGE: python urls_seb.py <domain> <course_id>")
        sys.exit(1)

    base = "%s.cv.uma.es" % sys.argv[1].lower()
    course_id = sys.argv[2]

    print("[+] Domain:", base)
    print("[+] Course id:", course_id)

    return base, course_id


# ============================================================
#  LOGIN -> COOKIES
# ============================================================

def login_and_get_cookies(base, course_id):
    url = "https://%s/course/view.php?id=%s" % (base, course_id)

    print("[+] Opening browser for login")
    print("[+] URL:", url)

    driver = create_driver()
    driver.get(url)

    input("\n>>> Do the full login and press ENTER here <<<\n")

    jar = requests.cookies.RequestsCookieJar()
    for c in driver.get_cookies():
        jar.set(
            c["name"],
            c["value"],
            domain=c.get("domain") or base,
            path=c.get("path") or "/"
        )

    driver.quit()

    print("[+] Cookies captured:", len(jar))
    return jar


# ============================================================
#  HTML UTILS
# ============================================================

def fetch_html(url, cookies):
    r = requests.get(url, cookies=cookies, timeout=20)
    r.raise_for_status()
    return r.text


def extract_hrefs(html):
    soup = BeautifulSoup(html, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]


def seb_format(url):
    url = url.split("#", 1)[0]
    p = urlparse(url)
    if not p.netloc or not p.path:
        return None

    out = "*://%s%s" % (p.netloc, p.path)
    if p.query:
        out += "?%s" % p.query
    return out + "*"


# ============================================================
#  FIXED URLS
# ============================================================

def generar_urls_fijas_seb(base, course_id):
    print("[+] Adding fixed SEB URLs")

    return set([
        "*://%s/course/view.php?id=%s*" % (base, course_id),
        "*://%s/course/resources.php?id=%s*" % (base, course_id),
        "*://%s/pluginfile.php/*" % base,
        "*://%s/mod/assign/view.php*" % base,
        "*://%s/mod/assign/index.php?id=%s*" % (base, course_id),
    ])


# ============================================================
#  STEP 1: COLLECT ACTIVITY PAGES
# ============================================================

def collect_activities(hrefs, base_url, base_host):
    activities = set()
    modurls = set()

    for h in hrefs:
        abs_url = urljoin(base_url, h)
        p = urlparse(abs_url)

        if p.netloc != base_host:
            continue
        if p.path not in CONTENT_PATHS:
            continue

        activities.add(abs_url)
        if p.path == "/mod/url/view.php":
            modurls.add(abs_url)

    return activities, modurls


# ============================================================
#  STEP 2: EXTERNALS
# ============================================================

def resolve_external_from_modurl(modurl, cookies, base_host):
    # 1) Try redirects
    try:
        r = requests.get(modurl, cookies=cookies, allow_redirects=True, timeout=20)
        final = (r.url or "").split("#", 1)[0]
        if urlparse(final).netloc and urlparse(final).netloc != base_host:
            return final
    except Exception:
        pass

    # 2) If no redirect, parse HTML and look for external link in main content
    try:
        html = fetch_html(modurl, cookies)
        soup = BeautifulSoup(html, "html.parser")
        main = soup.select_one("#region-main") or soup

        for a in main.find_all("a", href=True):
            abs2 = urljoin(modurl, a["href"])
            p2 = urlparse(abs2)
            if p2.scheme in ("http", "https") and p2.netloc and p2.netloc != base_host:
                return abs2.split("#", 1)[0]
    except Exception:
        pass

    return None



def extract_external_from_activity(activity_url, cookies, base_host):
    externals = set()
    html = fetch_html(activity_url, cookies)
    soup = BeautifulSoup(html, "html.parser")

    main = soup.select_one("#region-main") or soup

    for a in main.find_all("a", href=True):
        abs2 = urljoin(activity_url, a["href"])
        p = urlparse(abs2)
        if p.scheme in ("http", "https") and p.netloc != base_host:
            externals.add(abs2)

    return externals


# ============================================================
#  SCRAPE COURSE
# ============================================================

def scrape_course(base, course_id, cookies):
    base_url = "https://%s" % base
    base_host = base

    seed_pages = [
        "%s/course/view.php?id=%s" % (base_url, course_id),
        "%s/course/resources.php?id=%s" % (base_url, course_id),
        "%s/mod/assign/index.php?id=%s" % (base_url, course_id),
    ]

    activities = set()
    modurls = set()
    externals = set()

    print("[+] Scanning course index pages")

    for p in seed_pages:
        html = fetch_html(p, cookies)
        hrefs = extract_hrefs(html)
        a, m = collect_activities(hrefs, base_url, base_host)
        activities.update(a)
        modurls.update(m)

    print("[+] Activities found:", len(activities))
    print("[+] URL activities found:", len(modurls))

    # SOLO: externas desde mod/url
    for mu in modurls:
        ext = resolve_external_from_modurl(mu, cookies, base_host)
        if ext:
            externals.add(ext)

    print("[+] External URLs from mod/url:", len(externals))

    return activities, externals



# ============================================================
#  SAVE
# ============================================================

def save_all(activities, externals, base, course_id):
    out = set()

    out.update(generar_urls_fijas_seb(base, course_id))

    for u in activities:
        p = seb_format(u)
        if p:
            out.add(p)

    for u in externals:
        p = seb_format(u)
        if p:
            out.add(p)

    name = "URLs_%s.txt" % course_id
    with open(name, "w") as f:
        for u in sorted(out):
            f.write(u + "\n")

    print("[+] Saved file:", name)
    print("[+] Total URLs written:", len(out))


# ============================================================
#  MAIN
# ============================================================

def main():
    base, course_id = parse_args()
    cookies = login_and_get_cookies(base, course_id)
    activities, externals = scrape_course(base, course_id, cookies)
    save_all(activities, externals, base, course_id)


if __name__ == "__main__":
    main()
