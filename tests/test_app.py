import unittest
import os
from flask import Flask, jsonify
from peewee import SqliteDatabase

os.environ['TESTING'] = 'true'

from app import app, initialize_database, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.db = SqliteDatabase(':memory:')
        self.db.connect()
        self.db.create_tables([TimelinePost], safe=True)
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.db.drop_tables([TimelinePost])
        self.db.close()
        self.app_context.pop()

    def test_post_timeline_post(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test post'
        }

        response = self.client.post('/api/timeline_post', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue('name' in response_data)
        self.assertTrue('email' in response_data)
        self.assertTrue('content' in response_data)
        self.assertTrue('created_at' in response_data)

    def test_get_timeline_post(self):
        response = self.client.get('/api/timeline_post')
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue('timeline_posts' in response_data)
        self.assertIsInstance(response_data['timeline_posts'], list)

    def test_delete_timeline_post(self):
        post = TimelinePost.create(name='Test User', email='test@example.com', content='Test content')

        response = self.client.delete(f'/api/timeline_post?post_id={post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Timeline post deleted successfully')

if __name__ == '__main__':
    unittest.main()
