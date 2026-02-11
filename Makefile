# Makefile for inspection API (plan tech_1)
# Run from repo root. Uses repo-root .venv (create with: python3 -m venv .venv).

.PHONY: test test-unit test-integration test-contract build deploy lint format run-functions

test: test-unit test-integration test-contract

test-unit:
	cd functions && ../.venv/bin/python -m pytest ../tests/unit -v

test-integration:
	cd functions && ../.venv/bin/python -m pytest ../tests/integration -v

test-contract:
	cd functions && ../.venv/bin/python -m pytest ../tests/contract -v

build:
	.venv/bin/pip install -r functions/requirements.txt

deploy:
	firebase deploy --only functions,firestore,storage

lint:
	cd functions && ../.venv/bin/ruff check .

format:
	cd functions && ../.venv/bin/ruff format .

# Run Cloud Functions locally; uses .venv (symlinked as functions/venv so emulator finds it)
run-functions: build
	ln -sfn ../.venv functions/venv
	firebase emulators:start --only auth,firestore,functions
