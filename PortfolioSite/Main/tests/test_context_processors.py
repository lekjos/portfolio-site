from django.test import TestCase
from Main.tests.test_views import BaseTest

class GlobalProcessorTest(BaseTest):
    """
    Validate that global context processor is spitting out values
    """
    def test_home_context(self):
        """
        Test home page has global context processor content
        """
        r = self.c.get('/')
        self.assertIn('root_url',r.context,'Should be root_url in context')
        self.assertIn('django_environ',r.context,'Should be root_url in context')
        self.assertTrue(r.context['django_environ']=='dev','Django environ should be "dev" in context')