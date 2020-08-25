# import json
import requests
from urllib.parse import urlencode

from django.conf import settings

try:
    SKIP_BASE_URL = settings.SKIP_BASE_URL
except AttributeError:    
    SKIP_BASE_URL = 'http://skip.dev.hop.scimma.org/api'
SKIP_API_KEY = settings.SKIP_API_KEY

class SkipAPIClient():

    def get_alerts(self, *args, **kwargs):
        query_params = urlencode(kwargs)
        response = requests.get(f'{SKIP_BASE_URL}/alerts/?{query_params}', headers={'Authorization': f'Token {SKIP_API_KEY}'})
        response.raise_for_status()
        return response.json()['results']