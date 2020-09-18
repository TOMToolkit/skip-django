from django.views.generic import TemplateView


class SkipView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_index.html'


class SkipTargetView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_target.html'


class SkipSwiftXRTView(TemplateView):
    template_name = 'skip_dpd/skip_dpd_swiftxrt.html'

