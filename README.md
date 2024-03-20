# Bet-Maker backend

## First run
1. Create virtual environment and install dependencies
```{shell}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
pip install -r requirements.test.txt
```
2. Install `pre-commit` hooks
```{shell}
pre-commit install-hooks
pre-commit install
```
3. Create `.env` file, don't forget to set proper variables
```{shell}
cp .env_example .env
```

## Running locally
1. Launch server and DB
```{shell}
make up
```
1. Apply migrations
```{shell}
make migrate
```
1. Check http://0.0.0.0:80/docs, everything should be OK!


## Testing
Some steps should be made to run tests.

Tests must be run only with `APP_ENV=TEST`, there will be an error otherwise.

To run tests, stop your container with server (**betmaker_server**) and type:
```{shell}
make run_tests
```
