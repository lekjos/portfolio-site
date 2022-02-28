
# from https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def in_dictlist(key, value, my_dictlist, default=False, ignore_key_error=False):
    """
    Checks for key value pair in a list of dictionaries. Returns tuple (index, matching dict) or default (false if no kwarg).
    """
    for i, entry in enumerate(my_dictlist):
        try:
            if entry[key] == value:
                return i, entry
        except KeyError:
            if ignore_key_error:
                pass
    return default