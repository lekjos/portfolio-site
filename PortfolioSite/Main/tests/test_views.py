from django.test import TestCase, Client

# Create your tests here.
class BasePermissionsTest(TestCase):
    USERNAME = 'test_username'
    PASSWORD = 'testing1234'
    
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

class HomePageTest(BasePermissionsTest):
    def test_home(self):
        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 not logged in')

class AboutTest(BasePermissionsTest):
    """
    Test About View
    """
    def test_about(self):
        r = self.c.get('/about/')
        self.assertTrue(r.status_code==200, msg='About should return 200 not logged in')

class ContactTest(BasePermissionsTest):
    """
    Test Contact View
    """
    def test_home(self):
        r = self.c.get('/contact/')
        self.assertTrue(r.status_code==200, msg='Contact should return 200 not logged in')
