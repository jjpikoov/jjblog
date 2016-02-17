import os
import main
import unittest
import tempfile


class JJblogTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = main.app.test_client()
        main.database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(main.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/admin', data=dict(
                    username=username,
                    password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/admin/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('aadmin', 'admin')
        # assert 'Failed' in rv.data
        print(rv.data)
        rv = self.logout()


if __name__ == '__main__':
    unittest.main()
