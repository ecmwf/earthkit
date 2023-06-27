PROJECT := earthkit
CONDA := conda
CONDAFLAGS :=
COV_REPORT := html

setup:
	pre-commit install

default: qa unit-tests type-check

qa:
	pre-commit run --all-files

unit-tests:
	cd .. && python -m pytest earthkit -vv --cov=. --cov-report=$(COV_REPORT) && cd -

conda-env-update:
	$(CONDA) env update $(CONDAFLAGS) -f environment.yml

docker-build:
	docker build -t $(PROJECT) .

docker-run:
	docker run --rm -ti -v $(PWD):/srv $(PROJECT)

docs-build:
	cd docs && rm -fr _api && make clean && make html
