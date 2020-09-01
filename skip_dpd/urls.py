from django.urls import path

from skip_dpd import dash
from skip_dpd.views import SkipView, SkipTargetView

app_name = 'skip'

urlpatterns = [
    path('', SkipView.as_view(), name='index'),
    path('target/<int:pk>/', SkipTargetView.as_view(), name='target')
]
