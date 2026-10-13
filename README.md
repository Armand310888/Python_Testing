# Güdlft — Registration Platform

A Flask application for sports club competition registrations, improved as part of **OpenClassrooms Project 11: Debugging and Testing**.

The project focuses on correcting business logic, making the application testable, and validating it through unit, integration, functional, end-to-end, and load tests.

## Repository

**GitHub:** https://github.com/Armand310888/Python_Testing.git

## Features

- Club login using a registered email address.
- Display of upcoming competitions and remaining places.
- Competition booking using club points (one point per place).
- Validation of available points, remaining places, and the limit of **12 places per club per competition**.
- Public view of clubs and their points.
- Logout.

## Technologies

- **Python** and **Flask** — web application.
- **pytest** — automated tests and fixtures.
- **Flask test client** — HTTP integration tests without starting a separate server.
- **pytest-flask** — installed test dependency; the project's own `app` and `client` fixtures rely on pytest and Flask directly.
- **Coverage.py** (`coverage`) — code coverage measurement.
- **Selenium** — end-to-end browser testing with Chrome.
- **Locust** — HTTP load and performance testing.

## Installation

### 1. Clone the repository

Replace `REPOSITORY_URL_HERE` with the HTTPS URL of **your own GitHub fork**:

```bash
git clone https://github.com/Armand310888/Python_Testing.git
cd Python_Testing
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` instead.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

For Selenium tests, Google Chrome and a compatible ChromeDriver (typically managed by recent Selenium versions) must be available.

## Run the application

From the repository root:

```bash
FLASK_APP=server.py python -m flask run
```

Open `http://127.0.0.1:5000` in a browser.

The default application reads its clubs and competitions from the root JSON files. Automated tests use separate datasets to avoid modifying production-like data.

## Project structure

```text
Python_Testing/
├── server.py
├── clubs.json
├── competitions.json
├── requirements.txt
├── .coveragerc
├── README.md
├── templates/
│   ├── index.html
│   ├── welcome.html
│   └── booking.html
├── tests/
│   ├── conftest.py
│   ├── data/
│   │   ├── functional/
│   │   │   ├── clubs.json
│   │   │   ├── competitions.json
│   │   │   └── bookings.json
│   │   └── performance/
│   │       ├── clubs.json
│   │       └── competitions.json
│   ├── unit_tests/
│   ├── integration_tests/
│   ├── functional_tests/
│   │   ├── test_booking_journey.py
│   │   ├── test_selenium_booking.py
│   │   └── selenium_server.py
│   └── performance_tests/
│       ├── generate_data.py
│       ├── locustfile.py
│       └── performance_server.py
└── docs/
    └── locust-report.html
```

## Automated testing

### Unit, integration, and functional tests

```bash
python -m pytest tests/unit_tests tests/integration_tests tests/functional_tests/test_booking_journey.py -v
```

The application factory `create_app()` allows test data and Flask configuration to be injected. Shared pytest fixtures are defined in `tests/conftest.py`.

### Coverage

```bash
coverage run -m pytest tests/unit_tests tests/integration_tests tests/functional_tests/test_booking_journey.py
coverage report -m
```

**Measured result: 100% coverage of `server.py`.** The `.coveragerc` configuration excludes test files from the coverage calculation. Coverage indicates which lines were executed; it does not, by itself, prove that all possible behaviors have been tested.

### Selenium end-to-end test

Run the test Flask server with the dedicated functional dataset in **terminal 1**:

```bash
FLASK_APP=tests/functional_tests/selenium_server.py python -m flask run
```

Then run Selenium in **terminal 2**:

```bash
python -m pytest tests/functional_tests/test_selenium_booking.py -v
```

The scenario checks club login, competition selection, booking submission, confirmation, and updates to the club's points and competition availability.

**Important:** The Selenium test changes the in-memory data of the separate Flask server process. **Stop and restart that Flask server before each new Selenium run** to reset the dataset. Running pytest again without restarting the server may fail because the previous booking is still recorded in memory.

## Load testing with Locust

### Start the performance test server

```bash
FLASK_APP=tests/performance_tests/performance_server.py python -m flask run
```

### Start Locust in a second terminal

```bash
python -m locust -f tests/performance_tests/locustfile.py --host=http://127.0.0.1:5000
```

The `-f` option (`--locustfile`) specifies the Python file defining the simulated users and their tasks.

Open `http://127.0.0.1:8089` and configure **6 concurrent users** and a **2-minute run**. Use the same spawn rate when comparing different runs.

### Latest recorded results — 13 October 2026

| Metric | Result |
| --- | ---: |
| HTTP requests | **349** |
| Failed requests | **0** |
| Average response time | **4.31 ms** |
| Median response time | **3 ms** |
| 95th percentile | **9 ms** |
| 99th percentile | **11 ms** |
| Maximum response time | **18 ms** |
| Average throughput | **2.91 requests/s** |

These measurements describe a short local load test, not production capacity. The previous run (12 October 2026) recorded **364 requests** with **0 failures**.

**[View the full Locust HTML report](docs/locust-report.html)** — keep the `docs/locust-report.html` file alongside this README when committing it to GitHub.

## Notes

- Booking data is held in memory during execution; restarting the application resets that state.
- Test data is separated into functional and performance datasets.
- The project emphasizes reproducible tests and clear separation between test levels.
