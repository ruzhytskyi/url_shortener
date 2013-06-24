import os
from url_shortener import app, db
import unittest
import tempfile

class UrlShortenerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.db_fd, self.db_fn = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_fn 
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_fn)

    def test_shortener_page(self):
        resp = self.app.get('/shortener')
        assert 'Here will be your short url' in resp.data 
    
    def test_url_shortening(self):
        resp = self.app.post('/shortener',
                             data=dict(full_url='http://google.com'),
                             follow_redirects=True) 
        assert app.config['HOST'] in resp.data 

    def test_redirecting(self):
        resp = self.app.post('/shortener',
                             data=dict(full_url='http://google.com'),
                             follow_redirects=True) 

        assert app.config['HOST'] in resp.data
        form_start = resp.data.find('class="form-shortener"')
        url_end = resp.data.find('</a>', form_start) 
        url_start = resp.data.rfind('>', form_start, url_end) 
        short_url = resp.data[url_start+1:url_end]
        assert short_url != ''
        resp = self.app.get(short_url)
        assert 'http://google.com' in resp.data

    def test_sign_up(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "Logged in as 'user'" in resp.data
        assert "Statistics" in resp.data

    def test_sign_up_no_login(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "Please, provide your login" in resp.data
    
    def test_sign_up_no_password(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='',
                                       confirmation=''),
                             follow_redirects=True)
        assert "Please, provide your password" in resp.data
        assert "Please, repeat your password" in resp.data
   
    def test_sign_up_wrong_confirmation(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='s'),
                             follow_redirects=True)
        assert "Confirmation doesn&#39;t match password" in resp.data

    def test_sign_up_already_existing_user(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "Logged in as 'user'" in resp.data
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "User with login &#39;user&#39; already exists" in resp.data

    def test_login_logout(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "Logged in as 'user'" in resp.data
        assert "Statistics" in resp.data

        resp = self.app.get('/sign_out',
                            follow_redirects=True)
        assert "Logged in as 'user'" not in resp.data
        assert "Statistics" not in resp.data
    
        resp = self.app.post('/sign_in',
                             data=dict(login='user',
                                       password='pass'),
                             follow_redirects=True)
        assert "Logged in as 'user'" in resp.data
        assert "Statistics" in resp.data

    def test_login_user_not_registered(self):
        resp = self.app.post('/sign_in',
                             data=dict(login='user_nr',
                                       password='pass'),
                             follow_redirects=True)
        assert "User with login &#39;user_nr&#39; doesn&#39;t exist" in resp.data

    def test_login_wrong_password(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "Logged in as 'user'" in resp.data

        resp = self.app.get('/sign_out',
                            follow_redirects=True)
        assert "Logged in as 'user'" not in resp.data
        assert "Statistics" not in resp.data

        resp = self.app.post('/sign_in',
                             data=dict(login='user',
                                       password='s'),
                             follow_redirects=True)
        assert "Wrong password" in resp.data


    def test_login_user_field_empty(self):
        resp = self.app.post('/sign_in',
                             data=dict(login='',
                                       password='pass'),
                             follow_redirects=True)
        assert "Please, provide your login" in resp.data

    def test_statistics_page(self):
        resp = self.app.post('/sign_up',
                             data=dict(login='user',
                                       password='pass',
                                       confirmation='pass'),
                             follow_redirects=True)
        assert "Logged in as 'user'" in resp.data

        resp = self.app.post('/shortener',
                             data=dict(full_url='http://google.com'),
                             follow_redirects=True) 

        assert app.config['HOST'] in resp.data
        form_start = resp.data.find('class="form-shortener"')
        url_end = resp.data.find('</a>', form_start) 
        url_start = resp.data.rfind('>', form_start, url_end) 
        short_url = resp.data[url_start+1:url_end]
        assert short_url != ''
        resp = self.app.get(short_url)
        assert 'http://google.com' in resp.data
       
        resp = self.app.get('/statistics')
        assert "http://google.com" in resp.data
        assert short_url in resp.data
        assert "Creation date" in resp.data
        assert "Short url" in resp.data
        assert "Full url" in resp.data
        assert "Redirects" in resp.data

    def test_statistics_page_not_available_if_not_logged_in(self):
        resp = self.app.get('/statistics')
        assert "You should log in first" 

if __name__ == '__main__':
    unittest.main()
