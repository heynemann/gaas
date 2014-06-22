run:
	@gaas -c ./gaas/config/local.conf -d -vvv -p 9999

test:
	@coverage run --branch `which nosetests` -vv --rednose -s tests/
	@echo
	@coverage report -m --fail-under=80

ci_test: mongo_test test

tox:
	@PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox

tox3:
	@PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox -e py33

toxpypy:
	@PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox -e pypy

setup:
	@pip install -e .\[tests\]
	@-pip install ujson

kill_mongo_test:
	@ps aux | awk '(/mongod.+test/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'
	@rm -rf /tmp/gaas_test/mongodata

mongo_test: kill_mongo_test
	@rm -rf /tmp/gaas_test/mongodata && mkdir -p /tmp/gaas_test/mongodata
	@mongod --dbpath /tmp/gaas_test/mongodata --logpath /tmp/gaas_test/mongotestlog --port 4445 --quiet --smallfiles --oplogSize 128 &
	@sleep 2

migration:
	@cd gaas/storage/sqlalchemy/ && alembic revision -m "$(DESC)"

drop_now drop:
	@mysql -u root -e "DROP DATABASE IF EXISTS gaas; CREATE DATABASE IF NOT EXISTS gaas"
	@echo "DB RECREATED"

drop_test:
	@-cd tests/ && alembic downgrade base
	@mysql -u root -e "DROP DATABASE IF EXISTS test_gaas; CREATE DATABASE IF NOT EXISTS test_gaas"
	@echo "DB RECREATED"

data db:
	@cd gaas/storage/sqlalchemy/ && alembic upgrade head

data_test: drop_test
	@cd tests/ && alembic upgrade head
