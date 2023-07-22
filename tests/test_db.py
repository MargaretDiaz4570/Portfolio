# test_db.py

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of all models,
        # we do not need to recursively bind dependencies
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close 
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close the connection to db
        test_db.close()

    def test_timeline_post(self):
        # Create timeline posts.
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        getFirstPost = TimelinePost.get_by_id(first_post.id)
        assert getFirstPost.name == 'John Doe'
        assert getFirstPost.email == 'john@example.com'
        assert getFirstPost.content == 'Hello world, I\'m John!'

        getSecondPost = TimelinePost.get_by_id(second_post.id)
        assert getSecondPost.name == 'Jane Doe'
        assert getSecondPost.email == 'jane@example.com'
        assert getSecondPost.content == 'Hello world, I\'m Jane!'