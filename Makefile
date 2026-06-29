PROJECT := earthkit
CONDA := conda
CONDAFLAGS :=
COV_REPORT := html

setup:
	pre-commit install

default: qa unit-tests

qa:
	pre-commit run --all-files

unit-tests:
	cd .. && python -m pytest earthkit -vv --cov=. --cov-report=$(COV_REPORT) && cd -
