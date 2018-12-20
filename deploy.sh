#!/bin/bash

python setup.py sdist bdist_wheel
pip wheel -r requirements.txt
twine upload dist/*
rm -rf dist/ build/
rm -rf *.whl
