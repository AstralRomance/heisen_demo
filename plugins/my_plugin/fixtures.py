import os

import pytest

from plugins.my_plugin.wrappers import ExampleProduct, SampleProduct


@pytest.fixture(scope="session")
def product():
    if os.getenv("TARGET_PRODUCT") == "example":
        return ExampleProduct("https://www.example.com")
    elif os.getenv("TARGET_PRODUCT") == "sample":
        return SampleProduct("https://www.sample.com")
    else:
        raise ValueError(f"Unexpected product configured {os.getenv('TARGET_PRODUCT')}")


@pytest.fixture(scope="session")
def create_admin(product):
    return product.create_new_admin_user_session()
    