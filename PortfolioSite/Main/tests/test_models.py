from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
from ipaddress import ip_address
from Main.tests.test_views import BaseTest
from Main.models import Email, Project, Image
from pprint import pprint
import shutil

class EmailTest(BaseTest):
    """
    Test email model.
    """

    def test_string_rep(self):
        """
        Test email model string representation
        """
        testme = Email(
            name='job blow',
            subject = 'subject',
            body='test body',
            ip_address = '192.168.1.1',
        )
        subj_trunc = testme.subject
        stringrep_expected = testme.name + ' - ' + subj_trunc
        self.assertEqual(str(testme), stringrep_expected, "String_rep should be same as second arg.")
        
        testme.subject = 'asdlkj;fsajkl;dfasljk;dkl;jasdkl;jfasl;jkdfjkl;asdfljkasdl;jkfasjk;dfas;ljkdf;ljaksdf;ljkas;dljkfadwsfawqefawegefafwefaas;'
        subject_trunc = testme.subject[:75] + '...'
        stringrep_expected = testme.name + ' - ' + subject_trunc
        self.assertEqual(str(testme), stringrep_expected, "String_rep should be same as second arg.")

class ProjectTest(BaseTest):
    """
    Test project model.
    """

    def test_string_rep(self):
        """
        Test portfolio item string representation
        """
        testme = Project(title='titlesd')
        stringrep_expected = str(testme.title)
        self.assertEqual(str(testme), stringrep_expected, "String_rep should be same as second arg.")

class ImageTest(BaseTest):
    """
    Test project model.
    """

    def test_string_rep(self):
        """
        Test portfolio item string representation
        """
        testme = Image(title='titlesdfsd')
        stringrep_expected = str(testme.title)
        self.assertEqual(str(testme), stringrep_expected, "String_rep should be same as second arg.")

FIXTURES_DIR = os.path.join(settings.BASE_DIR,'fixtures/test_img.jpg')

class StepManagerTest(BaseTest):

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

    
    def tearDown(self):
        Project.objects.all().delete()
        Image.objects.all().delete()

        #delete media files
        dir_path = settings.MEDIA_ROOT
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)


    def test_create_project(self):
        """
        Test Create Method
        """
        self.assertEqual(self.test_proj1.order,1)
        self.assertEqual(self.test_proj2.order,2)
    
    def test_img_uploaded(self):
        """
        verify that image uploaded successfully
        """
        img = Image.objects.get(title="proj1 img1", project=self.test_proj1)
        self.assertEquals(img.title, self.proj1_img1.title)
        self.assertEquals(img.order, 1)

    def test_move_project(self):
        """
        Test moving object to new position
        """
        self.assertEqual(self.test_proj1.order,1, "initial value")
        self.assertEqual(self.test_proj2.order,2, "initial value")
        
        Project.objects.move(self.test_proj1, 2)

        self.test_proj1 = Project.objects.get(title="test title 1")
        self.test_proj2 = Project.objects.get(title="test title 2")
        self.assertEqual(self.test_proj1.order,2, "Updated value")
        self.assertEqual(self.test_proj2.order,1, "Updated value")

        Project.objects.move(self.test_proj1, 1)
        
        self.test_proj1 = Project.objects.get(title="test title 1")
        self.test_proj2 = Project.objects.get(title="test title 2")
        self.assertEqual(self.test_proj1.order,1, "Back to initial")
        self.assertEqual(self.test_proj2.order,2, "Back to initial")

    
    def test_move_img(self):
        """
        test moving images
        """
        self.assertEqual(self.proj1_img1.order,1)
        self.assertEqual(self.proj1_img2.order,2)
        self.assertEqual(self.proj2_img1.order,1)
        self.assertEqual(self.proj2_img2.order,2)

        Image.objects.move(self.proj1_img1, 2)
        self.proj1_img1 = Image.objects.get(title="proj1 img1")
        self.proj1_img2 = Image.objects.get(title="proj1 img2")
        self.assertEqual(self.proj1_img1.order,2, 'order changed')
        self.assertEqual(self.proj1_img2.order,1, 'order changed')
        self.assertEqual(self.proj2_img1.order,1, 'order unchanged')
        self.assertEqual(self.proj2_img2.order,2, 'order unchanged')

        Image.objects.move(self.proj1_img1, 1)
        self.proj1_img1 = Image.objects.get(title="proj1 img1")
        self.proj1_img2 = Image.objects.get(title="proj1 img2")
        self.assertEqual(self.proj1_img1.order,1, 'order returned to initial')
        self.assertEqual(self.proj1_img2.order,2, 'order returned to initial')
        self.assertEqual(self.proj2_img1.order,1, 'order unchanged')
        self.assertEqual(self.proj2_img2.order,2, 'order unchanged')




        