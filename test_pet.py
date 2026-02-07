from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, is_

def test_pet_schema():
    test_endpoint = "/pets/1"
    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200
    validate(instance=response.json(), schema=schemas.pet)


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {"status": status}

    response = api_helpers.get_api_data(test_endpoint, params)

    assert response.status_code == 200

    for pet in response.json():
        assert_that(pet["status"], is_(status))
        validate(instance=pet, schema=schemas.pet)


@pytest.mark.parametrize("pet_id", [999, -1, 10000])
def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"
    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404
