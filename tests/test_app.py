# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<title>MLH Fellow</title>' in html
        assert '<h2>Education</h2>' in html

    def test_timeline(self):
        getResponse = self.client.get('/api/timeline_post')
        assert getResponse.status_code == 200
        assert getResponse.is_json
        json = getResponse.get_json()
        assert 'timeline_posts' in json
        assert len(json['timeline_posts']) == 0

        # Send a post and check if the data returned by the api
        # is the data sent
        postResponse = self.client.post('/api/timeline_post', data={
            'name': 'Test testini',
            'email': 'test@gmail.com',
            'content': 'This is a test content'
        })
        assert postResponse.status_code == 200

        # Make another get petition and check if the post was
        # correctly added to the database
        getResponse = self.client.get('/api/timeline_post')
        json = getResponse.get_json()
        first_timeline_post = json['timeline_posts'][0]
        first_timeline_post['name'] = 'Test testini'
        first_timeline_post['email'] = 'test@gmail.com'
        first_timeline_post['content'] = 'This is a test content'

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post('/api/timeline_post', data={'email':'john@example.com', 'content':'Hello world, I\'m John!'})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid name' in html

        # POST request with empty content
        response = self.client.post('/api/timeline_post', data={'name': 'Pedrito', 'email':'john@example.com', 'content':''})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid content' in html

        # POST request with empty content
        response = self.client.post('/api/timeline_post', data={'name': 'Nelson Kanzela', 'email':'not-an-email', 'content':'Good'})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid email' in html