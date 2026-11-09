from src.models import Apartment
from src.manager import Manager
from src.models import Parameters, Tenant


def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key


def test_integration_tenants_loaded_in_manager():
    
    parameters = Parameters()
    manager = Manager(parameters)
    
    assert isinstance(manager.tenants, dict)
    assert len(manager.tenants) > 0, "Brak najemców w managerze lub plik JSON jest pusty"
   
    expected_tenants_dict = Tenant.from_json_file(parameters.tenants_json_path)
    
    for tenant_key, expected_tenant in expected_tenants_dict.items():
        assert tenant_key in manager.tenants, f"Najemca o kluczu {tenant_key} nie został znaleziony w managerze!"
        
        manager_tenant = manager.tenants[tenant_key]
        
        assert manager_tenant.name == expected_tenant.name, (
            f"Imię najemcy {manager_tenant.name} nie zgadza się z oczekiwanym {expected_tenant.name}"
        )



def test_integration_tenants_have_existing_apartments():
   
    parameters = Parameters()
    manager = Manager(parameters)
    
    
    for tenant_key, tenant in manager.tenants.items():
        assert tenant.apartment in manager.apartments, (
            f"Najemca {tenant.name} wskazuje na nieistniejące mieszkanie: {tenant.apartment}"
        )
    
    if manager.tenants:
        first_tenant_key = list(manager.tenants.keys())[0]
        tenant = manager.tenants[first_tenant_key]
        
        original_apartment = tenant.apartment
        
        try:
            tenant.apartment = "non-existent-apartment-key"
            assert tenant.apartment in manager.apartments, (
                f"Wykryto błędne/nieistniejące mieszkanie: {tenant.apartment}"
            )
        except AssertionError:
            pass
        finally:
            tenant.apartment = original_apartment