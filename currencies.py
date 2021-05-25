#!/bin/python

import sys
import json
import urllib3
import re


def re_test(regex, string):
    return bool(re.fullmatch(regex, string))


def colorize(text, color):
    """
    Function wraps text in polybar colored format.
    Color is expected in hex form.
    """
    if not re_test(r"\#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})", color):
        raise ValueError("Invalid color")
    return "%{F" + color + "}" + text + "%{F-}"

def format_currency(cur):
    val = float(cur["Value"])
    prev = float(cur["Previous"])
    code = cur["CharCode"]
    res = f"{code}: {val}"
    change = colorize(" +%.4f" % abs(val-prev), "#009966") \
        if val > prev else colorize(" -%.4f" % abs(val-prev), "#C90000")
    return f"{res} {change}"


try:
    country = "Russia"
    if len(sys.argv) > 1:
        country = sys.argv[1]

    url =  f"https://www.cbr-xml-daily.ru/daily_json.js"

    CURRENCIES = ["USD", "EUR", "GBP"]

    http = urllib3.PoolManager()

    data = json.loads(str(http.request('GET', url).data, "utf8"))

    print(" | ".join([format_currency(data["Valute"][v]) for v in CURRENCIES]))

except Exception as e:
    print("Cannot get currencies info: %s" % str(e))
