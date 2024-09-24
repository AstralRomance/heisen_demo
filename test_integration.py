import pytest


@pytest.mark.parametrize("target_vendor", ["Tyan", "Fujitsu", "Dell"])
@pytest.mark.parametrize("drives_type", ["HDD", "SSD"])
def test_reservation_create(
    product, target_vendor, create_reservation_config, create_reservation, drives_type
):
    reservation_config = create_reservation_config(target_vendor, drives_type)
    reservation_data = create_reservation(reservation_config)
    assert reservation_data["reservation_id"]
    assert product.get_resource_status(reservation_config["server"]["model"])[
        "is_reserved"
    ]
