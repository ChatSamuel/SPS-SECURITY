# Contributing to SPS SECURITY

Thank you for considering contributing to SPS SECURITY.

## How to contribute

You can contribute in several ways:

- Reporting bugs
- Suggesting features
- Improving documentation
- Adding detection engines
- Enhancing heuristics
- Improving performance

## Development setup

Clone repository:

git clone https://github.com/YOURUSER/sps-security.git

Enter directory:

cd sps-security

Create virtual environment:

python -m venv venv
source venv/bin/activate

Install:

pip install -e .

## Code style

- Python 3.9+
- Follow PEP8
- Keep functions small
- Use descriptive names

## Adding new detection engine

1. Create new file in:
sps_security/actions/

2. Implement scan function

3. Add to CLI menu

4. Update README

## Adding heuristic pattern

Edit:

sps_security/security/heuristic.py

Add pattern to list.

## Commit messages

Use format:

feat: add heuristic pattern
fix: monitor loop issue
docs: update README

## Pull Request process

1. Fork repository
2. Create branch
3. Commit changes
4. Push branch
5. Open Pull Request

## Code of conduct

Be respectful.
No malicious code.
Security-first mindset.
