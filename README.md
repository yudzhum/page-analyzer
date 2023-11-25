
[![Actions Status](https://github.com/yudzhum/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/yudzhum/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/647510c568941a372d33/maintainability)](https://codeclimate.com/github/yudzhum/python-project-83/maintainability)
![Github Actions Status](https://github.com/yudzhum/python-project-83/actions/workflows/check.yml/badge.svg)

## Page analyzer - a site that analyzes web pages for SEO suitability
[Page analyzer](https://python-project-83-production-3b68.up.railway.app/)
---
## Tech stack

- python = "^3.8"
- flask = "^2.2.3"
- gunicorn = "^20.1.0"
- python-dotenv = "^1.0.0"
- psycopg2-binary = "^2.9.6"
- validators = "^0.20.0"
- requests = "^2.29.0"
- beautifulsoup4 = "^4.12.2"

## Setup
1. Clone repository:\
 `git clone git@github.com:yudzhum/page-analyzer.git`\
2. Install poetry:\
 `make install`
3. Create `.env` file for enviromental variables storage\
4. Create a new PostgreSQL database\
 `make db-build `

## Usage
`make start`
