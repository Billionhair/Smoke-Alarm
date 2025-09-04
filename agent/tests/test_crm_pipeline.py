from agent.crm import pipeline


def test_score_and_advance_stage():
    lead = {"Email": "a@example.com", "Phone": "123", "Doors": "150", "Source": "Inbound"}
    score = pipeline.score_lead(lead)
    assert score >= 80
    pipeline.advance_stage(lead, "Contacted")
    assert lead["Stage"] == "Contacted"
    assert lead["LastActivityAt"]


def test_upsert_company_contact():
    lead = {"CompanyName": "Acme", "Email": "bob@acme.com"}
    companies = []
    contacts = []
    cid, pid = pipeline.upsert_company_contact(lead, companies, contacts)
    assert cid and pid
    # Idempotent
    cid2, pid2 = pipeline.upsert_company_contact(lead, companies, contacts)
    assert cid == cid2
    assert pid == pid2
    assert len(companies) == 1
    assert len(contacts) == 1
