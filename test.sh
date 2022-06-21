#!/bin/bash
export FLASK_CONFIG=testing
coverage run -m pytest --verbose && coverage report -m
