To start project enter below command to bash

$ git clone https://github.com/nickolamaz/Products.git

$ cd Products

$ virtualenv --no-site-packages .env

$ source .env/bin/activate

$ .env/bin/pip install -r requirements.txt

$ python manage.py syncdb

# Running django for local development

$ python manage.py runserver 0:8000 --settings=Products.settings.local

goto http://127.0.0.1:8000/