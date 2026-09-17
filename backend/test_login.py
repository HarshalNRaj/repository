import json
import urllib.request

url = "http://127.0.0.1:5000/api/auth/login"
data = json.dumps({"email": "demouser@example.com", "password": "Password@123"}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as resp:
        print("LOGIN STATUS:", resp.status)
        print("LOGIN RESPONSE:", resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("BODY:", e.read().decode("utf-8"))
