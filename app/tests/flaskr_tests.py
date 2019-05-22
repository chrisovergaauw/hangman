#!/usr/bin/env python

import unittest, os, re
from app import create_app, db


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'you-will-never-guess'
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False # just imagine this works :-)


class BasicTestCase(unittest.TestCase):

    app = create_app(TestConfig)

    def test_index_while_not_logged_in(self):
        tester = create_app().test_client(self)
        login(client=tester, username='hangman', password='3dhubs')
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)


def login(client, username, password):
    return client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/auth/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
