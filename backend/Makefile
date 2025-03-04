.PHONY: install run test build

install:
	virtualenv venv
	. venv/bin/activate
	venv/bin/python -m pip install -r requirements.txt
	venv/bin/python -m pip install pytest

run:
	venv/bin/python main.py

test:
	pytest