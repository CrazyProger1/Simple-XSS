.PHONY: test
test:
	poetry run python -m pytest tests/

.PHONY: run
run:
	poetry run python -m simplexss


.PHONY: cleancode
cleancode:
	isort .
	black .
	mypy .

.PHONY: translations
translations:
	poetry run python -m i18n src/__init__.py simplexss.pot


.PHONY: build
build:
	poetry run pyinstaller -F --name Simple-XSS --icon "resources/images/logo.ico" main.py


