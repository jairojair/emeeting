all: clean
	@gunicorn --pythonpath src app:app --bind=0.0.0.0:8000 --reload

clean:
	@find . -name "*.pyc" -delete
	@find . -name "*__pycache__" -delete
	@find . -name ".coverage" -delete

tests: clean fmt lint
	@PYTHONPATH=src pytest --cov=src tests/

lint:
	@pycodestyle --ignore=E501 src

fmt:
	@black .

deps:
	@pip install -r requirements.txt

migrate:
	@orator -n migrate -c src/settings.py -p src/migrations -f

resetdb:
	@orator migrate:reset -c src/settings.py -p src/migrations

serve:
	@mkdocs serve
