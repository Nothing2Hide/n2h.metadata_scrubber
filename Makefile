EXE_NAME := "scrubbertk"

test: pytest flake8

pytest:
	@echo "==== Running pytest ===="
	@bin/py.test --cov=src --cov-report=term-missing tests

flake8:
	@echo "==== Running Flake8 ===="
	@bin/flake8 src

installer:
	@echo "=== Building installer ==="
	@bin/pyinstaller -p src/n2h -F -n $(EXE_NAME) src/n2h/metadata_scrubber/gui.py
