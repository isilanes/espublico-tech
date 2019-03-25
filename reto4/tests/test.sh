#!/bin/bash

# Run tests and then show coverage report (only if no errors):
python -m unittest discover -s tests -v || exit
