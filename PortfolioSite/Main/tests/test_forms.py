from Main.tests.test_views import BaseTest
from django.test import TestCase
from Main.forms import ContactForm
from Main.models import Email

class ContactFormTest(BaseTest, TestCase):
    """
    Test email contact form.
    """
    @classmethod
    def setUpTestData(cls):
        cls.valid_form_data = {
            'name':'joebob;',
            'email':'joebob@joebob.com',
            'subject':'This is a valid subject.',
            'body':'This is a valid email body.',
        }
        cls.invalid_subject = {
            'subject':'This subject is way too long'+'asdfasdf'*50
        }
        cls.ip = '192.168.1.1'


    def test_init_without_ip(self):
        """
        Test that contact form can be initialized
        """
        with self.assertRaises(KeyError):
            form = ContactForm()
    
    def test_init_with_ip(self):
        """
        Form should initialize with ip_address kwarg
        """
        form = ContactForm(ip_address = '192.168.1.1')
    
    def test_valildate_email(self):
        """
        Test that form validates email address
        """
        form = ContactForm(self.valid_form_data, ip_address=self.ip)
        instance = form.save()

        self.assertEqual(self.valid_form_data['name'], instance.name)
        self.assertEqual(self.valid_form_data['subject'], instance.subject)
        self.assertEqual(self.valid_form_data['email'], instance.email)
        self.assertEqual(self.valid_form_data['body'], instance.body)
        self.assertEqual(instance.ip_address, '192.168.1.1')

    def test_blank_form(self):
        """
        Verify that blank form raises correct errors.
        """
        form = ContactForm({}, ip_address = self.ip)
        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['subject'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['body'], ['This field is required.'])
        
    def tearDown(self):
        """
        Remove models that were created
        """
        Email.objects.all().delete()
    
    
