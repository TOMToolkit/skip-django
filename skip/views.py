from django.views.generic import TemplateView


class SkipView(TemplateView):
    template_name = 'skip/skip_main.html'
