PYTHON ?= python3

.PHONY: install test lint run plan demo persona-json persona-prompt clean

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	PYTHONPATH=packages $(PYTHON) -m pytest -q

lint:
	PYTHONPATH=packages $(PYTHON) -m ruff check packages services tests scripts

run:
	PYTHONPATH=packages $(PYTHON) -m uvicorn services.api.main:app --reload --host 0.0.0.0 --port 8000

plan:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py plan --prompt "Trap Soul a 140 BPM em C# menor"

demo:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py demo --duration 8 --output data/output/demo.wav

persona-json:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py persona --format json

persona-prompt:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py persona --format prompt

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
