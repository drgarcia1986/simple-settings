clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

isort-check:
	@poetry run isort simple_settings --check

isort-fix:
	@poetry run isort simple_settings

flake8:
	@poetry run flake8 simple_settings/

test: clean flake8
	@poetry run pytest --cov-config .coveragerc --cov-report term-missing --cov simple_settings/ tests/

test-debug: clean
	@poetry run pytest -x --pdb simple_settings/ tests/

requirements: clean
	@poetry install --extras all

release-patch:
	@poetry run bumpversion patch

release-minor:
	@poetry run bumpversion minor

release-major:
	@poetry run bumpversion major

sdist: test
	@poetry build

outdated:
	@pip list --outdated --format=columns
