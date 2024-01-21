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

.PHONY: test
test:
	source venv/bin/activate; \
	source .env; \
	python -m unittest;

.PHONY: dev.collect
collect:
	source venv/bin/activate; \
	source .env; \
	python -m data_collector;

.PHONY: dev.analyze
analyze:
	source venv/bin/activate; \
	source .env; \
	python -m data_analyzer;

.PHONY: deploy.collector
deploy.collector:
	scripts/deploy_lambda.sh data_collector $LAMBDA_ARN_DATA_COLLECTOR

.PHONY: deploy.analyzer
deploy.analyzer:
	scripts/deploy_lambda.sh data_analyzer $LAMBDA_ARN_DATA_ANALYZER

.PHONE: run
run:
	source venv/bin/activate; \
	source .env; \
	python -m neighbor_price;

