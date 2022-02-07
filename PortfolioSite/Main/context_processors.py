from django.conf import settings
import os
def global_processor(request):
    """
    Adds globally available context for base template.
    """
    root_url = settings.ROOT_URL.replace('http://',"").replace('https://',"").replace('nojessery','NoJessery')

    return {
        "root_url": root_url,
        "django_environ": os.environ['DJANGO_ENV'],
        }