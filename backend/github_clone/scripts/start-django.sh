cd backend/github_clone

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py db_population

gunicorn github_clone.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --threads 4