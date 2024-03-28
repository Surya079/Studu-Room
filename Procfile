web: gunicorn
base.wsgi:application \
--worker-class threshold \
--threads 4 \
--user vercel \
--env
DJANGO_SETTINGS_MODULE=tamilbuddy.settings
