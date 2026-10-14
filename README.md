# RewriteOS Security Lab

A defensive cybersecurity lab built with Python and Docker.

## Features

- Analyzes simulated authentication logs.
- Counts failed login attempts by IP address.
- Detects addresses with five or more failures.
- Includes automated unit tests.

## Requirements

- Python 3.14 or a compatible Python 3 version.

## Run the analyzer

    python app/analyzer.py

## Run the tests

    python -m unittest discover -s tests -v

## Security scope

Uses fictional log data for educational and defensive purposes.
Does not monitor real systems.

## Roadmap

- [x] Python log analyzer
- [x] Automated unit tests
- [ ] Docker support
- [ ] Docker Compose
- [ ] Security dashboard

## Run with Docker

Build the image:

    docker build -t rewriteos-security-lab:v0.1.0 .

Run the analyzer:

    docker run --rm rewriteos-security-lab:v0.1.0

The container runs as a non-root user and analyzes fictional logs.

## Build note

The project currently supports the standard Docker build command.
