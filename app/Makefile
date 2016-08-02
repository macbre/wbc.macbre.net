coverage_options = --include='wbc/*' --omit='tests/*,env*/*,*__init__.py'

test:
	py.test -x tests/

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m py.test -x tests/
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage report $(coverage_options)
