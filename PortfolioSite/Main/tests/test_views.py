from django.test import TestCase, Client

# Create your tests here.
class BasePermissionsTest(TestCase):
    USERNAME = 'test_username'
    PASSWORD = 'testing1234'
    
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
    
    def test_home(self):
        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 not logged in')
