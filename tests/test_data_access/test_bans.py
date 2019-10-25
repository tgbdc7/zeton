import pytest
import datetime
import unittest

from zeton.data_access import bans
from zeton.data_access.bans import calculate_end_time_warn


class TestBans(unittest.TestCase):
    test_date = datetime.datetime(2019, 10, 25, 10, 10)

    def test_set_to_midnight(self):
        self.assertEqual(bans.set_to_midnight(self.test_date), datetime.datetime(2019, 10, 25, 0, 0))

    def test_calculate_end_time_warn(self):
        low_ban_id = 3
        mid_ban_id = 4
        high_ban_id = 6

        self.assertEqual(calculate_end_time_warn(self.test_date, low_ban_id), '2019-10-26T00:00:00')
        self.assertEqual(calculate_end_time_warn(self.test_date, mid_ban_id), '2019-10-25T10:40:00')
        self.assertEqual(calculate_end_time_warn(self.test_date, high_ban_id), '2019-10-26T10:10:00')


if __name__ == '__main__':
    unittest.main()
