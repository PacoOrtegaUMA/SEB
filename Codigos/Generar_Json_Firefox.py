#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os


OUTPUT_FILE = "policies.json"


# Politicas fijas: siempre activas
POLITICAS_FIJAS = {
    "ExtensionSettings": {
        "*": {
            "installation_mode": "blocked"
        }
    },
    "DisablePrivateBrowsing": True,
    "DisableFirefoxAccounts": True,
    "DisableDeveloperTools": True
}


def cargar_urls_txt(ruta):
    urls = []

    with open(ruta, "r") as f:
        for linea in f:
            linea = linea.strip()

            if not linea:
                continue

            urls.append(linea)

    return urls


def construir_base():
    return {
        "policies": POLITICAS_FIJAS.copy()
    }


def construir_json_whitelist(urls):
    data = construir_base()

    data["policies"]["WebsiteFilter"] = {
        "Block": ["<all_urls>"],
        "Exceptions": urls
    }

    return data


def construir_json_allow():
    # Permitir todo (pero sin extensiones)
    return construir_base()


def construir_json_block_all():
    data = construir_base()

    data["policies"]["WebsiteFilter"] = {
        "Block": ["<all_urls>"],
        "Exceptions": []
    }

    return data


def mostrar_uso():
    msg = (
        "Uso:\n"
        "  python3 Generar_Policies_Firefox.py <archivo_txt1> [archivo_txt2 ...]\n"
        "      -> Bloquea todo excepto las URLs listadas\n"
        "  python3 Generar_Policies_Firefox.py -allow\n"
        "      -> Permite todo Internet (sin extensiones)\n"
        "  python3 Generar_Policies_Firefox.py -block\n"
        "      -> Bloquea absolutamente todo\n"
    )

    sys.stderr.write(msg)
    sys.exit(1)


def guardar_json(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("[+] policies.json generado correctamente")


def main():

    if len(sys.argv) < 2:
        mostrar_uso()

    args = sys.argv[1:]

    modo_allow = False
    modo_block = False
    txt_files = []


    for arg in args:

        if arg == "-allow":
            modo_allow = True

        elif arg == "-block":
            modo_block = True

        else:
            txt_files.append(arg)


    if modo_allow and modo_block:
        sys.stderr.write("ERROR: No puedes usar -allow y -block a la vez\n")
        sys.exit(1)


    # 1) Whitelist desde TXT
    if txt_files:

        todas_las_urls = []
        vistas = set()

        for txt_file in txt_files:

            if not os.path.exists(txt_file):
                sys.stderr.write("ERROR: no existe %s\n" % txt_file)
                sys.exit(1)

            urls = cargar_urls_txt(txt_file)

            for url in urls:

                if url not in vistas:
                    vistas.add(url)
                    todas_las_urls.append(url)


        data = construir_json_whitelist(todas_las_urls)
        guardar_json(data)
        return


    # 2) Allow total
    if modo_allow:

        data = construir_json_allow()
        guardar_json(data)
        return


    # 3) Block total
    if modo_block:

        data = construir_json_block_all()
        guardar_json(data)
        return


    mostrar_uso()



if __name__ == "__main__":
    main()
