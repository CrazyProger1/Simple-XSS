.PHONY: test
test:
	poetry run python -m pytest tests/


.PHONY: run
run:
	poetry run python -m simplexss


.PHONY: translations
translations:
	poetry run python -m i18n simplexss/__init__.py simplexss.pot
