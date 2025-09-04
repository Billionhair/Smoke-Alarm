from agent.routing import planner


class DummyRes:
    def __init__(self, order, url):
        self.order = order
        self.url = url


def test_plan_route(monkeypatch):
    def fake_opt(addresses):
        return DummyRes(list(addresses), "http://gmaps")

    monkeypatch.setattr(planner, "optimize_route", fake_opt)
    res = planner.plan_route(["A", "B"])
    assert res["order"] == ["A", "B"]
    assert res["url"] == "http://gmaps"
