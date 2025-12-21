#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os
import plistlib
import re

def read_plist(path):
    # Works in Python 2 and 3
    if hasattr(plistlib, "readPlist"):
        return plistlib.readPlist(path)
    f = open(path, "rb")
    try:
        return plistlib.load(f)
    finally:
        f.close()

def write_plist(data, path):
    # Works in Python 2 and 3
    if hasattr(plistlib, "writePlist"):
        return plistlib.writePlist(data, path)
    f = open(path, "wb")
    try:
        plistlib.dump(data, f)
    finally:
        f.close()

def url_to_regex(url):
    """
    Convert a plain URL like
      https://mop.cv.uma.es/
    into a regex like
      ^https:\\/\\/mop\\.cv\\.uma\\.es\\/$
    """
    esc = re.escape(url)
    esc = esc.replace("/", "\\/")
    return "^" + esc + "$"

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py input.seb urls1.txt [urls2.txt ...]")
        sys.exit(1)

    # First arg is seb file, the rest are url list files
    seb_in_path = sys.argv[1]
    urls_paths = sys.argv[2:]

    base, ext = os.path.splitext(seb_in_path)
    seb_out_path = base + "URL" + ext

    # Read all url lists
    all_lines = []
    for urls_path in urls_paths:
        try:
            f = open(urls_path, "r")
            lines = f.read().splitlines()
            f.close()
        except IOError:
            print("Could not read urls file: " + urls_path)
            sys.exit(1)
        all_lines.extend(lines)

    rules = []
    seen = set()

    for line in all_lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue

        # If ends with *, keep as simple expression
        if line.endswith("*"):
            expr = line
            is_regex = False
        else:
            # No *, generate regex from URL
            expr = url_to_regex(line)
            is_regex = True

        key = (expr, is_regex)
        if key in seen:
            continue
        seen.add(key)

        rule = {
            "action": 1,        # 1 = allow
            "active": True,
            "expression": expr,
            "regex": is_regex
        }
        rules.append(rule)

    if not rules:
        print("No rules created, url lists are empty.")
        sys.exit(1)

    # Read seb plist
    try:
        data = read_plist(seb_in_path)
    except Exception:
        print("Could not read input seb file: " + seb_in_path)
        sys.exit(1)

    # Set url filter rules and enable filter
    data["URLFilterRules"] = rules
    data["URLFilterEnable"] = True
    # Compatibility key in some configs
    data["enableURLFilter"] = True

    # Write output seb
    try:
        write_plist(data, seb_out_path)
    except Exception:
        print("Could not write output SEB file: " + seb_out_path)
        sys.exit(1)

    print("Created: " + seb_out_path)

if __name__ == "__main__":
    main()
