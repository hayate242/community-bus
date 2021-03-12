
up-build:
	docker-compose up --build
up:
	docker-compose up --build -d
	make setup
	docker-compose logs -f -t
front-up:
	docker-compose exec node npm run serve
front-mock:
	docker-compose exec node npm run mock-serve
front-local:
	docker-compose exec node npm run local-serve
front-prod:
	docker-compose exec node npm run prod-serve

front-lint:
	docker-compose exec node npm run lint
front-build:
	docker-compose exec node npm run build
front-dev-build:
	docker-compose exec node npm run dev-build
front-prod-build:
	docker-compose exec node npm run prod-build

back-dev:
	docker-compose up  --build --scale node=0 --scale nginx=0
reset-db:
	rm -rf ./backend/bus/migrations/
	rm -rf ./backend/users/migrations/
	docker-compose exec db mysql -u django -pdjango -e 'drop database `django-db`'
	docker-compose exec db mysql -u django -pdjango -e 'create database `django-db`'
back-seed: reset-db
	docker-compose exec django /app/manage.py makemigrations
	docker-compose exec django /app/manage.py makemigrations users
	docker-compose exec django /app/manage.py migrate
	docker-compose exec django /app/manage.py migrate users
	docker-compose exec django /app/manage.py makemigrations bus
	docker-compose exec django /app/manage.py migrate bus
	docker-compose exec django bash -c '/app/manage.py loaddata /app/users/fixtures/*.json'
	docker-compose exec django bash -c '/app/manage.py loaddata /app/bus/fixtures/*.json'

setup:
	@if [ ! -d "frontend/node_modules" ]; then\
		docker-compose exec node npm install ;\
	fi
down:
	docker-compose down

migrate:
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate

clean:
	docker-compose down -v

	@if [ -d "frontend/node_modules" ]; then\
		docker-compose run --rm frontend rm -rf /app/node_modules; \
	fi
