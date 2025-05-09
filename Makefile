.PHONY: run format typecheck test install

# Run the FastAPI server
run:
	poetry run uvicorn app.main:app --reload

# Format code using Black
format:
	poetry run black .

# Check static types using Mypy
typecheck:
	poetry run mypy app/

# Run tests with Pytest
test:
	PYTHONPATH=. poetry run pytest

# Install all dependencies (including dev)
install:
	poetry install
