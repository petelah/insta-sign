import json
import os
import unittest

from src import create_app, db


class TestSuite(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        if os.environ.get("FLASK_ENV") != "testing":
            raise EnvironmentError("FLASK_ENV not equal to 'testing'")

        db.create_all()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        try:
            os.remove('../testdb.db')
        except Exception as e:
            print(e)
            print("Test db unable to be deleted, please delete manually.")

    def test_login(self):
        # successful login
        response = self.client.post(
            '/api/auth/login',
            json={
                    "email": "test0@test.com",
                    "password": self.app.config['TEST_PASSWORD']
                },
            headers={"Content-Type": "application/json"}
        )

        print(response.get_json())

        self.assertEqual(response.status_code, 200)
