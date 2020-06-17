import json
from unittest import TestCase as _TestCase


class TestCase(_TestCase):
    def assertJsonTypes(self, data):
        self.assertEqual(data, json.loads(json.dumps(data)))
