.PHONE: setup
setup:
	cp .env.sample .env;
	cp .env_test.sample .env_test;
	mkdir -p .docker-data/.mongo-data .docker-data/.rabbit-data .docker-data/.rabbit-log;

.PHONY: test
test:
	python3 -m venv venv; \
	source .env_test; \
	source venv/bin/activate; \
	python -m unittest; \

.PHONY: collect
collect:
	python3 -m venv venv; \
	source .env; \
	source venv/bin/activate; \
	python -m data_collector; \

.PHONY: analyze
analyze:
	python3 -m venv venv; \
	source .env; \
	source venv/bin/activate; \
	python -m data_analyzer; \

.PHONE: run
run:
	python3 -m venv venv; \
	source .env; \
	source venv/bin/activate; \
	python -m neighbor_price; \
