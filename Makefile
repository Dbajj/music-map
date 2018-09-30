venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

run-local: venv
	export FLASK_APP=app/main.py; \
	venv/bin/python -m flask run;


