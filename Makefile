.PHONY: test
test:
	source .env_test; \
	source venv/bin/activate; \
	python -m unittest; \

.PHONY: collect
collect:
	source .env; \
	source venv/bin/activate; \
	python -m data_collector; \
