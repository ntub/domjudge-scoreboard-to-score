SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

test:  ## Run check and test
	echo "Test"
.PHONY: test

lint:  ## Check lint
	poetry run flake8 .
	poetry run pydocstyle .
	poetry run isort --check --diff .
	poetry run black --check --diff .
.PHONY: lint

lint-fix:  ## Fix lint
	poetry run flake8 .
	poetry run pydocstyle .
	poetry run isort .
	poetry run black .
.PHONY: lint

typecheck:  ## Run typechecking
	poetry run mypy --show-error-codes --pretty .
.PHONY: typecheck

ci: lint typecheck test  ## Run all checks (lint, typecheck, test)
.PHONY: ci

clean:  ## Clean cache files
	find . -name '__pycache__' -type d | xargs rm -rvf
	find . -name '.mypy_cache' -type d | xargs rm -rvf
	find . -name '.pytest_cache' -type d | xargs rm -rvf
.PHONY: clean

build:  ## Build Docker image
	echo "Build."
.PHONY: build

.DEFAULT_GOAL := help
help: Makefile
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help
