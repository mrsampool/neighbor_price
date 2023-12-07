.PHONY: backend/test

test:
	source venv/bin/activate; \
	source .env; \
	python -m unittest; \
