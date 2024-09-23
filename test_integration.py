import pytest


@pytest.mark.parametrize(
    "test_record",
    [
        {"user": {"username": "some_user", "user_data": "some_data"}},
        {"message": {"user_id": 10, "message": "some message"}},
    ],
    ids=["user", "message"],
)
def test_simple_record_create(product, test_record):
    assert product.create_record(test_record).ok


def test_user_create():
    pass
