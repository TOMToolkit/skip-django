from django.views.generic import TemplateView


class SkipIndexView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_index.html'


class SkipAlertsView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_alerts.html'


class SkipTargetView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_target.html'


class SkipSwiftXRTView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_swiftxrt.html'

