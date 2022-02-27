from Main.tests.helpers import AddUser, AddFixtures, BaseTest, MoveBaseAbstract
from unittest import skip
from django.test import TestCase,Client
from django.contrib.auth.models import User

import json

from Main.models import Project, Image



class HomePageTest(AddFixtures, TestCase):
    def setUp(self):
        self.c=Client()
        self.test_proj2.published = True
        self.test_proj2.save()

    def test_home_unauthenticated(self):
        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 not logged in')  
        self.assertTrue(len(r.context['projects']) == 1)
        self.assertNotIn(f'<a class="btn btn-info mr-2 reorderBtn" id="{str(self.test_proj2.id)}-moveUp" role="button">Up</a>', r.content.decode('utf-8'))
    
    def test_home_authenticated(self):
        su = User.objects.create(username='uname')
        su.is_staff=True
        su.is_superuser=True
        su.set_password('paasssqwer123;')
        su.save()
        self.assertTrue(su.is_superuser)

        status = self.c.login(username='uname',password='paasssqwer123;')
        self.assertEqual(status, True)

        r = self.c.get('/')
        self.assertTrue(r.status_code==200, msg='Home page should return 200 logged in')  
        print(r.context['projects'])
        self.assertTrue(len(r.context['projects']) == 2)
        self.assertInHTML(f'<a class="btn btn-info mr-2 reorderBtn" id="{str(self.test_proj2.id)}-moveUp" role="button">Up</a>', r.content.decode('utf-8'))
        self.c.logout()

class TestProjectDetail(AddFixtures, TestCase):
    def setUp(self):
        self.c=Client()
        self.test_proj2.published = True
        self.test_proj2.save()
    
    def test_unpublished_unauthenticated(self):
        r = self.c.get(f'/projects/{self.test_proj1.id}/')
        self.assertEqual(r.status_code, 403, 'unauthenitcated user shouldn\'t see unpublished' )

        r = self.c.get(f'/projects/{self.test_proj2.id}/')
        self.assertEqual(r.status_code, 200)


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
        
