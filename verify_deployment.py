import requests
import sys

BASE_URL = "http://localhost:8000"

def test_backend():
    print("Testing Backend...")
    try:
        # 1. Health Check
        r = requests.get(f"{BASE_URL}/")
        if r.status_code != 200:
            print(f"❌ Health check failed: {r.status_code}")
            return False
        print("✅ Health check passed")

        # 2. Register
        username = "test_user_123"
        password = "password123"
        r = requests.post(f"{BASE_URL}/auth/register", json={"username": username, "hashed_password": password})
        # 200 or 400 if already exists is fine for now
        if r.status_code not in [200, 400]:
            print(f"❌ Register failed: {r.status_code} - {r.text}")
            return False
        print("✅ Register passed")

        # 3. Login
        r = requests.post(f"{BASE_URL}/auth/token", data={"username": username, "password": password})
        if r.status_code != 200:
            print(f"❌ Login failed: {r.status_code} - {r.text}")
            return False
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login passed")

        # 4. Create Note
        r = requests.post(f"{BASE_URL}/notes/", json={"title": "Test Note", "content": "This is a test"}, headers=headers)
        if r.status_code != 200:
            print(f"❌ Create Note failed: {r.status_code} - {r.text}")
            return False
        note_id = r.json()["id"]
        print("✅ Create Note passed")

        # 5. Get Notes
        r = requests.get(f"{BASE_URL}/notes/", headers=headers)
        if r.status_code != 200:
            print(f"❌ Get Notes failed: {r.status_code}")
            return False
        print("✅ Get Notes passed")

        # 6. Delete Note
        r = requests.delete(f"{BASE_URL}/notes/{note_id}", headers=headers)
        if r.status_code != 200:
            print(f"❌ Delete Note failed: {r.status_code}")
            return False
        print("✅ Delete Note passed")
        
        print("🎉 All Backend Tests Passed!")
        return True

    except Exception as e:
        print(f"❌ Exception during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if not success:
        sys.exit(1)
