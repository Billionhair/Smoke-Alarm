from agent.scrapers.rea import RealEstateAIScraper
from agent.scrapers.domain import DomainScraper
from agent.scrapers.maps import MapsScraper


def test_rea_parse():
    html = '<div data-name="Acme" data-phone="111"></div>'
    s = RealEstateAIScraper()
    res = s.parse(html)
    assert res == [{"name": "Acme", "phone": "111"}]


def test_domain_parse():
    html = '<li class="agency">Beta<span>222</span></li>'
    s = DomainScraper()
    res = s.parse(html)
    assert res == [{"name": "Beta", "phone": "222"}]


def test_maps_parse():
    data = {"results": [{"name": "Gamma", "phone": "333"}]}
    import json

    s = MapsScraper()
    res = s.parse(json.dumps(data))
    assert res == [{"name": "Gamma", "phone": "333"}]
