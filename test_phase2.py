import requests
import time
import sys

time.sleep(2)
BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

try:
    print("1. Testing login failure messaging...")
    login_data = {"username": "admin", "password": "wrongpassword"}
    r = session.post(f"{BASE_URL}/admin_login", data=login_data, allow_redirects=True)
    assert b"The password is not right." in r.content, f"Missing correct login failure message for admin. Got: {r.content}"
    
    collector_login_data = {"username": "nonexistent", "password": "wrongpassword"}
    r_col = session.post(f"{BASE_URL}/collector_login", data=collector_login_data, allow_redirects=True)
    assert b"The password is not right." in r_col.content, "Missing correct login failure message for collector"
    print("   -> Login failure messages validated.")

    print("2. Setting up collector account for testing...")
    # Login as admin to create collector
    session.post(f"{BASE_URL}/admin_login", data={"username": "admin", "password": "Admin@123!"})
    session.post(f"{BASE_URL}/admin/register_collector", data={"name": "Test Col", "username": "col2", "password": "Valid@123!"})
    session.get(f"{BASE_URL}/admin_logout")

    print("3. Testing Collector Change Password...")
    # Login as collector
    session.post(f"{BASE_URL}/collector_login", data={"username": "col2", "password": "Valid@123!"})
    
    # Test weak password format
    change_weak = {"current_password": "Valid@123!", "new_password": "weak"}
    r_weak = session.post(f"{BASE_URL}/collector/change_password", data=change_weak, allow_redirects=True)
    assert b"The password is not in the right format." in r_weak.content, "Missing format validation message"
    
    # Test wrong current password
    change_wrong = {"current_password": "Wrong@123!", "new_password": "ValidNew@123!"}
    r_wrong = session.post(f"{BASE_URL}/collector/change_password", data=change_wrong, allow_redirects=True)
    assert b"The password is not right." in r_wrong.content, "Missing wrong current password message"
    
    # Test valid change
    change_valid = {"current_password": "Valid@123!", "new_password": "ValidNew@123!"}
    r_valid = session.post(f"{BASE_URL}/collector/change_password", data=change_valid, allow_redirects=True)
    assert b"Password changed successfully!" in r_valid.content, "Missing success change password message"
    print("   -> Password change features validated.")

    print("ALL PHASE 2 TESTS PASSED.")

except Exception as e:
    print(f"TEST FAILED: {e}")
    sys.exit(1)
