.PHONE: init
init:
	cp .env.sample .env;
	mkdir -p .docker-data/.mongo-data .docker-data/.rabbit-data .docker-data/.rabbit-log .docker-data/.prometheus-data;
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt;

.PHONE: containers.start
containers.start:
	docker compose up -d;

.PHONE: containers.stop
containers.stop:
	docker compose stop;

.PHONY: test.unit
test.unit:
	source venv/bin/activate; \
	source .env; \
	python -m unittest discover -s . -p "test_*.py";

.PHONY: test.integration
test.integration:
	source venv/bin/activate; \
	source .env; \
	export REGION_DB_NAME=neighbor_price_test; \
	python -m pytest;

.PHONY: dev.collect
dev.collect:
	source venv/bin/activate; \
	source .env; \
	python -m data_collector;

.PHONY: dev.analyze
dev.analyze:
	source venv/bin/activate; \
	source .env; \
	python -m data_analyzer;

.PHONY: deploy.collector
deploy.collector:
	scripts/deploy_lambda.sh data_collector

.PHONY: deploy.analyzer
deploy.analyzer:
	scripts/deploy_lambda.sh data_analyzer

.PHONE: run
run:
	source venv/bin/activate; \
	source .env; \
	gunicorn neighbor_price.app:app;

