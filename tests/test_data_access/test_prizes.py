from unittest.mock import Mock, patch
from unittest import TestCase

from zeton.data_access import prizes


class TestPrizes(TestCase):

    @patch('zeton.data_access.prizes.get_db')
    def test_get_prizes(self, mock_get_db):
        expected_query = "SELECT * FROM prizes WHERE user_id = ? AND is_active = 1 ORDER BY points"

        db_mock = Mock()
        mock_get_db.return_value = db_mock
        prizes.get_prizes(child_id=1)

        db_mock.execute.assert_called_with(expected_query, (1,))

    @patch('zeton.data_access.prizes.get_db')
    def test_create_prize(self, mock_get_db):
        expected_query = "INSERT INTO prizes (user_id, name, points, max_day, max_week, max_month, is_active) " \
                         "VALUES (?, ?, ?, ?, ?, ?, ?)"

        db_mock = Mock()
        cursor_mock = Mock()
        db_mock.cursor.return_value = cursor_mock
        mock_get_db.return_value = db_mock
        prizes.create_prize(user_id=1, name='test-name', points='2', max_day=3, max_week=4, max_month=5, is_active=1)

        cursor_mock.execute.assert_called_with(expected_query, (1, 'test-name', '2', 3, 4, 5, 1))
        db_mock.commit.assert_called_once()
