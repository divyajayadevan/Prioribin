import requests
import time
import sys

# Give server time to start
time.sleep(2)

session = requests.Session()
BASE_URL = "http://127.0.0.1:5000"

try:
    print("1. Testing access control...")
    r = session.get(f"{BASE_URL}/admin", allow_redirects=False)
    assert r.status_code == 302, f"Expected 302, got {r.status_code}"
    assert "/admin_login" in r.headers['Location'], "Did not redirect to /admin_login"
    print("   -> Redirected to login successfully.")

    print("2. Testing login with default credentials...")
    login_data = {"username": "admin", "password": "Admin@123!"}
    r = session.post(f"{BASE_URL}/admin_login", data=login_data, allow_redirects=False)
    assert r.status_code == 302, "Login failed"
    assert "/admin" in r.headers['Location']
    # Follow redirect to establish session fully
    r = session.get(f"{BASE_URL}/admin")
    assert r.status_code == 200
    print("   -> Logged in successfully.")

    print("3. Testing password policy enforcement...")
    # Weak password
    register_data_weak = {
        "name": "Test Collector Weak",
        "username": "collector_weak",
        "password": "weakpassword"
    }
    r = session.post(f"{BASE_URL}/admin/register_collector", data=register_data_weak, allow_redirects=False)
    assert r.status_code == 302
    r_dash = session.get(f"{BASE_URL}/admin")
    assert b"Password policy error" in r_dash.content, "Weak password was not rejected"
    print("   -> Weak password rejected successfully.")

    # Strong password
    register_data_strong = {
        "name": "Test Collector Strong",
        "username": "collector_strong",
        "password": "Strong123!@#"
    }
    r = session.post(f"{BASE_URL}/admin/register_collector", data=register_data_strong, allow_redirects=False)
    assert r.status_code == 302
    r_dash = session.get(f"{BASE_URL}/admin")
    assert b"registered successfully" in r_dash.content, "Strong password was not accepted"
    print("   -> Strong password accepted successfully.")

    print("4. Testing logout...")
    r = session.get(f"{BASE_URL}/admin_logout", allow_redirects=False)
    assert r.status_code == 302
    assert "/" in r.headers['Location']
    r_admin = session.get(f"{BASE_URL}/admin", allow_redirects=False)
    assert r_admin.status_code == 302
    assert "/admin_login" in r_admin.headers['Location']
    print("   -> Logged out successfully.")

    print("ALL TESTS PASSED.")

except Exception as e:
    print(f"TEST FAILED: {e}")
    sys.exit(1)
