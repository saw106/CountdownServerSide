cover:
	coverage run --omit="/usr/*" RestEntry.py
report:
	coverage html 
clean:
	rm .coverage
	rm -rf htmlcov
