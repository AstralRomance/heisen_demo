import pytest
import os

# Default pytest_plugins declaration
pytest_plugins = (
    "plugins.my_plugin.fixtures",
    "plugins.my_plugin.assertions.fixtures",
)

# Partial pytest_plugins functionality enabled
# pytest_plugins = ("plugins.my_plugin.sample",)

# This thig also works with correct config for some reason
# pytest_plugins = ("plugins.my_plugin.sample", "plugins.my_plugin.fixtures", "plugins.my_plugin.assertions.fixtures", )


def pytest_runtest_teardown(item):
    print(f"pytest runtest teardown from tests scope {os.getenv('TARGET_PRODUCT')}")
