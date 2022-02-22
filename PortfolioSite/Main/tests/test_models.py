from django.conf import settings
import os
from ipaddress import ip_address
from Main.tests.helpers import BaseTest, AddFixtures, FIXTURES_DIR
from Main.models import Email, Project, Image
from pprint import pprint
from django.test import TestCase


class EmailTest(BaseTest, TestCase):
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

class ProjectTest(BaseTest, TestCase):
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

class ImageTest(BaseTest, TestCase):
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

class StepManagerTest(AddFixtures, BaseTest, TestCase):

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




        