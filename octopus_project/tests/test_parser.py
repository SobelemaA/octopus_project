import sys
import unittest
from unittest.mock import patch
import meter_stats

class TestMeterReadings(unittest.TestCase):

    # note: setup parser to run tests
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
    #
    # def test_parse_args(self):
    #     parser = meter_stats.parse_args(['meter_readings'])

    # def test_main(capsys):
    #     with patch('sys.argv', ['main', 'path', 'meter_readings']):
    #         meter_stats.main()

    def test_count_meters(self):
        result = meter_stats.count_meters([23, 53, 57, 96])
        self.assertEqual(result, 4)

    def test_total_valid_meters(self):
        result = meter_stats.total_valid_meter_readings(['V', 'F', 'F', 'V', 'V', 'V'])
        self.assertEqual(result, 4)

    def test_total_invalid_meters(self):
        result = meter_stats.total_invalid_meter_readings(['V', 'F', 'F', 'V', 'V', 'V'])
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()