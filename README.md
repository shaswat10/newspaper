# newspaper
1) Install requirements.txt file (pip install -r requirements.xt)
2) run django (python manage.py runserver)
3) run celery (celery -A newsProject worker --loglevel=INFO --concurrency 1 -P solo)