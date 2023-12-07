include test_env.sh

.PHONY: test
test:
	source venv/bin/activate; \
	python -m unittest; \
