import os


class StateAssertions:
    PRODUCTS_ASSERTIONS_MAPPING = {
        "resource_state": {
            "sample": "sample_resource_reserved",
            "example": "exmaple_resource_reserved",
        }
    }

    @classmethod
    def assert_resource_reserved(cls, reservation_data):
        target_assertion = getattr(
            cls,
            cls.PRODUCTS_ASSERTIONS_MAPPING["resource_state"].get(
                os.getenv("TARGET_PRODUCT")
            ),
        )
        return target_assertion(reservation_data)

    @classmethod
    def sample_resource_reserved(cls, reservation_data):
        assert reservation_data["is_reserved"]
        assert reservation_data["os_installation"] == "complete"

    @classmethod
    def exmaple_resource_reserved(cls, reservation_data):
        assert reservation_data["is_reserved"]
