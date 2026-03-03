import requests

import json

from assertpy import assert_that

BASE_URL = "https://airportgap.com/api/"


def test_get_all_airports():
    
    response = requests.get(f'{BASE_URL}/airports')
    
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

    airportid = "HAM"

    response = requests.get(f'{BASE_URL}/airports/{airportid}')

    data = response.json().get('data')
#    print(data)
 
    assert response.status_code == 200
    assert response.json != ""
    assert "id" in data
    assert data["id"] == "HAM"
    assert data["attributes"]["name"] == "Hamburg Airport"
    
    
def test_get_airports_by_id_notfound():

    airportid = "XXX"

    response = requests.get(f'{BASE_URL}/airports/{airportid}')

    data = response.json()
#    print(data)

    assert response.status_code == 404
    assert "errors" in data
    assert data["errors"][0]["title"] == "Not Found"
    
def test_get_airports_by_id_invalid():

    airportid = "123@"

    response = requests.get(f'{BASE_URL}/airports/{airportid}')

    data = response.json()
#    print(data)

    assert response.status_code == 404
    assert "errors" in data
    assert data["errors"][0]["title"] == "Not Found"

def test_get_airports_by_pagination():

    page = "?page="
    pageNumber = 10

    response = requests.get(f'{BASE_URL}/airports/{page}{pageNumber}')

    data = response.json()
    links = response.json().get("links", {})

    assert response.status_code == 200
    assert len(data) < 30
#    print(links)
    assert links["self"] == f"https://airportgap.com/api/airports{page}{pageNumber}"

    if links.get("prev") and "?page=" in links["prev"]:
        expected_next = f"https://airportgap.com/api/airports{page}{pageNumber-1}"
        assert links["prev"] == expected_next
    else:
        assert links.get("prev") in [None,"https://airportgap.com/api/airports"]


    if links.get("next") and "?page=" in links["next"]:
        expected_next = f"https://airportgap.com/api/airports{page}{pageNumber+1}"
        assert links["next"] == expected_next
    else:
        assert links.get("next") in [None,"https://airportgap.com/api/airports"]


def test_get_airports_by_pagination_invalid():

    page = "?page=ABC"

    response = requests.get(f'{BASE_URL}/airports/{page}')
    
    assert "text/html" in response.headers["Content-Type"]
    assert response.status_code == 404
    assert "The page you were looking for doesn't exist (404 Not found)" in response.text 


def test_get_airports_by_pagination_outofrange():

    page = "?page=999"

    response = requests.get(f'{BASE_URL}/airports/{page}')

    assert response.status_code in [200, 404]

    if response.status_code == 200:
        assert response.json()["data"] == []

def test_calculate_distance():
    payload = {
        "from" : "YNA",
        "to" : "YOC"
    }

    response = requests.post(f'{BASE_URL}/airports/distance', data=payload)
    data = response.json().get("data")
    
    assert_that(data).is_type_of(dict)
    assert_that(data).has_id("YNA-YOC")
    assert_that(data["type"]).is_equal_to("airport_distance")
    assert_that(data["attributes"]).is_not_empty()
    assert_that(data["attributes"]["miles"]).is_equal_to(2794.8986339626285)

def test_calculate_distance_same_airport():
    payload = {
        "from" : "YNA",
        "to" : "YNA"
    }

    response = requests.post(f'{BASE_URL}/airports/distance', data=payload)
    data = response.json().get("data")
    
    assert_that(data).is_type_of(dict)
    assert_that(data).has_id("YNA-YNA")
    assert_that(data["type"]).is_equal_to("airport_distance")
    assert_that(data["attributes"]).is_not_empty()
    assert_that(data["attributes"]["miles"]).is_equal_to(0.0)

def test_calculate_distance_invalid_airport():
    payload = {
        "from" : "YNA",
        "to" : "XXX"
    }

    response = requests.post(f'{BASE_URL}/airports/distance', data=payload)
    data = response.json().get("errors")
    
    assert_that(data).is_type_of(list)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(data[0]["detail"]).is_equal_to("Please enter valid 'from' and 'to' airports.")


def test_calculate_distance_empty_airport():
    payload = {
        "from" : "YNA",
        "to" : ""
    }

    response = requests.post(f'{BASE_URL}/airports/distance', data=payload)
    data = response.json().get("errors")
    
    assert_that(data).is_type_of(list)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(data[0]["detail"]).is_equal_to("Please enter valid 'from' and 'to' airports.")

def test_calculate_distance_missing_param():
    payload = {
        "from" : "YNA",
        
    }

    response = requests.post(f'{BASE_URL}/airports/distance', data=payload)
    data = response.json().get("errors")
    

    assert_that(data).is_type_of(list)
    assert_that(response.status_code).is_equal_to(422)
    assert_that(data[0]["detail"]).is_equal_to("Please enter valid 'from' and 'to' airports.")




