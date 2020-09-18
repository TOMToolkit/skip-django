import requests
from importlib import import_module
from urllib.parse import urlencode

from django.conf import settings

try:
    SKIP_BASE_URL = settings.SKIP_BASE_URL
except AttributeError:    
    SKIP_BASE_URL = 'http://skip.dev.hop.scimma.org/api'
SKIP_API_KEY = settings.SKIP_API_KEY


def get_client():
    try:
        api_class = settings.SKIP_CLIENT
    except AttributeError:
        api_class = 'skip_dpd.skip_client.SkipClient'
    
    module_name, class_name = api_class.rsplit('.', 1)
    try:
        client_module = import_module(module_name)
        clazz = getattr(client_module, class_name)
        return clazz
    except (ImportError, AttributeError):
        raise ImportError(f'Could not import {api_class}. Did you provide the correct path?')


class SkipClient():

    def get_alerts(self, *args, **kwargs):
        # process the list of topic IDs into zero or more query_params
        topics = kwargs.pop('topic', [])
        query_params = urlencode(kwargs)
        # process the topics (if any) into query params
        for topic in topics:
            query_params = query_params + f'&topic={topic}'

        response = requests.get(f'{SKIP_BASE_URL}/alerts/?{query_params}',
                                headers={'Authorization': f'Token {SKIP_API_KEY}'})
        response.raise_for_status()
        return response.json()['results']

    def get_topics(self, *args, **kwargs):
        query_params = urlencode(kwargs)
        response = requests.get(f'{SKIP_BASE_URL}/topics/?{query_params}', headers={'Authorization': f'Token {SKIP_API_KEY}'})
        response.raise_for_status()
        return response.json()['results']
