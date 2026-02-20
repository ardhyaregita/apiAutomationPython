import requests

import json

def test_get_all_airports():

    url = "https://airportgap.com/api/airports"

    response = requests.get(url)
    data = response.json().get('data')

    elapsed = response.elapsed.total_seconds()

    print("\n=== ELAPSED TIME ===")
    print(elapsed)

    print("\n=== HEADERS ===")
    for k, v in response.headers.items():
        print(f"{k}: {v}")

    print("\n=== RESPONSE BODY ===")
    pretty_response = json.dumps(response.json(), indent=2)
    print(pretty_response)

    
    assert response.status_code == 200
    assert elapsed < 2
    assert response.json != ""
     


