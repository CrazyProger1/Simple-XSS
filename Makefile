.PHONY: test
test:
	poetry run python -m pytest tests/


.PHONY: run
run:
	poetry run python -m simplexss


.PHONY: translations
translations:
	poetry run python -m i18n simplexss/__init__.py simplexss.pot


.PHONY: build
build:
	poetry run pyinstaller -F --name Simple-XSS --icon "resources/images/logo.ico" simplexss/__main__.py
	copy resources dist/resources
	copy settings.toml dist/settings.toml