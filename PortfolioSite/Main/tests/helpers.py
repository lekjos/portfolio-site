from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
import unittest
from django.contrib.auth.models import User

import shutil, os, json

from Main.models import Project, Image

FIXTURES_DIR = os.path.join(settings.BASE_DIR,'fixtures/test_img.jpg')

class AddUser():
    USERNAME = 'test_username'
    PASSWORD = 'testing1234'

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username=cls.USERNAME,
            password=cls.PASSWORD,
        )
        super().setUpTestData()

class AddFixtures():
    @classmethod
    def setUpTestData(cls):
        cls.test_proj1 = Project.objects.create(
            title="test title 1",
            description='<p>test description </p>',
        )
        cls.test_proj2 = Project.objects.create(
            title="test title 2",
            description='<p>test description </p>',
        )

        cls.proj1_img1 = Image.objects.create(
            title="proj1 img1",
            image = SimpleUploadedFile(name='test_image.jpg', content=open(FIXTURES_DIR, 'rb').read(), content_type='image/jpeg'),
            caption='<p>test description </p>',
            related_pk=cls.test_proj1.id
        )
        cls.proj1_img2 = Image.objects.create(
            title="proj1 img2",
            image = SimpleUploadedFile(name='test_image.jpg', content=open(FIXTURES_DIR, 'rb').read(), content_type='image/jpeg'),
            caption='<p>test description </p>',
            related_pk=cls.test_proj1.id
        )

        cls.proj2_img1 = Image.objects.create(
            title="proj2 img1",
            image = SimpleUploadedFile(name='test_image.jpg', content=open(FIXTURES_DIR, 'rb').read(), content_type='image/jpeg'),
            caption='<p>test description </p>',
            related_pk=cls.test_proj2.id
        )
        cls.proj2_img2 = Image.objects.create(
            title="proj2 img2",
            image = SimpleUploadedFile(name='test_image.jpg', content=open(FIXTURES_DIR, 'rb').read(), content_type='image/jpeg'),
            caption='<p>test description </p>',
            related_pk=cls.test_proj2.id
        )
        super().setUpTestData()

    
    def tearDown(self):
        Project.objects.all().delete()
        Image.objects.all().delete()

        #delete media files
        dir_path = settings.MEDIA_ROOT
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        
        super().tearDown()

# Create your tests here.
class BaseTest():
    
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

class MoveBaseAbstract(AddUser, AddFixtures, BaseTest):
    model_name = ""
    model_class = None
    base_url = None

    def test_move_basics(self):
        f"""
        Test moving {self.model_name} via view
        """
        r = self.c.put(self.base_url+str(self.test_proj1.id)+"/", content_type='application/json')
        self.assertEqual(r.status_code, 403, 'should require login')

        self.c.login(username=self.USERNAME,password=self.PASSWORD)
        r = self.c.put(self.base_url+str(self.test_proj1.id)+"/", content_type='application/json')
        self.assertEqual(r.status_code, 400, 'empty request is bad request')

        r = self.c.post(self.base_url+str(self.test_proj1.id)+"/", content_type='application/json')
        self.assertEqual(r.status_code, 405, 'post not allowed')

        r = self.c.get(self.base_url+str(self.test_proj1.id)+"/", content_type='application/json')
        self.assertEqual(r.status_code, 405, 'get not allowed')

        r = self.c.put(self.base_url+str(self.test_proj1.id+20)+"/", content_type='application/json', data={'action':'down'})
        self.assertEqual(r.status_code, 404, 'not found')

    def test_min_reached_response(self):
        f"""test minimum reached error for {self.model_name}"""
        self.c.login(username=self.USERNAME,password=self.PASSWORD)
        r = self.c.put(self.base_url+str(self.test_proj1.id)+"/", content_type='application/json', data={'action':'down'})

        self.assertEqual(r.status_code, 400, 'min already reached')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['status'], 'min already reached', 'min already reached')

    def test_max_reached_response(self):
        f"""test max reached error for {self.model_name}"""
        self.c.login(username=self.USERNAME,password=self.PASSWORD)
        r = self.c.put(self.base_url+str(self.test_proj2.id)+"/", content_type='application/json', data={'action':'up'})

        self.assertEqual(r.status_code, 400, 'max already reached')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['status'], 'max already reached', 'max already reached')

    def test_successful_move_up(self):
        f"""test successful response for {self.model_name}"""
        self.c.login(username=self.USERNAME,password=self.PASSWORD)
        r = self.c.put(self.base_url+str(self.test_proj1.id)+"/", content_type='application/json', data={'action':'up'})

        self.assertEqual(r.status_code, 203, 'success')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['status'], 'success', 'success')
        
        self.test_proj1 = self.model_class.objects.get(pk=self.test_proj1.id)
        self.assertEqual(self.test_proj1.order, 2,'should be in second position')

        self.model_class.objects.move(self.test_proj1,1)
        self.test_proj1 = self.model_class.objects.get(pk=self.test_proj1.id)
        self.assertEqual(self.test_proj1.order, 1,'return to initial')

    def test_successful_move_down(self):
        f"""test successful response for {self.model_name}"""
        self.c.login(username=self.USERNAME,password=self.PASSWORD)
        r = self.c.put(self.base_url+str(self.test_proj2.id)+"/", content_type='application/json', data={'action':'down'})

        self.assertEqual(r.status_code, 203, 'success')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['status'], 'success', 'success')
        
        self.test_proj2 = self.model_class.objects.get(pk=self.test_proj2.id)
        self.assertEqual(self.test_proj2.order, 1,'should be in second position')

        self.model_class.objects.move(self.test_proj2,2)
        self.test_proj2 = self.model_class.objects.get(pk=self.test_proj2.id)
        self.assertEqual(self.test_proj2.order, 2,'return to initial')