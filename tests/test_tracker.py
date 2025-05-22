import unittest
import unittest.mock
import json
import io
import os
import sys
import types
from contextlib import redirect_stdout
import importlib.machinery
import importlib.util

MODULE_PATH = os.path.join(os.path.dirname(__file__), '..', 'main - 2023-07-09T194426.036.py')


def load_tracker_module(fake_requests):
    with unittest.mock.patch.dict(sys.modules, {'requests': fake_requests}):
        loader = importlib.machinery.SourceFileLoader('tracker', MODULE_PATH)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
    return module


class TestGetAircraftLocation(unittest.TestCase):
    def test_extract_location(self):
        sample_data = {
            "ac": {
                "lat": 37.7749,
                "lon": -122.4194,
                "alt_baro": 1500
            }
        }

        def fake_get(url, headers=None):
            class Response:
                content = json.dumps(sample_data).encode('utf-8')
            return Response()

        fake_requests = types.SimpleNamespace(get=unittest.mock.Mock(side_effect=fake_get))

        tracker = load_tracker_module(fake_requests)
        fake_requests.get.reset_mock()

        buf = io.StringIO()
        with redirect_stdout(buf):
            tracker.get_aircraft_location('TESTTAIL')
        output = buf.getvalue()

        self.assertIn("Latitude: 37.7749", output)
        self.assertIn("Longitude: -122.4194", output)
        self.assertIn("Altitude: 1500 feet", output)


if __name__ == '__main__':
    unittest.main()
