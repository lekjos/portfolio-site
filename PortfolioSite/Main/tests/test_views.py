from Main.tests.helpers import AddUser, AddFixtures, BaseTest, MoveBaseAbstract
from unittest import skip
from django.test import TestCase

import json

from Main.models import Project



class HomePageTest(BaseTest, TestCase):
    def test_home(self):
        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 not logged in')  



class TestMoveAjax(MoveBaseAbstract, TestCase):
    model_class = Project
    base_url = "/ajax/move-project/"





# class ContactTest(BaseTest):
#     """
#     Test Contact View
#     """
#     def test_home(self):
#         r = self.c.get('/contact/')
#         self.assertTrue(r.status_code==200, msg='Contact should return 200 not logged in')
    
#     def test_title(self):
#         r = self.c.get('/contact/')
#         self.assertContains(r,'<title>Contact')

#     def test_form_in_context(self):
#         r = self.c.get('/contact/')
        
