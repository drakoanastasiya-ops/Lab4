import pytest
from pydantic import ValidationError
from src.models import Apartment, Tenant, Room


def test_apartment_fields():
    data = Apartment(
        key="apart-test",
        name="Test Apartment",
        location="Test Location",
        area_m2=50.0,
        rooms={
            "room-1": Room(name="Living Room", area_m2=30.0),
            "room-2": Room(name="Bedroom", area_m2=20.0)
        }
    )
    assert data.key == "apart-test"
    assert data.name == "Test Apartment"
    assert data.location == "Test Location"
    assert data.area_m2 == 50.0
    assert len(data.rooms) == 2


def test_apartment_from_dict():
    data = {
        "key": "apart-test",
        "name": "Test Apartment",
        "location": "Test Location",
        "area_m2": 50.0,
        "rooms": {
            "room-1": {"name": "Living Room", "area_m2": 30.0},
            "room-2": {"name": "Bedroom", "area_m2": 20.0}
        }
    }
    apartment = Apartment(**data)
    assert apartment.key == data["key"]
    assert apartment.name == data["name"]
    assert apartment.location == data["location"]
    assert apartment.area_m2 == data["area_m2"]
    assert len(apartment.rooms) == len(data["rooms"])


def test_tenant_direct_creation():
    """a) Test sprawdzający bezpośrednie tworzenie obiektu Tenant (co najmniej 6 asercji)"""
    tenant = Tenant(
        name="Jan Kowalski",
        apartment="apart-test",
        room="room-1",
        rent_pln=1500.0,
        deposit_pln=1500.0,
        date_agreement_from="2026-01-01",
        date_agreement_to="2026-12-31"
    )
    
    assert tenant.name == "Jan Kowalski"
    assert tenant.apartment == "apart-test"
    assert tenant.room == "room-1"
    assert tenant.rent_pln == 1500.0
    assert tenant.deposit_pln == 1500.0
    assert tenant.date_agreement_from == "2026-01-01"


def test_tenant_from_dict_and_validation():
    """b) Test sprawdzający tworzenie obiektu Tenant ze słownika (co najmniej 4 asercje w tym jedna sprawdzająca, że pojawia się błąd walidacji)"""
    tenant_data = {
        "name": "Anna Nowak",
        "apartment": "apart-test",
        "room": "room-2",
        "rent_pln": 1200.0,
        "deposit_pln": 1200.0,
        "date_agreement_from": "2026-02-01",
        "date_agreement_to": "2027-02-01"
    }
    
    tenant = Tenant(**tenant_data)
    
    assert tenant.name == tenant_data["name"]
    assert tenant.apartment == tenant_data["apartment"]
    assert tenant.room == tenant_data["room"]
    assert tenant.rent_pln == tenant_data["rent_pln"]
    
    invalid_data = {
        "name": "Invalid Tenant"
    }
    
    with pytest.raises(ValidationError):
        Tenant(**invalid_data)