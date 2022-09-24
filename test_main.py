from fastapi.testclient import TestClient
from main import app
from database import *

client = TestClient(app)

"""
Test cases to validate endpoint get-contacts
"""

def test_wrong_types():

    response = client.get("/get-contacts/''/''")
    assert response.status_code == 422
    assert response.json() == \
           {'detail': "Search can only be done with ['phone', 'email', 'city', 'state', 'id', 'name']"}

    response = client.get("/get-contacts/''/1")
    assert response.status_code == 422
    assert response.json() == \
           {'detail': "Search can only be done with ['phone', 'email', 'city', 'state', 'id', 'name']"}

    response = client.get("/get-contacts/phoneemail/38545858")
    assert response.status_code == 422
    assert response.json() == \
           {'detail': "Search can only be done with ['phone', 'email', 'city', 'state', 'id', 'name']"}

def test_valid_type_empty_db():
    startDB(False)
    # TC for field validation

    response = client.get("/get-contacts/pHOne/sd")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/get-contacts/pHONE/38545858")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/get-contacts/phone/sd")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/get-contacts/phone/38545858")
    assert response.status_code == 200
    assert response.json() == []


def test_valid_type_one_result():
    startDB()

    response = client.get("/get-contacts/phone/38545858")
    assert response.status_code == 200
    assert response.json() == [{'id': 2, 'personDetails': {'firstName': 'AUGUSTO', 'lastName': 'PAULO',
                                                           'dateOfBirth': '1990-08-20'}, 'company': 'BOSCH',
                                'profileImage': 'https://assets.b9.com.br/wp-content/uploads/2014/08/bulbasaur.png',
                                'email': [{'type': 'PERSONAL', 'value': 'AUGUSTO@hotmail.com'}, {'type': 'WORK',
                                'value': 'AUGUSTO@lenovo.com'}], 'phoneNumber': [{'type': 'WORK', 'value': '38545858'}],
                                'address': [{'apartment': '0', 'street': 'Rua 1, 7', 'city': 'SUMARE', 'state': 'SP',
                                             'postalCode': '13179213', 'country': 'BRAZIL'}]}]

    response = client.get("/get-contacts/email/MARY@hotmail.com")
    assert response.status_code == 200
    assert response.json() == [{'id': 3, 'personDetails': {'firstName': 'MARY', 'lastName': 'SUE',
                              'dateOfBirth': '1990-07-03'}, 'company': 'GOOGLE',
                              'profileImage': 'https://www.pngmart.com/files/13/Pokemon-Charmander-Transparent-PNG.png',
                              'email': [{'type': 'PERSONAL', 'value': 'MARY@hotmail.com'}], 'phoneNumber':
                              [{'type': 'PERSONAL', 'value': '12345678'}], 'address': [{'apartment': '0',
                              'street': 'Rua 1, 9', 'city': 'SUMARE', 'state': 'SP', 'postalCode': '13179213',
                              'country': 'BRAZIL'}]}]

def test_valid_type_more_than_one_result():
    startDB()

    response = client.get("/get-contacts/city/Sumare")
    assert response.status_code == 200
    assert response.json() == \
        [
          {
            "id": 2,
            "personDetails": {
              "firstName": "AUGUSTO",
              "lastName": "PAULO",
              "dateOfBirth": "1990-08-20"
            },
            "company": "BOSCH",
            "profileImage": "https://assets.b9.com.br/wp-content/uploads/2014/08/bulbasaur.png",
            "email": [
              {
                "type": "PERSONAL",
                "value": "AUGUSTO@hotmail.com"
              },
              {
                "type": "WORK",
                "value": "AUGUSTO@lenovo.com"
              }
            ],
            "phoneNumber": [
              {
                "type": "WORK",
                "value": "38545858"
              }
            ],
            "address": [
              {
                "apartment": "0",
                "street": "Rua 1, 7",
                "city": "SUMARE",
                "state": "SP",
                "postalCode": "13179213",
                "country": "BRAZIL"
              }
            ]
          },
          {
            "id": 3,
            "personDetails": {
              "firstName": "MARY",
              "lastName": "SUE",
              "dateOfBirth": "1990-07-03"
            },
            "company": "GOOGLE",
            "profileImage": "https://www.pngmart.com/files/13/Pokemon-Charmander-Transparent-PNG.png",
            "email": [
              {
                "type": "PERSONAL",
                "value": "MARY@hotmail.com"
              }
            ],
            "phoneNumber": [
              {
                "type": "PERSONAL",
                "value": "12345678"
              }
            ],
            "address": [
              {
                "apartment": "0",
                "street": "Rua 1, 9",
                "city": "SUMARE",
                "state": "SP",
                "postalCode": "13179213",
                "country": "BRAZIL"
              }
            ]
          },
          {
            "id": 1,
            "personDetails": {
              "firstName": "PEDRO",
              "lastName": "VICENTE",
              "dateOfBirth": "1993-09-21"
            },
            "company": "ELDORADO",
            "profileImage": "https://4.bp.blogspot.com/-cebXJ9RB6r8/UPCCOoQHf0I/AAAAAAAAAyQ/fnM9_IbeW3U/s1600/pikachu_by_caridea-d3i4jd5.png",
            "email": [
              {
                "type": "PERSONAL",
                "value": "PEDROV@hotmail.com"
              },
              {
                "type": "WORK",
                "value": "PEDROV@lenovo.com"
              }
            ],
            "phoneNumber": [
              {
                "type": "PERSONAL",
                "value": "989230310"
              }
            ],
            "address": [
              {
                "apartment": "0",
                "street": "Rua 1, 2",
                "city": "SUMARE",
                "state": "SP",
                "postalCode": "13179213",
                "country": "BRAZIL"
              }
            ]
          }
        ]

    def test_valid_type_no_contacts_found():
        startDB()

        response = client.get("/get-contacts/city/Itu")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_contacts_empty_db():
        startDB(False)

        response = client.get("/get-contacts/all")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_contacts_non_empty_db():
        startDB()

        response = client.get("/get-contacts/all")
        assert response.status_code == 200