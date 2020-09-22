from django.urls import path

from skip_dpd import dash
from skip_dpd.views import SkipAlertsView, SkipIndexView, SkipSwiftXRTView, SkipTargetView

app_name = 'skip'

urlpatterns = [
    path('', SkipIndexView.as_view(), name='index'),
    path('alerts', SkipAlertsView.as_view(), name='alerts'),
    path('target/<int:pk>/', SkipTargetView.as_view(), name='target'),
    path('swift', SkipSwiftXRTView.as_view(), name='swiftxrt')
]
