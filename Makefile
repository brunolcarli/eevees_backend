install:
	pip install -r requirements.txt

shell:
	python manage.py shell

run:
	python manage.py runserver 0.0.0.0:7735

migrate:
	python manage.py makemigrations
	python manage.py migrate
