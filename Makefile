test: pytest flake8

pytest:
	@echo "==== Running pytest ===="
	@bin/py.test --cov=src --cov-report=term-missing tests

flake8:
	@echo "==== Running Flake8 ===="
	@bin/flake8 src
