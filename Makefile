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
