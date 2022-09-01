import requests

from django.core.cache import cache
from django.conf import settings
from rest_framework.authentication import get_authorization_header


def get_permission_data(self, request, path=None):
    key = '{user_id}_{path}'.format(user_id=request.user.id, path=path)
    data = cache.get(key)
    if data:
        return data
    try:
        headers = {"Authorization": get_authorization_header(request)}
        r = requests.get(settings.AUTH_SERVER_PREFIX + path, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)
    except Exception as err:
        raise Exception(err)
    cache.set(key, r.json())
    return r.json()
