clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

isort-check:
	isort --check

isort-fix:
	isort -rc .

flake8:
	flake8 simple_settings/

test: clean flake8
	py.test --cov-config .coveragerc --cov-report term-missing --cov simple_settings/ tests/

test-debug: clean
	py.test -x --pdb simple_settings/ tests/

requirements: clean
	pip install -U -r requirements-dev.txt

release-patch:
	bumpversion patch

release-minor:
	bumpversion minor

release-major:
	bumpversion major

sdist: test
	@python setup.py sdist bdist_wheel upload
