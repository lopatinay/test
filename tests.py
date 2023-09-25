import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from main import Scheduler


class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()

    @patch('main.datetime')
    def test_user_activity_runs_every_hour(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0)
        mock_task = Mock()

        self.scheduler.schedule(mock_task, datetime(2023, 1, 1, 12, 1), interval=timedelta(hours=1))

        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 1)
        self.scheduler.run()
        mock_task.assert_called_once()

    @patch('main.datetime')
    def test_software_update_runs_every_night(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 23, 59)
        mock_task = Mock()

        self.scheduler.schedule(mock_task, datetime(2023, 1, 2), interval=timedelta(days=1))

        mock_datetime.now.return_value = datetime(2023, 1, 2)
        self.scheduler.run()
        mock_task.assert_called_once()

    @patch('main.datetime')
    def test_alarm_runs_at_7_am(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 6, 59)
        mock_task = Mock()

        self.scheduler.schedule(mock_task, datetime(2023, 1, 1, 7, 0), interval=timedelta(days=1))

        mock_datetime.now.return_value = datetime(2023, 1, 1, 7, 0)
        self.scheduler.run()
        mock_task.assert_called_once()

    @patch('main.datetime')
    def test_non_recurring_task_is_removed(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0)
        mock_task = Mock()

        self.scheduler.schedule(mock_task, datetime(2023, 1, 1, 12, 1), is_recurring=False)

        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 1)
        self.scheduler.run()
        mock_task.assert_called_once()

        mock_task.reset_mock()
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 2)
        self.scheduler.run()
        mock_task.assert_not_called()


if __name__ == "__main__":
    unittest.main()
