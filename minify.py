import urllib, sys
from urllib.parse import urlencode
from http.client import HTTPConnection

print("Starting...")

with open("static/code.js", "r") as f:
    params = urlencode([
        ("js_code", f.read()),
        ("compilation_level", "SIMPLE_OPTIMIZATIONS"),
        ("output_format", "text"),
        ("output_info", "compiled_code"),
    ])

headers = { "Content-type": "application/x-www-form-urlencoded" }
conn = HTTPConnection("closure-compiler.appspot.com")
conn.request("POST", "/compile", params, headers)

response = conn.getresponse()
data = response.read().decode("utf-8")
with open("static/code.min.js", "w") as f:
    f.write(data)
conn.close()

print("Done")
