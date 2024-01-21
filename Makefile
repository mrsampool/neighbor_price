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
	mkdir -p package/components; \
	cp -r components/event_manager package/components/; \
	cp -r components/regions package/components/; \
	cp components/__init__.py package/components/; \
	cp -r data_analyzer package/; \
	\
	mv package/data_analyzer/lambda/* package/ ; \
	\
	source venv/bin/activate; \
	pip install \
	-r package/lambda_requirements.txt \
    --target ./package \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: --upgrade; \
	\
	cd package; \
	zip -r ../data_analyzer_package.zip .; \
	cd ..; \
	rm -rf package;
	aws lambda update-function-code \
	--function-name arn:aws:lambda:us-west-1:065361442221:function:data_analyzer \
	--zip-file fileb://data_analyzer_package.zip;

.PHONE: run
run:
	python3 -m venv venv; \
	source .env; \
	source venv/bin/activate; \
	python -m neighbor_price;

