run: .run

.run:
	@python -m uvicorn main:app --reload
	@echo "" > .run

create-migrations:
	@set PYTHONPATH=%PYTHONPATH%;%cd% && alembic revision --autogenerate -m $(d)

run-migrations:
	@set PYTHONPATH=%PYTHONPATH%;%cd% && alembic upgrade head

clean:
	del .run