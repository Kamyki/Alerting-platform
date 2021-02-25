#!/usr/bin/env python3
import yaml
NAME="services.yaml"
with open(NAME, 'r') as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
