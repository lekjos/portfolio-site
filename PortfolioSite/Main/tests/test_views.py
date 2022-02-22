from Main.tests.helpers import AddUser, AddFixtures, BaseTest, MoveBaseAbstract
from unittest import skip
from django.test import TestCase

import json

from Main.models import Project, Image



class HomePageTest(BaseTest, TestCase):
    def test_home(self):
        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 not logged in')  

class TestProjectMoveAjax(MoveBaseAbstract, TestCase):
    model_class = Project
    base_url = "/ajax/move-project/"

    def _get_objects(self):
        return (self.test_proj1, self.test_proj2)

class TestImageMoveAjax(MoveBaseAbstract, TestCase):
    model_class = Image
    base_url = "/ajax/move-image/"

    def _get_objects(self):
        return (self.proj1_img1, self.proj1_img2)




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
        
