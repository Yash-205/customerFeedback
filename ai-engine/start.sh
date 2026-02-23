#!/bin/bash
./venv/bin/python -m uvicorn app.main:app --port 8000 --reload
