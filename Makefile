run-client:
	python src/client.py $(addr)

install:
	pip install mysqlclient

install-server:
	mysql -p < db/build_database.sql
	make install

run-server:
	cd src/ && python -m server 9999
