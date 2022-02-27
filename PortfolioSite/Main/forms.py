from django.forms import forms, ModelForm
from Main.models import Email

class ContactForm(ModelForm):
    """
    Contact form which emails site administrator when submitted
    """
    class Meta:
        model = Email
        fields = ['name','email','subject','body']
    
    def __init__(self, *args, **kwargs):
        """
        Form requires ip_address kwarg
        """
        self.ip_address = kwargs.pop('ip_address')
        super().__init__(*args, **kwargs)
    
    def save(self,commit=True, *args, **kwargs):
        email = super().save(commit=False, *args, **kwargs)
        email.ip_address = self.ip_address
        if commit:
            email.save()
        return email

