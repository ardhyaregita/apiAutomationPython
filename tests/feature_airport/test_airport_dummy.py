import requests
import pytest
from assertpy import assert_that

BASE_URL = "https://airportgap.com/api"

# 1. Fixture untuk Login (Hanya jalan 1x)
@pytest.fixture(scope="session")
def auth_token():
    payload = {
        "email": "yourbestie@yopmail.com", 
        "password": "Pass123@"
    }
    
    print("\n[DEBUG] Menjalankan Fixture: Login untuk ambil token...")
    response = requests.post(f"{BASE_URL}/tokens", data=payload)
    
    assert response.status_code == 200, f"Login Gagal! Detail: {response.text}"
    
    token = response.json().get("token")
    print(f"[DEBUG] Token didapat: {token[:10]}...") 
    return token

# 2. Test Case 1: Cek profil user (Contoh endpoint yang butuh token)
def test_get_user_favorites(auth_token):
    headers = {"Authorization": f"Token {auth_token}"}
    
    print("[DEBUG] Menjalankan Test: Get Favorites...")
    response = requests.get(f"{BASE_URL}/favorites", headers=headers)
    
    # Kita validasi status code-nya
    assert response.status_code == 200
    
    data = response.json().get("data")
    print(f"[DEBUG] Jumlah favorit: {len(data)}")
    assert isinstance(data, list)

# 3. Test Case 2: Cek detail airport (Tanpa token juga bisa, tapi kita tes koneksi)
def test_get_airport_detail():
    response = requests.get(f"{BASE_URL}/airports/KIX")
    assert response.status_code == 200
    assert_that(response.json()["data"]["id"]).is_equal_to("KIX")

