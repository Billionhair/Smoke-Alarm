from agent import stripe_sync


class FakeDB:
    def __init__(self):
        self.rows = {"Invoices": [{"InvoiceID": "INV1", "Status": "Sent", "PaidAt": ""}]}

    def find_row(self, sheet, column, value):
        for idx, row in enumerate(self.rows[sheet], start=2):
            if row[column] == value:
                return idx, row
        return None, None

    def update_row(self, sheet, idx, row):
        self.rows[sheet][idx - 2] = row


def test_update_invoice_status():
    db = FakeDB()
    stripe_sync.update_invoice_status(db, "INV1", paid=True)
    row = db.rows["Invoices"][0]
    assert row["Status"] == "Paid"
    assert row["PaidAt"]
