#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# ============================================================
#  RESOLUCIÓN DE SALTOS (EXTERNAS)
# ============================================================

def resolver_url_final(url_moodle, cookies):
    """Entra en Moodle y persigue el enlace hasta la web externa."""
    try:
        r = requests.get(url_moodle, cookies=cookies, timeout=10, allow_redirects=True)
        if "uma.es" not in r.url:
            return r.url
        soup = BeautifulSoup(r.text, "html.parser")
        link_respaldo = soup.select_one(".urlworkaround a") or soup.select_one("#region-main a")
        if link_respaldo and link_respaldo.has_attr('href'):
            return link_respaldo['href']
        return r.url
    except:
        return url_moodle

# ============================================================
#  ESCANEADOR
# ============================================================

def ejecutar_escaneo(subdominio, course_id):
    base_host = f"{subdominio}.cv.uma.es"
    main_url = f"https://{base_host}/course/view.php?id={course_id}"

    driver = webdriver.Firefox()
    driver.get(main_url)
    print(f"\n[*] Navegador en: {main_url}")
    input(">>> LOGUEATE Y PULSA ENTER CUANDO VEAS LAS PESTAÑAS DEL CURSO <<<\n")

    jar = requests.cookies.RequestsCookieJar()
    for c in driver.get_cookies():
        jar.set(c["name"], c["value"], domain=c.get("domain") or base_host)

    tabs = driver.find_elements(By.CSS_SELECTOR, "a[href*='section=']")
    tab_urls = list(set([t.get_attribute("href") for t in tabs]))
    tab_urls.append(main_url)

    urls_encontradas = set()
    basura = ['edit', 'delete', 'sesskey', 'admin', 'move', 'hide', 'duplicate']

    for url in tab_urls:
        print(f"[*] Escaneando sección: {url}")
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        container = soup.select_one(".course-content") or soup.select_one(".content")
        
        if container:
            for a in container.find_all("a", href=True):
                href = urljoin(url, a['href'])
                
                if any(x in href for x in basura) or href.startswith("#"):
                    continue

                # SI ES UN RECURSO TIPO URL -> GUARDAMOS EL SALTO Y LA EXTERNA
                if "/mod/url/view.php" in href:
                    print(f"    [>] Recurso URL detectado: {href}")
                    # 1. Guardamos la de Moodle (el salto)
                    urls_encontradas.add(href)
                    
                    # 2. Investigamos y guardamos la de destino (la externa)
                    final = resolver_url_final(href, jar)
                    if final != href:
                        print(f"        [+] Destino resuelto: {final}")
                        urls_encontradas.add(final)
                
                # RECURSOS INTERNOS (PDF, Tareas, etc.)
                elif any(x in href for x in ["/mod/resource/", "/mod/folder/", "/mod/assign/"]):
                    urls_encontradas.add(href)
                
                # ENLACES EXTERNOS DIRECTOS
                elif "uma.es" not in href and len(href) > 10:
                    urls_encontradas.add(href)

    driver.quit()
    return urls_encontradas

# ============================================================
#  FORMATEO Y GUARDADO
# ============================================================

def main():
    if len(sys.argv) < 3: return
    sub = sys.argv[1].lower()
    c_id = sys.argv[2]
    base = f"{sub}.cv.uma.es"

    urls_raw = ejecutar_escaneo(sub, c_id)

    final_rules = {
        f"*://{base}/pluginfile.php/*",
        f"*://{base}/course/view.php?id={c_id}*",
        f"*://{base}/mod/assign/view.php* "
    }

    for u in urls_raw:
        u_clean = u.split("#")[0]
        p = urlparse(u_clean)
        
        if p.netloc:
            regla = f"*://{p.netloc}{p.path}"
            if p.query:
                regla += f"?{p.query}"
            
            if not regla.endswith("*"):
                regla += "*"
            
            final_rules.add(regla)

    with open(f"URLs_{c_id}.txt", "w", encoding="utf-8") as f:
        for r in sorted(list(final_rules)):
            f.write(r + "\n")

    print(f"\n[OK] Archivo generado: URLS_TODO_{c_id}.txt")
    print(f"[*] Ahora tienes tanto los enlaces /mod/url/ como las externas finales.")

if __name__ == "__main__":
    main()
