from ipaddress import ip_address
from Main.tests.test_views import BaseTest
from Main.models import Email, Project, Image

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
        