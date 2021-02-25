#!/bin/bash

echo "remember to get 'secret.yaml' (with DB credentials) file first"
python3 -m unittest db_tests.py
