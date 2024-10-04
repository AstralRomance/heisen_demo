# heisen_demo
Demo repo for Heisenbug conf.
This is sample project for demonstrate some pytest plugins possibilities.

## Testing object
There is two products: "Sample" and "Example" products which provides access to some resources like servers, drives etc and some specific functions like OS installation. Counts that all operations performed using REST API, and it's mocked via requests_mock library.

# Setup:
Create python virtual environment and install requirements using `python3 -m pip install -r requirements.txt`
Also you must define environment variable TARGET_PRODUCT as "sample" or "example" to avoid value error: `export TARGET_PRODUCT=sample`

# Tests run:
All tests running with pytest, use following command to run all available tests
`python3 -m pytest . -v -s`

Use pytest marks to run specific tests like this
`python3 -m pytest . -v -s -m sample`

You can get all custom available marks in pytest.ini file
