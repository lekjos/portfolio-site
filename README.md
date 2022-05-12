# portfolio-site
 Personal portfolio site for the author built in Django

# Setup Instrucitons

1. Clone Repo
2. Navigate to repository root
3. run `python -m venv env` to create virtual enviornment
4. run `pip install -r requirements.txt && pip install -r requirements_dev.txt`
5. Add .env file to root of repo (add environment variable `DJANGO_ENV=DEV` if in development)... see `settings.py` for available options
6. Run `python manage.py migrate`
7. If in production, run `python manage.py collectstatic`
8. Run `python manage.py createsuperuser` and follow prompts to create first user
9. Run `python manage.py runserver`
