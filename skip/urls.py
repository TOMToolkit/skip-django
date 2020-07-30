from django.urls import path

from skip import dash
from skip.views import SkipView

app_name = 'skip'

urlpatterns = [
    path('', SkipView.as_view(), name='index'),
]
