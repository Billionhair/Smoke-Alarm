import unittest
from unittest.mock import patch
import requests

from agent.router import optimize_route, plan_multi_day_routes


class TestRouter(unittest.TestCase):
    @patch("agent.router.requests.get")
    def test_optimize_route_many_stops(self, mock_get):
        addresses = [
            "40.748817,-73.985428",
            "40.689247,-74.044502",
            "40.752726,-73.977229",
            "40.758896,-73.985130",
            "40.706086,-73.996864",
            "40.730610,-73.935242",
            "40.829643,-73.926175",
            "40.837049,-73.865433",
            "40.748441,-73.985664",
            "40.712776,-74.005974",
        ]
        mock_get.return_value.json.return_value = {
            "code": "Ok",
            "waypoints": [
                {"waypoint_index": i} for i in range(len(addresses))
            ],
            "trips": [{"distance": 1000, "duration": 600}],
        }
        mock_get.return_value.raise_for_status.return_value = None
        result = optimize_route(addresses)
        self.assertEqual(len(result.order), len(addresses))
        self.assertGreater(result.distance_km, 0)
        self.assertGreater(result.duration_min, 0)

    @patch("agent.router.requests.get")
    def test_optimize_route_http_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("boom")
        with self.assertRaises(RuntimeError):
            optimize_route(["1,2", "3,4"])

    def test_plan_multi_day_handles_cancellations(self):
        addresses = [
            "40.748817,-73.985428",
            "40.689247,-74.044502",
            "40.752726,-73.977229",
            "40.758896,-73.985130",
        ]
        responses = {
            "40.748817,-73.985428": True,
            "40.752726,-73.977229": True,
        }
        plan = plan_multi_day_routes(addresses, days=2, responses=responses)
        # two addresses should remain, each scheduled on a separate day
        self.assertEqual(sorted(plan.canceled), sorted([addresses[1], addresses[3]]))
        self.assertEqual(len(plan.daily), 2)
        self.assertEqual(plan.daily[1].order, [addresses[0]])
        self.assertEqual(plan.daily[2].order, [addresses[2]])


if __name__ == "__main__":
    unittest.main()

