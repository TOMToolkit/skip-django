# Getting Started

- Create a virtualenv
- `pip install -r requirements.txt`
- Update `SKIP_API_KEY` with a valid value in `settings.py`
- `./manage.py collectstatic`
- `./manage.py migrate`
- `./manage.py runserver`
- Visit `localhost:8000/skip`


# Installation into the TOM Toolkit

This section is under maintenance, as it isn't 100% clear that the instructions couldn't be simplified.

- Add `skip` and `django_plotly_dash.apps.DjangoPlotlyDashConfig` to `INSTALLED_APPS` in `settings.py`.
- Add `SKIP_API_KEY` with an appropriate value to `settings.py`.
- Add `X_FRAME_OPTIONS = 'SAMEORIGIN'` to `settings.py`.
- Possible: Copy `PLOTLY_COMPONENTS = [<various>]` from `skip-django` to `settings.py`.
- Add `path('django_plotly_dash/', include('django_plotly_dash.urls'))` and `path('skip/', include('skip_urls', namespace='skip'))` to `urls.py`.