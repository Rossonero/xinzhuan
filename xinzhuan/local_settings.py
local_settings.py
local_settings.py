DATABASE_IP = '127.0.0.1'
DATABASE_USER = 'root'
DATABASE_PASS = 'forelord12'

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': 'xinzhuan',                      # Or path to database file if using sqlite3.
         'USER': DATABASE_USER,                      # Not used with sqlite3.
         'PASSWORD': DATABASE_PASS,                  # Not used with sqlite3.
         'HOST': DATABASE_IP,                      # Set to empty string for localhost. Not used with sqlite3.
         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
     }
 }