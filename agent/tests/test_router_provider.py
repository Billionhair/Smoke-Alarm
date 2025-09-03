import unittest
from unittest.mock import patch

from agent import router
from agent.router_providers import MapboxProvider, OSRMProvider
from agent.config import cfg

class TestRouterProvider(unittest.TestCase):
    def test_mapbox_selected(self):
        with (
            patch.object(cfg, "routing_provider", "mapbox"),
            patch.object(cfg, "mapbox_token", "x"),
            patch.object(
                MapboxProvider, "optimize", return_value=router.RouteResult([], 0, 0, "")
            ) as mock_opt,
        ):
            router.optimize_route(["a", "b"])
            mock_opt.assert_called_once()

    def test_default_osrm(self):
        with patch.object(cfg, "routing_provider", "osrm"), patch.object(
            OSRMProvider, "optimize", return_value=router.RouteResult([], 0, 0, "")
        ) as mock_opt:
            router.optimize_route(["a", "b"])
            mock_opt.assert_called_once()

if __name__ == "__main__":
    unittest.main()
