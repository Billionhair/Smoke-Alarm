from datetime import datetime

from agent import outreach


def test_run_sequence_idempotent(tmp_path):
    today = datetime(2024, 1, 1)
    lead = {
        "LeadID": "L1",
        "Name": "Bob",
        "Phone": "123",
        "Email": "bob@example.com",
        "CreatedAt": "2024-01-01T00:00:00",
    }
    activities = set()
    sent = []

    def sms(to, body):
        sent.append((to, body))

 codex/identify-repo-features-and-builds-016493
    actions = outreach.run_sequence("pm_trial", [lead], activities, send_sms=sms, today=today)
    assert actions == [("L1", "sms")]
    assert len(sent) == 1
    # Re-run should not duplicate
    actions = outreach.run_sequence("pm_trial", [lead], activities, send_sms=sms, today=today)

    actions = outreach.run_sequence(
        "pm_trial", [lead], activities, send_sms=sms, today=today
    )
    assert actions == [("L1", "sms")]
    assert len(sent) == 1
    # Re-run should not duplicate
    actions = outreach.run_sequence(
        "pm_trial", [lead], activities, send_sms=sms, today=today
    )
 main
    assert actions == []
