import datetime

from unittest.mock import Mock, patch, ANY
from unittest import TestCase

from zeton.data_access import bans
from zeton.data_access.bans import calculate_end_time_warn


class TestBans(TestCase):
    test_date = datetime.datetime(2019, 10, 25, 10, 10)

    @patch('zeton.data_access.bans.get_db')
    def test_insert_default_ban(self, mock_get_db):
        expected_query = "INSERT INTO  'bans_name' VALUES (NULL, ?, ?, ?)"

        db_mock = Mock()
        mock_get_db.return_value = db_mock
        bans.insert_default_ban(1, 2, 3)
        db_mock.execute.assert_called_with(expected_query, (1, 2, 3))
        db_mock.commit.assert_called_once()

    @patch('zeton.data_access.bans.get_db')
    def test_count_all_default_bans(self, mock_get_db):
        db_mock = Mock()
        mock_get_db.return_value = db_mock
        bans.insert_all_default_bans(1)
        self.assertEqual(db_mock.commit.call_count, 6)

    @patch('zeton.data_access.bans.get_db')
    def test_update_warn_per_ban_id(self, mock_get_db):
        expected_query = 'UPDATE bans SET  start_timestamp =  ?, end_timestamp = ? WHERE child_id = ? AND ban_id = ?'

        db_mock = Mock()
        mock_get_db.return_value = db_mock
        bans.update_warn_per_ban_id(1, 2)
        db_mock.execute.assert_called_with(expected_query, (ANY, ANY, 1, 2))

    @patch('zeton.data_access.bans.get_db')
    def test_add_warn_per_ban_id(self, mock_get_db):
        expected_query = 'INSERT INTO bans VALUES (NULL, ?, ?, ?, ?)'

        db_mock = Mock()
        mock_get_db.return_value = db_mock
        bans.add_warn_per_ban_id(1, 2)
        db_mock.execute.assert_called_with(expected_query, (1, 2, ANY, ANY))

    def test_set_to_midnight(self):
        self.assertEqual(bans.set_to_midnight(self.test_date), datetime.datetime(2019, 10, 25, 0, 0))

    def test_calculate_end_time_warn(self):
        low_ban_id = 3
        mid_ban_id = 4
        high_ban_id = 6

        self.assertEqual(calculate_end_time_warn(self.test_date, low_ban_id), '2019-10-26T00:00:00')
        self.assertEqual(calculate_end_time_warn(self.test_date, mid_ban_id), '2019-10-25T10:40:00')
        self.assertEqual(calculate_end_time_warn(self.test_date, high_ban_id), '2019-10-26T10:10:00')
