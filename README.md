# Getting Started

- Create a virtualenv
- `pip install -r requirements.txt`
- Update `SKIP_API_KEY` with a valid value in `settings.py`
- `./manage.py collectstatic`
- `./manage.py migrate`
- `./manage.py runserver`
- Point your browser to http://127.0.0.1:8000/skip/
