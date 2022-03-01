
# from https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
from django.urls import reverse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def find_next_and_previous(id_:int, qs:dict, view_name='project') -> dict:
    """
    Returns dict of next and previous item's ID and Title. Pass in ordered queryset as dictionary with 'id' and 'title' fields.
    Optional arg view_name: used for reverse()

    Output:
    {
        'previous_id': <int>,
        'previous_title': <str>,
        'next_id': <int>,
        'next_title': <str>,
    }
    """
    match_found=False
    r = {
        'previous_id': None,
        'previous_url': None,
        'previous_title': None,
        'next_id': None,
        'next_url': None,
        'next_title': None,
    }

    for entry in qs:
        if match_found:
            r['next_id'] = entry['id']
            r['next_url'] = reverse(view_name, kwargs={'pk':entry['id']})
            r['next_title'] = entry['title']
            return r
        if entry['id'] == id_:
            match_found=True
        else:
            r['previous_id']=entry['id']
            r['previous_url'] = reverse(view_name, kwargs={'pk':entry['id']})
            r['previous_title']=entry['title']
        

    return r