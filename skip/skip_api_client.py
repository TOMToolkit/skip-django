import json
import requests

from django.conf import settings


class SkipAPIClient():

    def __init__(self, *args, **kwargs):
        pass

    def get_alerts(self, *args, **kwargs):
        response = requests.