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
   poetry shell
   ```

---

## ✦ Running the Server

To start the FastAPI development server on `localhost:8000`:

```bash
make run
```

This will launch the app with live reload via Uvicorn. You can then visit:

```
http://localhost:8000/helloworld
```

---

## ✦ Makefile Commands

| Command          | Description                               |
| ---------------- | ----------------------------------------- |
| `make run`       | Start the FastAPI server with live reload |
| `make format`    | Format code with Black                    |
| `make typecheck` | Check static types with Mypy              |
| `make test`      | Run tests                                 |
| `make install`   | Install all project dependencies          |

## ✦ License

This project is released under the [CC0 Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/).
You may fork, adapt, reuse, or ignore it freely.

[![Public Domain](https://licensebuttons.net/p/mark/1.0/88x31.png)](http://questioncopyright.org/promise)

> ["Make art not law"](http://questioncopyright.org/make_art_not_law_interview) - Nina Paley

