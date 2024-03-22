#!/bin/bash

# Run flake8 linting
flake8_result=$(flake8 .)

if [ -z "$flake8_result" ]; then
    echo "No linting errors found."
    exit 0
else
    echo "Linting errors detected:"
    echo "$flake8_result"
    exit 1
fi