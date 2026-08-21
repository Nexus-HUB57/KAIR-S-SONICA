PYTHON ?= python3

.PHONY: install test lint run plan demo load load-studio-master persona-json persona-prompt clean

REQUESTS ?= 20
CONCURRENCY ?= 5
STUDIO_ROUNDS ?= 5
STUDIO_WEBSOCKETS ?= 5

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	PYTHONPATH=packages $(PYTHON) -m pytest -q

lint:
	PYTHONPATH=packages $(PYTHON) -m ruff check packages services tests scripts tools --extend-exclude scripts/assemble_unleash_the_dragon_real_v2.py

run:
	PYTHONPATH=packages $(PYTHON) -m uvicorn services.api.main:app --reload --host 0.0.0.0 --port 8000

plan:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py plan --prompt "Trap Soul a 140 BPM em C# menor"

demo:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py demo --duration 8 --output data/output/demo.wav

load:
	PYTHONPATH=packages $(PYTHON) scripts/load_test_orchestrate.py --requests $(REQUESTS) --concurrency $(CONCURRENCY)

load-studio-master:
	PYTHONPATH=packages $(PYTHON) scripts/load_test_studio_master.py --rounds $(STUDIO_ROUNDS) --concurrency $(CONCURRENCY) --websocket-clients $(STUDIO_WEBSOCKETS)

persona-json:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py persona --format json

persona-prompt:
	PYTHONPATH=packages $(PYTHON) scripts/run_local.py persona --format prompt

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
