import json
import urllib.request

url = "http://127.0.0.1:5000/api/auth/signup"
payload = {
    "name": "Demo User",
    "email": "demouser@example.com",
    "password": "Password@123",
    "phone": "9876543210",
    "role": "user"
}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as resp:
        print("SIGNUP STATUS:", resp.status)
        print("SIGNUP RESPONSE:", resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("BODY:", e.read().decode("utf-8"))
