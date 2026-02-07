import pytest
import api_helpers
import schemas
from jsonschema import validate
from hamcrest import assert_that, is_

@pytest.fixture
def created_order():
    response = api_helpers.get_api_data(
        "/pets/findByStatus",
        {"status": "available"}
    )
    assert response.status_code == 200
    pets = response.json()
    assert len(pets) > 0

    pet_id = pets[0]["id"]

    payload = {"pet_id": pet_id}
    order_response = api_helpers.post_api_data("/store/order", payload)
    assert order_response.status_code == 201

    return order_response.json()




def test_patch_order_by_id(created_order):
    order_id = created_order["id"]

    patch_payload = {"status": "sold"}
    response = api_helpers.patch_api_data(
        f"/store/order/{order_id}",
        patch_payload
    )

    assert response.status_code == 200
    assert_that(
        response.json()["message"],
        is_("Order and pet status updated successfully")
    )


def test_patch_order_invalid_status(created_order):
    order_id = created_order["id"]

    patch_payload = {"status": "invalid_status"}
    response = api_helpers.patch_api_data(
        f"/store/order/{order_id}",
        patch_payload
    )

    assert response.status_code == 400
