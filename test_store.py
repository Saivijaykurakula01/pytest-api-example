import api_helpers
from hamcrest import assert_that, is_

def test_patch_order_by_id():
    order_payload = {"pet_id": 0}
    create_response = api_helpers.post_api_data("/store/order", order_payload)

    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    patch_payload = {"status": "sold"}
    patch_response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)

    assert patch_response.status_code == 200
    assert_that(
        patch_response.json()["message"],
        is_("Order and pet status updated successfully")
    )
