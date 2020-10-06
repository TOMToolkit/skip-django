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

- Add `skip_dpd`, `bootstrap4`, and  `django_plotly_dash.apps.DjangoPlotlyDashConfig` to `INSTALLED_APPS` in `settings.py`.
- Add `SKIP_API_KEY` with an appropriate value to `settings.py`.
- Add `X_FRAME_OPTIONS = 'SAMEORIGIN'` to `settings.py`.
- Copy `PLOTLY_COMPONENTS = [<various>]` from `skip_dpd_base/settings.py` to `settings.py`.
- Add `path('django_plotly_dash/', include('django_plotly_dash.urls'))` to your top level `urls.py` (Note: in a TOM built with the TOM Toolkit, this may cause problems as it may need to live specifically in `tom_common/urls.py` but this is untested).
- Add `path('skip/', include('skip_dpd.urls', namespace='skip'))` to `urls.py` wherever you want it (e.g., `tom_alerts/urls.py`).
