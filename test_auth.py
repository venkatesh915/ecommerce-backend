import urllib.request
import urllib.error
import json

base_url = "http://127.0.0.1:8000"

def make_request(url, data=None, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')

print("Registering...")
status, text = make_request(f"{base_url}/auth/register", data={
    "email": "test@test.com",
    "password": "password123",
    "full_name": "Test User"
})
print(status, text)

print("Logging in...")
status, text = make_request(f"{base_url}/auth/login", data={
    "email": "test@test.com",
    "password": "password123"
})
print(status, text)

if status == 200:
    token = json.loads(text).get("access_token")
    print("Getting user profile...")
    status2, text2 = make_request(f"{base_url}/user/me", headers={"Authorization": f"Bearer {token}"})
    print(status2, text2)
