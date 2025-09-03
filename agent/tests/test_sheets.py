from agent.sheets import SheetDB

def test_format_address():
    data = {
        "AddressLine1": "1 Main St",
        "Suburb": "Springfield",
        "Postcode": "1234",
        "State": "NSW",
    }
    assert SheetDB.format_address(data) == "1 Main St, Springfield, 1234, NSW"
