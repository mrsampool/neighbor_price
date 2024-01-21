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

.PHONY: collect
collect:
	source venv/bin/activate; \
	source .env; \
	python -m data_collector; \

.PHONY: analyzer.run
analyze:
	python3 -m venv venv; \
	source .env; \
	source venv/bin/activate; \
	python -m data_analyzer;

.PHONY: deploy.analyzer
deploy.analyzer:
	scripts/deploy_data_analyzer_lambda.sh

.PHONE: run
run:
	python3 -m venv venv; \
	source .env; \
	source venv/bin/activate; \
	python -m neighbor_price;

