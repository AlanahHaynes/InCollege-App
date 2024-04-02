import unittest
from unittest.mock import patch
from epic8 import UserAccount, InCollegeAccts

class TestReminderMessage(unittest.TestCase):

    def setUp(self):
        self.app = InCollegeAccts()
        UserAccount.set_in_college_app(self.app)

    @patch('builtins.print')
    def test_reminder_message_generation(self, mock_print):
        # Create a user who hasn't applied for a job in the past 7 days
        user = UserAccount("test_user", "Password123!", "Test", "User", membership_type="Standard")
        user.create_job_application_history([
            {"job_title": "Software Developer", "date_applied": "2022-01-01"},
            {"job_title": "Data Analyst", "date_applied": "2022-01-05"}
        ])

        # Set the last job application date to more than 7 days ago
        # Simulate the user logging in
        user.last_login_date = "2022-01-10"

        # Call the method that generates the reminder message
        self.app.generateReminderMessage(user)

        # Check if the system printed the expected reminder message
        mock_print.assert_called_with("Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")

if __name__ == '__main__':
    unittest.main()