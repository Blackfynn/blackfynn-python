install:
	pip install -e .
	pip install -r requirements-test.txt -r requirements-format.txt

format:
	isort -rc .
	black .

lint:
	@isort -rc --check-only .
	@black --check .
