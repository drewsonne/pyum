install: clean rst-readme
	pip install -e .

rst-readme:
	pandoc README.md -f markdown -t rst -s -o README.rst

build:
	python setup.py sdist bdist_wheel

release-test: clean rst-readme build
	twine upload -r pypitest dist/pyum-*

release: clean rst-readme build
	twine upload -r pypi dist/pyum-*

test: clean rst-readme
	tox

clean:
	rm -rf dist build *.egg-info MANIFEST README.rst .tox .eggs