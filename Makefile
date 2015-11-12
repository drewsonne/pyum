rst-readme:
	pandoc README.md -f markdown -t rst -s -o README.rst

release-test: rst-readme
	twine upload -r pypitest dist/pyum-*

release: rst-readme
	twine upload -r pypi dist/pyum-*