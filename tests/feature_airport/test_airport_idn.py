import requests

import json

def test_get_all_airports():
    
    url = "https://airportgap.com/api/airports"
    
    response = requests.get(url)
    data = response.json().get('data')
    
    elapsed = response.elapsed.total_seconds()
 
    assert response.status_code == 200
    assert elapsed < 10
    assert response.json != ""
    assert len(data) > 5
    assert response.json 

    first_item = data[0]

#    print(first_item)
    assert "id" in first_item
    assert "attributes" in first_item

#    for k, v in first_item.items():
#        print(k, type(v))

    assert isinstance(first_item["id"], str)
    assert isinstance(first_item["type"], str)
    assert isinstance(first_item["attributes"], dict)


def test_get_airports_by_id():

    url = "https://airportgap.com/api/airports/HAM"

    response = requests.get(url)

    data = response.json().get('data')
#    print(data)
 
    assert response.status_code == 200
    assert response.json != ""
    assert "id" in data
    assert data["id"] == "HAM"
    assert data["attributes"]["name"] == "Hamburg Airport"
    
    
def test_get_airports_by_id_notfound():

    url = "https://airportgap.com/api/airports/XXX"

    response = requests.get(url)

    data = response.json()
#    print(data)

    assert response.status_code == 404
    assert "errors" in data
    assert data["errors"][0]["title"] == "Not Found"
    
def test_get_airports_by_id_invalid():

    url = "https://airportgap.com/api/airports/123#"

    response = requests.get(url)

    data = response.json()
#    print(data)

    assert response.status_code == 404
    assert "errors" in data
    assert data["errors"][0]["title"] == "Not Found"

def test_get_airports_by_pagination():

    url = "https://airportgap.com/api/airports/?page=1"
    
    page = 1

    response = requests.get(url)

    data = response.json()
    links = response.json().get("links", {})

    assert response.status_code == 200
    assert len(data) < 30
#    print(links)
    assert links["self"] == f"https://airportgap.com/api/airports?page={page}"

    if links.get("prev") and "?page=" in links["prev"]:
        expected_next = f"https://airportgap.com/api/airports?page={page-1}"
        assert links["prev"] == expected_next
    else:
        assert links.get("prev") in [None,"https://airportgap.com/api/airports"]


    if links.get("next") and "?page=" in links["next"]:
        expected_next = f"https://airportgap.com/api/airports?page={page+1}"
        assert links["next"] == expected_next
    else:
        assert links.get("next") in [None,"https://airportgap.com/api/airports"]


def test_get_airports_by_pagination_invalid():

    url = "https://airportgap.com/api/airports/?page=ABC"

    response = requests.get(url)
    
    assert "text/html" in response.headers["Content-Type"]
    assert response.status_code == 404
    assert "The page you were looking for doesn't exist (404 Not found)" in response.text 


def test_get_airports_by_pagination_outofrange():

    url = "https://airportgap.com/api/airports/?page=999"
    response = requests.get(url)

    assert response.status_code in [200, 404]

    if response.status_code == 200:
        assert response.json()["data"] == []