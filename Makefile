.PHONY: run rundev format typecheck test install

run:
	@echo "Starting FastAPI server loop..."
	@while true; do \
		CONTRAILS_RESTART_ON_UPDATE=1 poetry run uvicorn app.main:app; \
		echo "[server exited] Restarting in 1s..."; \
		sleep 1; \
	done

# Run the FastAPI server in development mode (no autoreloading from /roll)
rundev:
	CONTRAILS_RESTART_ON_UPDATE=0 poetry run uvicorn app.main:app --reload

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
