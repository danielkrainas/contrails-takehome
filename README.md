![Contrails Project Banner](./assets/banner.png)

# Contrails Take Home

![Python](https://img.shields.io/badge/python-%3E=3.11-blue?logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/built%20with-poetry-cyan?logo=poetry)
[![License: CC0](https://img.shields.io/badge/license-CC0-ff69b4.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

## ✦ Project Overview

This project is a take-home coding assignment for the Contrails group at Breakthrough Energy. It implements a simple, modular REST API using FastAPI, with a focus on clean architecture, reproducibility, and incremental feature development.

## ✦ Project Setup

This project is built with **Python 3.11+** and uses **[Poetry](https://python-poetry.org/)** for dependency and environment management.

### 🔧 Dependencies

Core dependencies:

* [`fastapi`](https://fastapi.tiangolo.com/) - API framework
* [`uvicorn`](https://www.uvicorn.org/) - ASGI server

Dev tools (optional, recommended):

* [`black`](https://black.readthedocs.io/) - code formatter
* [`mypy`](http://mypy-lang.org/) - static type checker
* [`pytest`](https://docs.pytest.org/) - unit testing

---

## ✦ Installation Instructions

1. **Install Poetry (if you don't have it):**

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone the repository:**

   ```bash
   git clone git@github.com/danielkrainas/contrails-takehome.git
   cd contrails-takehome
   ```

3. **Install dependencies and create a virtual environment:**

   ```bash
   make install
   ```

4. **Activate the virtual environment (optional):**

   ```bash
   poetry env activate 
   ```

---

## ✦ Running the Server

You can start the FastAPI server in two modes:

### Development mode (with live reload)

Use this for active development:

```bash
make rundev
```

This runs the server with Uvicorn's `--reload` option, automatically restarting on code changes.

---

### Restartable mode (used with `/roll`)

Use this to test the `/roll` webhook or simulate production-style restarts:

```bash
make run
```

This runs the server in a loop. When `/roll` is triggered, the app will pull the latest code and restart itself. This behavior is controlled by the `CONTRAILS_RESTART_ON_UPDATE` environment variable. It's automatically set by the Makefile.

---

Once the server is running, you can visit:

- `http://localhost:8000/helloworld` - basic endpoint
- `http://localhost:8000/docs` - auto-generated Swagger docs
- `http://localhost:8000/redoc` - alternative ReDoc interface

## ✦ Makefile Commands

| Command          | Description                                                               |
| ---------------- | ------------------------------------------------------------------------- |
| `make run`       | Start the FastAPI server in a restartable loop (used with `/roll`)        |
| `make rundev`    | Start the FastAPI server with live reload for development (auto-restarts) |
| `make install`   | Install project dependencies using Poetry                                 |
| `make test`      | Run the test suite with Pytest                                            |
| `make format`    | Format code using Black                                                   |
| `make typecheck` | Run static type checks using Mypy                                         |

## ✦ API Examples

### 📍 `GET /helloworld`

#### Plain text response (default):

```bash
curl http://localhost:8000/helloworld
```

#### JSON response:

```bash
curl -H "Accept: application/json" http://localhost:8000/helloworld
```

#### With timezone parameter:

```bash
curl -H "Accept: application/json" "http://localhost:8000/helloworld?tz=Europe/London"
```

#### With invalid timezone:

```bash
curl -H "Accept: application/json" "http://localhost:8000/helloworld?tz=NotARealZone"
```

---

### 📍 `POST /unravel`

#### Example request:

```bash
curl -X POST http://localhost:8000/unravel \
  -H "Content-Type: application/json" \
  -d '{
    "key1": {"keyA": ["foo", 0, "bar"]},
    "some other key": 2,
    "finally": "end"
  }'
```

#### Expected response:

```json
["key1", "keyA", "foo", 0, "bar", "some other key", 2, "finally", "end"]
```

### 📍 `POST /roll`

Triggers a rolling update of the server by pulling the latest code from `main` and restarting the app.

#### Example:

```bash
curl -X POST http://localhost:8000/roll
````

**Note:** Only works when running with `make run`. No-op in `rundev` mode.

## ✦ License

This project is released under the [CC0 Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/).
You may fork, adapt, reuse, or ignore it freely.

[![Public Domain](https://licensebuttons.net/p/mark/1.0/88x31.png)](http://questioncopyright.org/promise)

> ["Make art not law"](http://questioncopyright.org/make_art_not_law_interview) - Nina Paley

