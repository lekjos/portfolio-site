# portfolio-site
 Personal portfolio site for the author built in Django

# Build Instrucitons

## Create local database or use elephantSQL database
1. Install PosgreSQL on local machine
2. create database 'django'
3. default user 'postgres
4. password [omitted]

## Create venv
1. Navigate to repository root
2. run `python -m venv env` to create virtual enviornment
3. run `pip install -r requirements.txt`

## Set up local machine
1. Clone Repo
2. Add .env file to root of repo (add environment variable `DJANGO_ENV=DEV` if in development)
3. Run `python manage.py migrate`
5. If in production, run `python manage.py collectstatic`
6. Run `python manage.py createsuperuser` and follow prompts to create first user
7. Run `python manage.py runserver`
