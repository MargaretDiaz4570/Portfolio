#!/bin/bash


# Make the script executable
chmod +x $PWD/python3-virtualenv/bin/python

# Run the tests
$PWD/python3-virtualenv/bin/python -m unittest discover -v tests/