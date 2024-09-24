import os

import pytest


@pytest.fixture()
def assert_resource_reserved(product):
    def factory(resource_data):
        reservation_data = product.get_resource_status(resource_data)
        if os.getenv("TARGET_PRODUCT") == "example":
            assert reservation_data["is_reserved"]
        elif os.getenv("TARGET_PRODUCT") == "sample":
            assert reservation_data["is_reserved"]
            assert reservation_data["os_installation"] == "complete"

    return factory
