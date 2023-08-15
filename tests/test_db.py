import unittest
from unittest.mock import patch
from app import TimelinePost, initialize_database

class TestTimelinePost(unittest.TestCase):
    @patch('tests.test_db.initialize_database', return_value=None)
    def test_timeline_post(self, mock_initialize_database):
        # Simulate creating a TimelinePost instance
        post = TimelinePost(name="Test Title", email="test@example.com", content="Test Content")

        # Perform assertions to test the functionality
        self.assertEqual(post.name, "Test Title")
        self.assertEqual(post.email, "test@example.com")
        self.assertEqual(post.content, "Test Content")

if __name__ == '__main__':
    unittest.main()
