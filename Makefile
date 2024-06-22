runserver:
	docker exec -it manager-web python manage.py runserver

install-requirements:
	docker exec -it manager-web pip install -r requirements.txt

launch-docker:
	bash docker-launch.sh

launch-docker-build:
	bash docker-launch.sh build

migrate:
	docker exec -it manager-web python manage.py migrate

create-super-user:
	docker exec -it manager-web python manage.py createsuperuser
