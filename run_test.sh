#!/bin/bash

# Activate the virtual environment
source python-virtualenv/bin/activate

# Run the tests
python -m unittest discover -v tests/
