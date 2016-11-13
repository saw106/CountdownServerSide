cover:
	coverage run TestDBResources.py
	coverage html
clean:
	rm .coverage
	rm -rf htmlcov
