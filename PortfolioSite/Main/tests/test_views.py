from django.test import TestCase, Client

# Create your tests here.
class BaseTest(TestCase):
    USERNAME = 'test_username'
    PASSWORD = 'testing1234'
    
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

class HomePageTest(BaseTest):
    def test_home(self):
        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 not logged in')

class AboutTest(BaseTest):
    """
    Test About View
    """
    def test_about(self):
        r = self.c.get('/about/')
        self.assertTrue(r.status_code==200, msg='About should return 200 not logged in')
    
    def test_title(self):
        r = self.c.get('/about/')
        self.assertContains(r,'<title>About')
    


class ContactTest(BaseTest):
    """
    Test Contact View
    """
    def test_home(self):
        r = self.c.get('/contact/')
        self.assertTrue(r.status_code==200, msg='Contact should return 200 not logged in')
    
    def test_title(self):
        r = self.c.get('/contact/')
        self.assertContains(r,'<title>Contact')

    def test_form_in_context(self):
        r = self.c.get('/contact/')
        
