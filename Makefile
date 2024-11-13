.PHONY: test
test:
	pytest

pretty:
	ruff format .
	ruff check --fix
