install:
	pip install --upgrade -e . -r requirements-test.txt -r requirements-format.txt

format:
	isort .
	black .

lint:
	@isort --check-only .
	@black --check .
