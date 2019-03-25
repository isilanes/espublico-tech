#!/bin/bash

# Run tests and then show coverage report (only if no errors):
python3 -m unittest discover -s tests -v || exit
