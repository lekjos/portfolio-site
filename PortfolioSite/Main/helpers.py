
# from https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
from django.urls import reverse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def find_next_and_previous(slug:str, qs:dict, view_name='project') -> dict:
    """
    Returns dict of next and previous item's ID and Title. Pass in ordered queryset as dictionary with 'id' and 'title' fields.
    Optional arg view_name: used for reverse()

    Output:
    {
        'previous_slug': <str>,
        'previous_title': <str>,
        'next_slug': <str>,
        'next_title': <str>,
    }
    """
    match_found=False
    r = {
        'previous_slug': None,
        'previous_url': None,
        'previous_title': None,
        'next_slug': None,
        'next_url': None,
        'next_title': None,
    }

    for entry in qs:
        if match_found:
            r['next_slug'] = entry['slug']
            r['next_url'] = reverse(view_name, kwargs={'slug':entry['slug']})
            r['next_title'] = entry['title']
            return r
        if entry['slug'] == slug:
            match_found=True
        else:
            r['previous_slug']=entry['slug']
            r['previous_url'] = reverse(view_name, kwargs={'slug':entry['slug']})
            r['previous_title']=entry['title']
        

    return r