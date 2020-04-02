format:
	isort -rc .
	black .

lint:
	# TODO: put back once import re-ordering is validated
	# @isort -rc --check-only .
	@black --check .