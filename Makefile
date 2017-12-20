run-client:
	python src/client.py

install-server:
	mysql -p < db/build_database.sql

run-server:
	python src/server.py
